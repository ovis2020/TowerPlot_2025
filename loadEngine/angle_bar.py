STEEL_DENSITY = 7850  # kg/m³
STEEL_DENSITY_IMPERIAL = 0.2836  # lb/in³

def calculate_linear_weight(pa: float, t: float) -> float:
    """
    Calculate linear weight of angle bar.
    
    Args:
        pa: Profile angle dimension in mm
        t: Thickness in mm
    
    Returns:
        Linear weight in kg/m
    """
    pa_m = pa / 1000
    t_m = t / 1000
    
    # Cross-sectional area (m²)
    area = (2 * pa_m * t_m - t_m**2)
    
    # Linear weight (kg/m)
    return round(area * STEEL_DENSITY, 4)

def calculate_linear_weight_imperial(pa: float, t: float) -> float:
    """
    Calculate linear weight of angle bar in imperial units.

    Args:
        pa: Profile angle dimension in inches
        t: Thickness in inches

    Returns:
        Linear weight in kg/m
    """
    pa_m = pa * 25.4 / 1000  # Convert inches to meters
    t_m = t * 25.4 / 1000  # Convert inches to meters
    
    # Cross-sectional area (m²)
    area = (2 * pa_m * t_m - t_m**2)
    
    # Linear weight (kg/m)
    return round(area * STEEL_DENSITY, 4)

# Complete ANGLE_BARS_SI dictionary with linear weight for each bar
ANGLE_BARS_SI = {
    # 1-inch width bars (25 mm)
    "L25x25x2": {"pa": 25, "t": 2, "weight_per_meter": calculate_linear_weight(25, 2)},
    "L25x25x3": {"pa": 25, "t": 3, "weight_per_meter": calculate_linear_weight(25, 3)},
    "L25x25x4": {"pa": 25, "t": 4, "weight_per_meter": calculate_linear_weight(25, 4)},
    "L25x25x5": {"pa": 25, "t": 5, "weight_per_meter": calculate_linear_weight(25, 5)},
    "L25x25x6": {"pa": 25, "t": 6, "weight_per_meter": calculate_linear_weight(25, 6)},
    "L25x25x8": {"pa": 25, "t": 8, "weight_per_meter": calculate_linear_weight(25, 8)},
    "L25x25x10": {"pa": 25, "t": 10, "weight_per_meter": calculate_linear_weight(25, 10)},
    "L25x25x12": {"pa": 25, "t": 12, "weight_per_meter": calculate_linear_weight(25, 12)},

    # 2-inch width bars (50 mm)
    "L50x50x2": {"pa": 50, "t": 2, "weight_per_meter": calculate_linear_weight(50, 2)},
    "L50x50x3": {"pa": 50, "t": 3, "weight_per_meter": calculate_linear_weight(50, 3)},
    "L50x50x4": {"pa": 50, "t": 4, "weight_per_meter": calculate_linear_weight(50, 4)},
    "L50x50x5": {"pa": 50, "t": 5, "weight_per_meter": calculate_linear_weight(50, 5)},
    "L50x50x6": {"pa": 50, "t": 6, "weight_per_meter": calculate_linear_weight(50, 6)},
    "L50x50x8": {"pa": 50, "t": 8, "weight_per_meter": calculate_linear_weight(50, 8)},
    "L50x50x10": {"pa": 50, "t": 10, "weight_per_meter": calculate_linear_weight(50, 10)},
    "L50x50x12": {"pa": 50, "t": 12, "weight_per_meter": calculate_linear_weight(50, 12)},

    # 3-inch width bars (75 mm)
    "L75x75x2": {"pa": 75, "t": 2, "weight_per_meter": calculate_linear_weight(75, 2)},
    "L75x75x3": {"pa": 75, "t": 3, "weight_per_meter": calculate_linear_weight(75, 3)},
    "L75x75x4": {"pa": 75, "t": 4, "weight_per_meter": calculate_linear_weight(75, 4)},
    "L75x75x5": {"pa": 75, "t": 5, "weight_per_meter": calculate_linear_weight(75, 5)},
    "L75x75x6": {"pa": 75, "t": 6, "weight_per_meter": calculate_linear_weight(75, 6)},
    "L75x75x8": {"pa": 75, "t": 8, "weight_per_meter": calculate_linear_weight(75, 8)}
}

