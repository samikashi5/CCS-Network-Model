import math

# Exact coordinates from Google Maps
sources = {
    "Los_Angeles_Refinery_Carson": (33.8066091, -118.2453533),
    "Chevron_Richmond_Refinery_Richmond": (37.9327902, -122.3939549),
    "Martinez_Refining_Company_Martinez": (38.0132956, -122.1059974),
    "Chevron_El_Segundo_Refinery_El_Segundo": (33.9158229, -118.4189695),
    "Valero_Benicia_Refinery_Benicia": (38.0527, -122.1589),
}

# Aemetis storage facility near Modesto (central valley)
sink = (37.64, -120.99)

def haversine(coord1, coord2):
    """Calculate great-circle distance in km"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    R = 6371  # Earth radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

# Calculate distances
print("Great-circle distances from each refinery to Modesto/Aemetis:\n")
print("Source | Straight Line (km) | Road Distance Est. (km) | Pipeline Est. (km)")
print("-" * 80)

road_factor = 1.15  # Roads are ~15% longer than straight line
pipeline_factor = 1.05  # Pipelines are ~5% longer (more direct routing possible)

for name, coord in sources.items():
    straight = haversine(coord, sink)
    road = straight * road_factor
    pipeline = straight * pipeline_factor
    print(f"{name:45} | {straight:18.1f} | {road:23.1f} | {pipeline:17.1f}")

# Now create the CSV with proper distances
print("\n" + "="*80)
print("Updated sources.csv with calculated distances:\n")

csv_data = [
    ("Los_Angeles_Refinery_Carson", 33.8066091, -118.2453533, 5840000),
    ("Chevron_Richmond_Refinery_Richmond", 37.9327902, -122.3939549, 4370000),
    ("Martinez_Refining_Company_Martinez", 38.0132956, -122.1059974, 3650000),
    ("Chevron_El_Segundo_Refinery_El_Segundo", 33.9158229, -118.4189695, 3150000),
    ("Valero_Benicia_Refinery_Benicia", 38.0527, -122.1589, 2670000),
]

print("source,lat,lon,emissions_tons,distance_overground_km,distance_underground_km")
for name, lat, lon, emissions in csv_data:
    straight = haversine((lat, lon), sink)
    road = round(straight * road_factor, 0)
    pipeline = round(straight * pipeline_factor, 0)
    print(f"{name},{lat},{lon},{emissions},{int(road)},{int(pipeline)}")
