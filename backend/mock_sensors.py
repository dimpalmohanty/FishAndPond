"""
mock_sensors.py
---------------
Simulates IoT sensor readings for fish ponds.

PRODUCTION SWAP NOTE:
    In production, replace `get_pond_data()` with a real API call:

    def get_pond_data(pond_id: str):
        response = requests.get(f"https://your-dotnet-api.com/ponds/{pond_id}/sensors")
        return response.json()

    Function name and return shape stay IDENTICAL — nothing else changes.
"""

import random
from datetime import datetime


# Realistic sensor ranges for healthy fish ponds
SENSOR_RANGES = {
    "ph":                 (6.0, 9.0),    # ideal: 6.5 - 8.5
    "temperature_c":      (20.0, 35.0),  # ideal: 25 - 30
    "dissolved_oxygen":   (2.0, 9.0),    # ideal: 5+ mg/L
    "ammonia_ppm":        (0.0, 2.0),    # ideal: < 0.5 ppm
    "turbidity_ntu":      (5.0, 80.0),   # ideal: 10 - 40 NTU
    "algae_index":        (0.0, 1.0),    # 0 = none, 1 = heavy bloom
    "nitrite_ppm":        (0.0, 1.0),    # ideal: < 0.1 ppm
    "water_depth_m":      (1.0, 3.5),    # pond depth in meters
}

# Pre-seeded pond profiles so readings feel consistent per pond
POND_PROFILES = {
    "pond_1": {
        "name": "Pond 1 - Rohu Stock",
        "fish_type": "Rohu (Labeo rohita)",
        "fish_count": 1200,
        "area_sqm": 500,
        # offsets to make each pond feel different
        "offsets": {"ph": 0.3, "temperature_c": 0, "dissolved_oxygen": 0.5,
                    "ammonia_ppm": -0.1, "algae_index": 0.1}
    },
    "pond_2": {
        "name": "Pond 2 - Catla Stock",
        "fish_type": "Catla (Catla catla)",
        "fish_count": 800,
        "area_sqm": 350,
        "offsets": {"ph": -0.4, "temperature_c": 1.5, "dissolved_oxygen": -1.0,
                    "ammonia_ppm": 0.3, "algae_index": 0.2}
    },
    "pond_3": {
        "name": "Pond 3 - Mixed Carp",
        "fish_type": "Mixed Carp",
        "fish_count": 2000,
        "area_sqm": 800,
        "offsets": {"ph": 0.1, "temperature_c": -1.0, "dissolved_oxygen": 1.0,
                    "ammonia_ppm": 0.5, "algae_index": -0.1}
    },
}


def _clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def get_pond_data(pond_id: str) -> dict:
    """
    Returns current sensor readings for a given pond.

    Args:
        pond_id: One of 'pond_1', 'pond_2', 'pond_3'

    Returns:
        dict with all sensor readings + pond metadata
    """
    if pond_id not in POND_PROFILES:
        pond_id = "pond_1"

    profile = POND_PROFILES[pond_id]
    offsets = profile["offsets"]

    # Generate randomized but realistic readings
    ph_base           = random.uniform(6.5, 8.2)
    temp_base         = random.uniform(26.0, 31.0)
    do_base           = random.uniform(4.5, 7.5)
    ammonia_base      = random.uniform(0.1, 0.7)
    turbidity_base    = random.uniform(15.0, 45.0)
    algae_base        = random.uniform(0.1, 0.5)
    nitrite_base      = random.uniform(0.02, 0.3)
    depth_base        = random.uniform(1.5, 3.0)

    return {
        # Pond metadata
        "pond_id":         pond_id,
        "pond_name":       profile["name"],
        "fish_type":       profile["fish_type"],
        "fish_count":      profile["fish_count"],
        "area_sqm":        profile["area_sqm"],

        # Sensor readings
        "ph":              round(_clamp(ph_base + offsets.get("ph", 0), 5.5, 9.5), 2),
        "temperature_c":   round(_clamp(temp_base + offsets.get("temperature_c", 0), 18.0, 38.0), 1),
        "dissolved_oxygen":round(_clamp(do_base + offsets.get("dissolved_oxygen", 0), 1.0, 10.0), 2),
        "ammonia_ppm":     round(_clamp(ammonia_base + offsets.get("ammonia_ppm", 0), 0.0, 3.0), 3),
        "turbidity_ntu":   round(_clamp(turbidity_base, 5.0, 100.0), 1),
        "algae_index":     round(_clamp(algae_base + offsets.get("algae_index", 0), 0.0, 1.0), 2),
        "nitrite_ppm":     round(_clamp(nitrite_base, 0.0, 1.5), 3),
        "water_depth_m":   round(depth_base, 2),

        # Meta
        "last_updated":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status":          "live",
    }


def get_all_ponds_summary() -> list:
    """Returns a summary of all ponds — useful for dashboard display."""
    return [get_pond_data(pid) for pid in POND_PROFILES.keys()]


def get_safe_ranges() -> dict:
    """Returns the ideal safe ranges for each parameter — injected into AI context."""
    return {
        "ph":                 {"min": 6.5,  "max": 8.5,  "unit": ""},
        "temperature_c":      {"min": 25.0, "max": 30.0, "unit": "°C"},
        "dissolved_oxygen":   {"min": 5.0,  "max": 9.0,  "unit": "mg/L"},
        "ammonia_ppm":        {"min": 0.0,  "max": 0.5,  "unit": "ppm"},
        "turbidity_ntu":      {"min": 10.0, "max": 40.0, "unit": "NTU"},
        "algae_index":        {"min": 0.0,  "max": 0.3,  "unit": "(0-1 scale)"},
        "nitrite_ppm":        {"min": 0.0,  "max": 0.1,  "unit": "ppm"},
    }
