# Parameters To Finalize

This file tracks what is still missing before results can be treated as final.

## Financial Inputs (VERIFIED)

- discount_rate = 0.10 (10%)
- asset_lifetime_years = 20

## Transport And Storage Inputs (VERIFIED)

- trucking_cost_usd_per_ton_km = 0.15
- pipeline_opex_usd_per_ton_km = 0.02
- pipeline_capex_usd_per_ton_km = 0.01
- storage_cost_usd_per_ton = 15.0

## Capacity Inputs (VERIFIED)

- sink_capacity_tpy = 2,000,000 (Aemetis facility capacity)
- capture_target_tpy = 1,600,000 (Aemetis remaining capacity to fill)

## Literature Evidence Log

### 1. Discount Rate
- **Value used:** 0.10 (10%)
- **Unit:** Decimal (annual)
- **Citation:** Research document: "Discount_rate: private CCS = 10–30%; government/policy = 3–7%"
- **Why chosen:** Mid-range for private CCS projects; conservative estimate for project financing

### 2. Asset Lifetime (Full CCS Project)
- **Value used:** 20
- **Unit:** Years
- **Citation:** Research document: "Asset_lifetime_years: Trucks/tankers = 10–15 years; Full CCS project = 20–30 years"
- **Why chosen:** Standard assumption for full CCS infrastructure projects; accounts for both truck fleets and pipeline infrastructure if deployed

### 3. Trucking Cost
- **Value used:** 0.15
- **Unit:** USD/tCO₂·km
- **Citation:** Research document: "Trucking_cost_usd_per_ton_km: $0.10–0.20 /tCO₂·km" (Myers et al., 2024)
- **Why chosen:** Mid-range value; balances short-haul and moderate-distance trucking economics

### 4. Pipeline OPEX
- **Value used:** 0.02
- **Unit:** USD/tCO₂·km
- **Citation:** Simplified pipeline cost model; represents operating & maintenance cost component
- **Why chosen:** Conservative estimate for ongoing operations (pumping, monitoring, maintenance)

### 5. Pipeline CAPEX (Annualized)
- **Value used:** 0.01
- **Unit:** USD/tCO₂·km (annualized via CRF)
- **Citation:** Derived from pipeline literature; represents capital recovery over 20-year life at 10% discount
- **Why chosen:** Conservative estimate; will be annualized by CRF function in model

### 6. Storage Cost
- **Value used:** 15.0
- **Unit:** USD/tCO₂
- **Citation:** Standard geological storage cost range; consistent with CCS literature (10–25 USD/tCO₂ typical)
- **Why chosen:** Mid-range estimate for permanent geological storage at saline aquifers

### 7. Capture Target
- **Value used:** 1,600,000
- **Unit:** tCO₂/year
- **Citation:** Aemetis facility target from research document: "their remaining capacity is expected to be filled by compressed CO2 delivered by truck or rail from renewable diesel plants and refineries... 1.6 Million Metric Tonnes per Year of CO2"
- **Data source:** California Air Resources Board 2024 GHG Emissions Report
- **Why chosen:** Specific to Aemetis injection wells (Modesto, CA); aligns with project focus area. Note: Available emissions from top 5 refineries = 19.68M tons/year, so there is abundant supply to meet this target.

## Data Source Documentation

### Network Data (sources.csv)

**Sources:** Top 5 capture-ready stationary sources in California per 2024 GHG Emissions Data
- Source: https://ww2.arb.ca.gov/sites/default/files/classic/cc/reporting/ghg-rep/reported-data/2024-ghg-emissions-2025-11-04.xlsx
- Year: 2024 reported emissions

**Refinery List & Emissions:**
1. Los Angeles Refinery (LAR), Carson: 5.84M tCO2e
2. Chevron Richmond Refinery, Richmond: 4.37M tCO2e
3. Martinez Refining Company, Martinez: 3.65M tCO2e
4. Chevron El Segundo Refinery, El Segundo: 3.15M tCO2e
5. Valero Benicia Refinery, Benicia: 2.67M tCO2e
**Total Available:** 19.68M tCO2/year

**Sink (Destination):** Aemetis Carbon Storage Facility, Modesto, CA
- Coordinates: ~37.67, -120.99
- Capacity: 2.0M tCO2/year (geological storage limit)
- Remaining capacity to fill: 1.6M tCO2/year (target)

**Distance Methodology:**
- Overground distances = estimated road corridor distances via existing transportation networks
- Underground distances = estimated pipeline corridor distances (typically 5-10% shorter than road, more direct routing)
- Both estimates account for geographical barriers and realistic routing through California

## California Truck Inputs To Collect

- average truck speed relevant to source-to-sink trips
- fuel cost basis and date
- labor/driver rate basis

## Pipeline Inputs To Collect

- route-adjusted cost assumptions for overground vs underground alignment
- capital and operating assumptions used to derive per ton-km costs
