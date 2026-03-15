"""
Script to generate realistic sample energy operational data.
Run once to produce sample_energy_data.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

sites = ["Site_A_HongKong", "Site_B_Shenzhen", "Site_C_Shanghai",
         "Site_D_Beijing", "Site_E_Guangzhou"]

start = datetime(2024, 1, 1)
records = []

for site in sites:
    base_consumption = np.random.uniform(400, 900)
    base_solar = np.random.uniform(50, 200)
    for day in range(365):
        dt = start + timedelta(days=day)
        month = dt.month
        seasonal = 1 + 0.3 * np.sin((month - 1) / 12 * 2 * np.pi)
        noise = np.random.normal(0, 0.05)
        is_anomaly = np.random.random() < 0.02  # 2% anomaly rate

        consumption = base_consumption * seasonal * (1 + noise)
        if is_anomaly:
            consumption *= np.random.uniform(1.4, 1.8)

        solar = base_solar * max(0, np.sin((month - 3) / 12 * 2 * np.pi) + 0.5)
        solar *= np.random.uniform(0.85, 1.15)

        wind = np.random.uniform(20, 80) * (1 + 0.2 * np.random.randn())
        grid = max(0, consumption - solar - wind)
        co2 = grid * 0.233  # kg CO2 per kWh (HK grid factor)

        records.append({
            "date": dt.strftime("%Y-%m-%d"),
            "site": site,
            "consumption_kwh": round(consumption, 2),
            "solar_production_kwh": round(max(0, solar), 2),
            "wind_production_kwh": round(max(0, wind), 2),
            "grid_import_kwh": round(grid, 2),
            "co2_emissions_kg": round(co2, 2),
            "peak_demand_kw": round(consumption * np.random.uniform(0.12, 0.18), 2),
            "is_anomaly": is_anomaly,
        })

df = pd.DataFrame(records)
df.to_csv("sample_energy_data.csv", index=False)
print(f"Generated {len(df)} records across {len(sites)} sites.")
print(df.head())
