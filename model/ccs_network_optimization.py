from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd
import pulp


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"


def crf(discount_rate: float, lifetime_years: int) -> float:
    if discount_rate <= 0:
        return 1.0 / max(lifetime_years, 1)
    growth = (1 + discount_rate) ** lifetime_years
    return discount_rate * growth / (growth - 1)


@dataclass
class Parameters:
    # NEED INFO: Financial assumptions from literature/project financing plan.
    discount_rate: float = 0.10
    asset_lifetime_years: int = 20

    # NEED INFO: Transport/storage assumptions from literature.
    trucking_cost_usd_per_ton_km: float = 0.08
    pipeline_opex_usd_per_ton_km: float = 0.02
    pipeline_capex_usd_per_ton_km: float = 0.01
    storage_cost_usd_per_ton: float = 15.0

    # NEED INFO: Sink capacity and capture target assumptions.
    sink_capacity_tpy: float = 2_000_000.0
    capture_target_tpy: float | None = None


def load_sources(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    base_required = {"source", "lat", "lon", "emissions_tons"}
    missing_base = base_required - set(df.columns)
    if missing_base:
        raise ValueError(f"Missing required columns: {sorted(missing_base)}")

    has_single_distance = "distance_km" in df.columns
    has_two_routes = {"distance_overground_km", "distance_underground_km"}.issubset(df.columns)

    if not has_single_distance and not has_two_routes:
        raise ValueError(
            "Provide either distance_km or both distance_overground_km and distance_underground_km."
        )

    if has_single_distance and not has_two_routes:
        df["distance_overground_km"] = df["distance_km"]
        df["distance_underground_km"] = df["distance_km"]

    numeric_cols = [
        "lat",
        "lon",
        "emissions_tons",
        "distance_overground_km",
        "distance_underground_km",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[numeric_cols].isna().any().any():
        raise ValueError("Found missing/non-numeric values in required numeric columns.")

    if (df["emissions_tons"] < 0).any() or (df["distance_overground_km"] < 0).any() or (df["distance_underground_km"] < 0).any():
        raise ValueError("emissions_tons and distances must be non-negative.")

    return df


def pipeline_unit_cost_usd_per_ton_km(params: Parameters) -> float:
    # Simple annualized pipeline unit cost proxy.
    return params.pipeline_opex_usd_per_ton_km + params.pipeline_capex_usd_per_ton_km * crf(
        params.discount_rate,
        params.asset_lifetime_years,
    )


def build_and_solve_network(sources_df: pd.DataFrame, params: Parameters) -> Dict[str, pd.DataFrame]:
    model = pulp.LpProblem("CCS_MinCost_Network", pulp.LpMinimize)

    sources: List[str] = sources_df["source"].astype(str).tolist()
    emissions = dict(zip(sources_df["source"], sources_df["emissions_tons"]))
    dist_over = dict(zip(sources_df["source"], sources_df["distance_overground_km"]))
    dist_under = dict(zip(sources_df["source"], sources_df["distance_underground_km"]))

    modes = ["pipeline", "truck"]
    routes = ["overground", "underground"]

    flow = pulp.LpVariable.dicts(
        "flow",
        ((s, m, r) for s in sources for m in modes for r in routes),
        lowBound=0,
        cat="Continuous",
    )
    select_mode = pulp.LpVariable.dicts(
        "select_mode",
        ((s, m) for s in sources for m in modes),
        lowBound=0,
        upBound=1,
        cat="Binary",
    )
    select_route = pulp.LpVariable.dicts(
        "select_route",
        ((s, r) for s in sources for r in routes),
        lowBound=0,
        upBound=1,
        cat="Binary",
    )

    pipeline_cost = pipeline_unit_cost_usd_per_ton_km(params)
    truck_cost = params.trucking_cost_usd_per_ton_km

    # L in equations is route distance for each source: overground or underground.
    model += pulp.lpSum(
        flow[(s, "pipeline", "overground")] * (pipeline_cost * dist_over[s] + params.storage_cost_usd_per_ton)
        + flow[(s, "pipeline", "underground")] * (pipeline_cost * dist_under[s] + params.storage_cost_usd_per_ton)
        + flow[(s, "truck", "overground")] * (truck_cost * dist_over[s] + params.storage_cost_usd_per_ton)
        + flow[(s, "truck", "underground")] * (truck_cost * dist_under[s] + params.storage_cost_usd_per_ton)
        for s in sources
    )

    for s in sources:
        model += pulp.lpSum(flow[(s, m, r)] for m in modes for r in routes) <= emissions[s], f"supply_{s}"

        # Binary mode choice per source: pipeline OR truck.
        model += pulp.lpSum(select_mode[(s, m)] for m in modes) == 1, f"one_mode_{s}"
        model += pulp.lpSum(select_route[(s, r)] for r in routes) == 1, f"one_route_{s}"

        for m in modes:
            model += pulp.lpSum(flow[(s, m, r)] for r in routes) <= emissions[s] * select_mode[(s, m)], f"mode_link_{s}_{m}"
        for r in routes:
            model += pulp.lpSum(flow[(s, m, r)] for m in modes) <= emissions[s] * select_route[(s, r)], f"route_link_{s}_{r}"

    # Aemetis sink capacity inequality.
    model += pulp.lpSum(flow[(s, m, r)] for s in sources for m in modes for r in routes) <= params.sink_capacity_tpy, "sink_capacity"

    total_available = float(sources_df["emissions_tons"].sum())
    required_flow = params.capture_target_tpy if params.capture_target_tpy is not None else min(total_available, params.sink_capacity_tpy)
    model += pulp.lpSum(flow[(s, m, r)] for s in sources for m in modes for r in routes) == required_flow, "required_capture"

    model.solve(pulp.PULP_CBC_CMD(msg=False))
    status = pulp.LpStatus[model.status]
    if status != "Optimal":
        raise RuntimeError(f"Optimization failed. Solver status: {status}")

    rows = []
    for s in sources:
        flow_pipeline = sum(float(pulp.value(flow[(s, "pipeline", r)])) for r in routes)
        flow_truck = sum(float(pulp.value(flow[(s, "truck", r)])) for r in routes)
        route_over = int(round(float(pulp.value(select_route[(s, "overground")]))))
        route_under = int(round(float(pulp.value(select_route[(s, "underground")]))))
        mode_pipeline = int(round(float(pulp.value(select_mode[(s, "pipeline")]))))
        mode_truck = int(round(float(pulp.value(select_mode[(s, "truck")]))))
        chosen_route = "overground" if route_over == 1 else "underground"
        chosen_distance = dist_over[s] if route_over == 1 else dist_under[s]

        rows.append(
            {
                "source": s,
                "emissions_tons": emissions[s],
                "selected_pipeline": mode_pipeline,
                "selected_truck": mode_truck,
                "selected_overground": route_over,
                "selected_underground": route_under,
                "chosen_route": chosen_route,
                "L_km": chosen_distance,
                "flow_pipeline_tons": flow_pipeline,
                "flow_truck_tons": flow_truck,
                "flow_total_tons": flow_pipeline + flow_truck,
            }
        )

    allocation_df = pd.DataFrame(rows)
    summary_df = pd.DataFrame(
        [
            {
                "status": status,
                "objective_total_cost_usd_per_year": float(pulp.value(model.objective)),
                "total_flow_tons_per_year": float(allocation_df["flow_total_tons"].sum()),
                "sink_capacity_tpy": params.sink_capacity_tpy,
                "capture_target_tpy": required_flow,
                "discount_rate": params.discount_rate,
                "asset_lifetime_years": params.asset_lifetime_years,
                "pipeline_unit_cost_usd_per_ton_km": pipeline_cost,
                "truck_unit_cost_usd_per_ton_km": truck_cost,
                "storage_cost_usd_per_ton": params.storage_cost_usd_per_ton,
            }
        ]
    )
    variables_df = pd.DataFrame(
        [{"var_name": v.name, "value": float(v.varValue)} for v in model.variables()]
    )

    return {"allocation": allocation_df, "summary": summary_df, "variables": variables_df}


def save_results(results: Dict[str, pd.DataFrame]) -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    results["allocation"].to_csv(OUTPUTS_DIR / "allocation_results.csv", index=False)
    results["summary"].to_csv(OUTPUTS_DIR / "summary_results.csv", index=False)
    results["variables"].to_csv(OUTPUTS_DIR / "decision_variables.csv", index=False)


def print_results(results: Dict[str, pd.DataFrame]) -> None:
    print("\n=== Summary ===")
    print(results["summary"].to_string(index=False, float_format=lambda x: f"{x:,.4f}"))
    print("\n=== Allocation ===")
    print(results["allocation"].to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    print("\n=== Decision Variables ===")
    for _, row in results["variables"].iterrows():
        print(f"{row['var_name']} {row['value']}")


def main() -> None:
    sources_path = DATA_DIR / "sources.csv"
    if not sources_path.exists():
        raise FileNotFoundError("Missing required input file: data/sources.csv")

    sources_df = load_sources(sources_path)
    params = Parameters()
    results = build_and_solve_network(sources_df, params)
    save_results(results)
    print_results(results)


if __name__ == "__main__":
    main()
