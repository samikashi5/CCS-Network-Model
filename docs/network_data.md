# Network Data Requirements

## Top 5 Source Facilities

Use the five nearest major stationary CO2 sources to Aemetis.

Required file: data/sources.csv

Required columns:

- source
- lat
- lon
- emissions_tons
- distance_overground_km
- distance_underground_km

## How L Enters The Equations

For each source i, route r, and mode m:

- If route is overground, L_i = distance_overground_km
- If route is underground, L_i = distance_underground_km

Transport term in objective is of form:

cost_(i,m,r) = flow_(i,m,r) * (unit_cost_m * L_i + storage_cost)

So L is explicitly route-specific.

## Route Comparison Rule

Model compares both route choices for each source:

- overground
- underground

and picks one route per source via a binary route variable.

## Data Status

✅ **VERIFIED:**
- Top 5 source facilities: Populated in data/sources.csv
- Annual emissions per source: Populated (ranging 180,000–520,000 tons/year)
- Overground and underground route distances: Populated for all 5 sources
- Route distance methodology: Overground = road distances; Underground = pipeline corridor estimates

## Suggested Sources

- EPA eGRID / GHGRP datasets
- California Air Resources Board and local district inventories
- permit filings and sustainability disclosures
- GIS road/pipeline corridor estimates for route distances
