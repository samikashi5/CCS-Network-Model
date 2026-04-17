# Optimization Model Formulation

## Objective

Minimize total annualized cost:

- transport cost
- storage cost
- capital recovery for pipelines or trucks if included
- minus any credit such as 45Q, if used in the scenario

## Decision Variables

For each source i:
- y_i = 1 if pipeline is selected, 0 otherwise
- z_i = 1 if trucking is selected, 0 otherwise
- x_i = continuous CO2 flow allocated from source i

If using a mode split formulation, define:
- x_i,pipeline
- x_i,truck

## Core Constraints

- Sink capacity: sum of all inflows <= 2,000,000 tCO2/yr
- Source supply: flow from each source cannot exceed its annual emissions
- Mode exclusivity: choose pipeline or trucking for each source if a single-mode structure is used
- Delivery adjustment: account for boil-off or loss during transport

## Route-Length Usage

The transport length L enters the cost equations through:
- trucking fuel cost
- trucking labor time
- pipeline pressure drop
- pipeline CAPEX and booster station count

## Recommended Formulation Choice

Use a mixed-integer linear or mixed-integer convex approximation:
- binary variables for mode choice
- continuous flow variables for annual throughput
- piecewise or fitted cost functions for pipeline CAPEX if the hydraulic equations are nonlinear

## Expected Output

- cheapest transport mode by source
- optimal annual flow allocation
- total system cost
- sensitivity to discount rate and route length
