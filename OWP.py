from playwright.sync_api import sync_playwright
import pandas as pd
import re
import math
import tqdm
import time
import sys

resolution= sys.argv[1]
resolution = int(resolution)  # Convert to integer
GTI = sys.argv[2]
GTI = float(GTI)  # Convert to integer
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
# Input coordinates
coordinates = list(generate_montana_grid(resolution))  # 100 km resolution



# Output storage
data = []

def extract_precip_values(text_block):
    pattern = re.compile(
        r"1d\s+(\d+)\s*%[\s\S]*?\(\s*[\d.\-]+\s*-\s*[\d.]+\s*\)\s*[\d.]+\s*\(\s*[\d.\-]+\s*-\s*[\d.]+\s*\)\s*([\d.]+)\s*\(\s*[\d.\-]+\s*-\s*[\d.]+\s*\)",
        re.MULTILINE
    )
    matches = pattern.findall(text_block)
    aep_dict = {int(aep): float(value) for aep, value in matches if int(aep) in [50, 20, 10, 4, 2, 1]}
    return [aep_dict.get(x, None) for x in [50, 20, 10, 4, 2, 1]]

start_time = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for lon, lat in coordinates:
        page = browser.new_page()
        url = f"https://water.noaa.gov/precip-frequency/atlas15/pilot#@={lon},{lat},4.9&bm=topographic&ts=am&pt=depth&u=english&aep=50&ci=90&d=1d&future=gwl&prediction=gwl&period1=3&period2={GTI}"
        page.goto(url)
        print(f"Processing {lon}, {lat}")
        page.wait_for_timeout(1000)  # 1 second wait

        # Extract visible text
        content = page.evaluate("""
            () => {
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                let node, textContent = [];
                while (node = walker.nextNode()) {
                    const trimmed = node.textContent.trim();
                    if (trimmed) {
                        textContent.push(trimmed);
                    }
                }
                return textContent.join('\\n');
            }
        """)


        # Extract precipitation values for 1-day
        values = extract_precip_values(content)

        data.append({
            'Longitude': lon,
            'Latitude': lat,
            'AEP_50%_in': values[0],
            'AEP_20%_in': values[1],
            'AEP_10%_in': values[2],
            'AEP_4%_in': values[3],
            'AEP_2%_in': values[4],
            'AEP_1%_in': values[5],
        })

        page.close()

    browser.close()
end_time = time.time()-start_time
print(f"Time taken: {end_time:.2f} seconds")
# Save results
df = pd.DataFrame(data)
df.to_csv(f"precipitation_results_1d_{GTI}C_{resolution}KM.csv", index=False)

