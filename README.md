
# CCS-Network-Model
=======
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

## Next Steps (In Order)

1. Replace sample source data with real top-5 facility data.
2. Replace all NEED INFO parameter values with literature-backed values.
3. Re-run the model and inspect output tables.
4. Document assumptions and sources in docs/parameters.md and docs/network_data.md.