# Complete ANGLE_BARS_IMPERIAL dictionary with linear weight for each bar
ANGLE_BARS_IMPERIAL = {
    # 1-inch width bars
    "L1x1x1/8": {"pa": round(1 * 25.4, 2), "t": round(1/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(1, 1/8)},
    "L1x1x3/16": {"pa": round(1 * 25.4, 2), "t": round(3/16 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(1, 3/16)},
    "L1x1x1/4": {"pa": round(1 * 25.4, 2), "t": round(1/4 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(1, 1/4)},
    "L1x1x5/16": {"pa": round(1 * 25.4, 2), "t": round(5/16 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(1, 5/16)},
    "L1x1x3/8": {"pa": round(1 * 25.4, 2), "t": round(3/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(1, 3/8)},
    "L1x1x1/2": {"pa": round(1 * 25.4, 2), "t": round(1/2 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(1, 1/2)},

    # 2-inch width bars
    "L2x2x1/8": {"pa": round(2 * 25.4, 2), "t": round(1/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(2, 1/8)},
    "L2x2x3/16": {"pa": round(2 * 25.4, 2), "t": round(3/16 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(2, 3/16)},
    "L2x2x1/4": {"pa": round(2 * 25.4, 2), "t": round(1/4 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(2, 1/4)},
    "L2x2x5/16": {"pa": round(2 * 25.4, 2), "t": round(5/16 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(2, 5/16)},
    "L2x2x3/8": {"pa": round(2 * 25.4, 2), "t": round(3/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(2, 3/8)},
    "L2x2x1/2": {"pa": round(2 * 25.4, 2), "t": round(1/2 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(2, 1/2)},

    # 3-inch width bars
    "L3x3x1/8": {"pa": round(3 * 25.4, 2), "t": round(1/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(3, 1/8)},
    "L3x3x3/16": {"pa": round(3 * 25.4, 2), "t": round(3/16 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(3, 3/16)},
    "L3x3x1/4": {"pa": round(3 * 25.4, 2), "t": round(1/4 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(3, 1/4)},
    "L3x3x5/16": {"pa": round(3 * 25.4, 2), "t": round(5/16 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(3, 5/16)},
    "L3x3x3/8": {"pa": round(3 * 25.4, 2), "t": round(3/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(3, 3/8)},
    "L3x3x1/2": {"pa": round(3 * 25.4, 2), "t": round(1/2 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(3, 1/2)}
}

ROUND_BARS_SI = {
    # SI Round Bars (Diameter in mm)
    "R12.7x2": {"pa": 12.7, "t": 2, "weight_per_meter": calculate_linear_weight(12.7, 2)},
    "R12.7x4": {"pa": 12.7, "t": 4, "weight_per_meter": calculate_linear_weight(12.7, 4)},
    "R25.4x2": {"pa": 25.4, "t": 2, "weight_per_meter": calculate_linear_weight(25.4, 2)},
    "R25.4x4": {"pa": 25.4, "t": 4, "weight_per_meter": calculate_linear_weight(25.4, 4)},
    "R38.1x2": {"pa": 38.1, "t": 2, "weight_per_meter": calculate_linear_weight(38.1, 2)},
    "R38.1x4": {"pa": 38.1, "t": 4, "weight_per_meter": calculate_linear_weight(38.1, 4)},
    "R50.8x2": {"pa": 50.8, "t": 2, "weight_per_meter": calculate_linear_weight(50.8, 2)},
    "R50.8x4": {"pa": 50.8, "t": 4, "weight_per_meter": calculate_linear_weight(50.8, 4)},
    "R63.5x2": {"pa": 63.5, "t": 2, "weight_per_meter": calculate_linear_weight(63.5, 2)},
    "R63.5x4": {"pa": 63.5, "t": 4, "weight_per_meter": calculate_linear_weight(63.5, 4)},
    "R76.2x2": {"pa": 76.2, "t": 2, "weight_per_meter": calculate_linear_weight(76.2, 2)},
    "R76.2x4": {"pa": 76.2, "t": 4, "weight_per_meter": calculate_linear_weight(76.2, 4)},
    "R101.6x2": {"pa": 101.6, "t": 2, "weight_per_meter": calculate_linear_weight(101.6, 2)},
    "R101.6x4": {"pa": 101.6, "t": 4, "weight_per_meter": calculate_linear_weight(101.6, 4)},
}

ROUND_BARS_IMPERIAL = {
    # Imperial Round Bars (Diameter in inches)
    "R1/2x1/8": {"pa": round(0.5 * 25.4, 2), "t": round(1/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(0.5, 1/8)},
    "R1/2x1/4": {"pa": round(0.5 * 25.4, 2), "t": round(1/4 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(0.5, 1/4)},
    "R1x1/8": {"pa": round(1.0 * 25.4, 2), "t": round(1/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(1.0, 1/8)},
    "R1x1/4": {"pa": round(1.0 * 25.4, 2), "t": round(1/4 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(1.0, 1/4)},
    "R2x1/8": {"pa": round(2.0 * 25.4, 2), "t": round(1/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(2.0, 1/8)},
    "R2x1/4": {"pa": round(2.0 * 25.4, 2), "t": round(1/4 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(2.0, 1/4)},
    "R3x1/8": {"pa": round(3.0 * 25.4, 2), "t": round(1/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(3.0, 1/8)},
    "R3x1/4": {"pa": round(3.0 * 25.4, 2), "t": round(1/4 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(3.0, 1/4)},
    "R4x1/8": {"pa": round(4.0 * 25.4, 2), "t": round(1/8 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(4.0, 1/8)},
    "R4x1/4": {"pa": round(4.0 * 25.4, 2), "t": round(1/4 * 25.4, 2), "weight_per_meter": calculate_linear_weight_imperial(4.0, 1/4)},
}
