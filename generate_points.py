import math

def generate_montana_grid(res_km=5):
    # Approximate bounding box for Montana
    min_lat, max_lat = 44.2, 49.0
    min_lon, max_lon = -116.1, -104.0
    
    # Step size: convert km to degrees
    deg_per_km_lat = 1 / 111  # 1° lat ~111 km
    deg_per_km_lon = 1 / (111 * math.cos(math.radians((min_lat + max_lat) / 2)))  # adjust for latitude

    lat_step = res_km * deg_per_km_lat
    lon_step = res_km * deg_per_km_lon

    grid_points = []
    lat = min_lat
    while lat <= max_lat:
        lon = min_lon
        while lon <= max_lon:
            grid_points.append((round(lon, 4), round(lat, 4)))
            lon += lon_step
        lat += lat_step

    return grid_points
print(generate_montana_grid(100))
print(len(generate_montana_grid(100)))