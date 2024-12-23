STEEL_DENSITY = 7850  # kg/m³

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

# Complete ANGLE_BARS dictionary with linear weight for each bar
ANGLE_BARS = {
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
