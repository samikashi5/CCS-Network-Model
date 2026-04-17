# CCS Transport And Storage Network Optimization

## Research Question

How can a CO2 pipeline and storage network be designed to minimize total transport and storage costs for captured emissions from major stationary sources while accounting for storage capacity and infrastructure constraints?

## Project Goal

Build a clean optimization model for the top 5 nearby sources around the Aemetis site, choosing:

- transport mode (pipeline or truck)
- route type (overground or underground)
- annual transported flow from each source

while enforcing sink capacity and source emission limits.

## What Is Implemented

- Binary variable per source for mode choice
- Binary variable per source for route choice
- Continuous flow variable by source/mode/route
- Objective: minimize total transport + storage cost
- Constraints:
	- source flow limit
	- sink capacity: sum of all flows <= 2,000,000 tCO2/yr
	- one mode per source
	- one route per source

## Required Input Data

File: data/sources.csv

Columns:

source,lat,lon,emissions_tons,distance_overground_km,distance_underground_km

Where L in equations is:

- L = distance_overground_km when overground route is selected
- L = distance_underground_km when underground route is selected

## Missing Information You Must Fill

Edit model/ccs_network_optimization.py and update all fields marked NEED INFO in class Parameters:

- discount_rate
- asset_lifetime_years
- trucking_cost_usd_per_ton_km
- pipeline_opex_usd_per_ton_km
- pipeline_capex_usd_per_ton_km
- storage_cost_usd_per_ton
- sink_capacity_tpy (default is 2,000,000)
- capture_target_tpy (optional)

## Run

From the project root:

1. pip install -r requirements.txt
2. python model/ccs_network_optimization.py

Outputs:

- outputs/summary_results.csv
- outputs/allocation_results.csv
- outputs/decision_variables.csv

## How To Read The Output Files (Very Simple Guide)

Think of the 3 output files as:

- one summary card,
- one detailed decision table,
- one technical audit log.

### 1) outputs/summary_results.csv (Summary Card)

What it does:

- Gives one quick row that answers: Did the model run, how much CO2 was handled, and what was the total cost?

What the main columns mean:

- status: Did the solve work? "Optimal" means yes, the model found the best valid answer.
- objective_total_cost_usd_per_year: Total yearly system cost in USD.
- total_flow_tons_per_year: Total CO2 moved to storage per year.
- sink_capacity_tpy: Maximum the sink can accept per year.
- capture_target_tpy: How much CO2 the model was required to capture.

Other columns (assumptions used):

- discount_rate and asset_lifetime_years: Finance assumptions for pipeline capex annualization.
- pipeline_unit_cost_usd_per_ton_km and truck_unit_cost_usd_per_ton_km: Transport cost assumptions.
- storage_cost_usd_per_ton: Storage cost assumption.

Use this file when you want the big picture first.

### 2) outputs/allocation_results.csv (Detailed Decision Table)

What it does:

- Shows each source and exactly what the model decided for that source.

What the columns mean in plain language:

- source: Which plant/facility row you are looking at.
- emissions_tons: Max CO2 available from that source.
- selected_pipeline / selected_truck: Which transport mode was chosen.
	- 1 = chosen
	- 0 = not chosen
- selected_overground / selected_underground: Which route type was chosen.
	- 1 = chosen
	- 0 = not chosen
- chosen_route: Same route choice, written as text for readability.
- L_km: Distance used for that chosen route.
- flow_pipeline_tons: Tons moved by pipeline from that source.
- flow_truck_tons: Tons moved by truck from that source.
- flow_total_tons: Total tons moved from that source.

Use this file when someone asks: "What happened at each source?"

### 3) outputs/decision_variables.csv (Technical Audit Log)

What it does:

- Stores the raw variable values directly from the solver.
- Best for debugging, validation, and checking model internals.

Columns:

- var_name: Internal variable name.
- value: Solved value for that variable.

Common variable name patterns:

- flow_(source, mode, route): How much flow was assigned.
- select_mode_(source, ...): Which mode binary variable is on/off.
- select_route_(source, ...): Which route binary variable is on/off.

Use this file when you need technical proof of the exact solve decisions.

## Fast Way To Read Results (In Order)

1. Open outputs/summary_results.csv to confirm the run worked and see the total cost/flow.
2. Open outputs/allocation_results.csv to see decisions source by source.
3. Open outputs/decision_variables.csv only if you need a deeper technical check.

If you are presenting results to non-technical teammates, start with summary_results.csv and allocation_results.csv.

## Next Steps (In Order)

1. Replace sample source data with real top-5 facility data.
2. Replace all NEED INFO parameter values with literature-backed values.
3. Re-run the model and inspect output tables.
4. Document assumptions and sources in docs/parameters.md and docs/network_data.md.
