# Project Requirements

## Problem Context

Carbon capture and storage is often discussed in terms of capture technology, but one of the biggest barriers to large-scale deployment is what happens after CO2 is captured. The CO2 must be transported and permanently stored safely and cost-effectively. Emission sources and geologic storage sites are not always colocated, and storage sites have capacity limits. This project focuses on designing an efficient regional transport and storage network under those real-world constraints.

## Research Question

How can a CO2 pipeline and storage network be designed to minimize total transport and storage costs for captured emissions from major stationary sources while accounting for storage capacity and infrastructure constraints?

## Required Model Structure

1. Decision variables:
	- binary mode variable per source (pipeline vs truck)
	- binary route variable per source (overground vs underground)
	- continuous flow variable per source/mode/route
2. Objective:
	- minimize total transport + storage cost
3. Constraints:
	- source flow <= source annual emissions
	- sink capacity: sum of all inflows <= 2,000,000 tCO2/yr
	- one mode selected per source
	- one route selected per source

## Required Data Inputs

1. Network data:
	- top 5 nearby source locations
	- overground and underground route distances to sink
2. Source emissions:
	- annual CO2 tons per source
3. Literature coefficients:
	- transport costs and other model coefficients for trucking/pipeline assumptions
4. Financial inputs:
	- discount rate and asset lifetime (if annualizing capex assumptions)

## Current Missing Information (NEED INFO)

- verified top-5 source list
- verified route distances for overground and underground alternatives
- literature-backed trucking and pipeline cost coefficients
- finalized financial assumptions

## Deliverables

- optimized allocation table by source
- selected mode and route by source
- model summary with objective value and sink utilization
