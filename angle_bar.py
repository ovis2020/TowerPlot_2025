# Density of A36 Steel (kg/m³)
STEEL_DENSITY = 7850

def calculate_linear_weight(b1, b2, t):
    # Convert dimensions from mm to meters for area calculation
    b1_m = b1 / 1000
    b2_m = b2 / 1000
    t_m = t / 1000
    
    # Cross-sectional area (m²)
    area = (b1_m * t_m + b2_m * t_m - t_m**2)
    
    # Linear weight (kg/m)
    return round(area * STEEL_DENSITY, 4)

# Complete ANGLE_BARS dictionary with linear weight for each bar
ANGLE_BARS = {
    # 1-inch width bars (25 mm)
    "L25x25x2": {"b1": 25, "b2": 25, "t": 2, "weight_per_meter": calculate_linear_weight(25, 25, 2)},
    "L25x25x3": {"b1": 25, "b2": 25, "t": 3, "weight_per_meter": calculate_linear_weight(25, 25, 3)},
    "L25x25x4": {"b1": 25, "b2": 25, "t": 4, "weight_per_meter": calculate_linear_weight(25, 25, 4)},
    "L25x25x5": {"b1": 25, "b2": 25, "t": 5, "weight_per_meter": calculate_linear_weight(25, 25, 5)},
    "L25x25x6": {"b1": 25, "b2": 25, "t": 6, "weight_per_meter": calculate_linear_weight(25, 25, 6)},
    "L25x25x8": {"b1": 25, "b2": 25, "t": 8, "weight_per_meter": calculate_linear_weight(25, 25, 8)},
    "L25x25x10": {"b1": 25, "b2": 25, "t": 10, "weight_per_meter": calculate_linear_weight(25, 25, 10)},
    "L25x25x12": {"b1": 25, "b2": 25, "t": 12, "weight_per_meter": calculate_linear_weight(25, 25, 12)},

    # 2-inch width bars (50 mm)
    "L50x50x2": {"b1": 50, "b2": 50, "t": 2, "weight_per_meter": calculate_linear_weight(50, 50, 2)},
    "L50x50x3": {"b1": 50, "b2": 50, "t": 3, "weight_per_meter": calculate_linear_weight(50, 50, 3)},
    "L50x50x4": {"b1": 50, "b2": 50, "t": 4, "weight_per_meter": calculate_linear_weight(50, 50, 4)},
    "L50x50x5": {"b1": 50, "b2": 50, "t": 5, "weight_per_meter": calculate_linear_weight(50, 50, 5)},
    "L50x50x6": {"b1": 50, "b2": 50, "t": 6, "weight_per_meter": calculate_linear_weight(50, 50, 6)},
    "L50x50x8": {"b1": 50, "b2": 50, "t": 8, "weight_per_meter": calculate_linear_weight(50, 50, 8)},
    "L50x50x10": {"b1": 50, "b2": 50, "t": 10, "weight_per_meter": calculate_linear_weight(50, 50, 10)},
    "L50x50x12": {"b1": 50, "b2": 50, "t": 12, "weight_per_meter": calculate_linear_weight(50, 50, 12)},

    # 3-inch width bars (75 mm)
    "L75x75x2": {"b1": 75, "b2": 75, "t": 2, "weight_per_meter": calculate_linear_weight(75, 75, 2)},
    "L75x75x3": {"b1": 75, "b2": 75, "t": 3, "weight_per_meter": calculate_linear_weight(75, 75, 3)},
    "L75x75x4": {"b1": 75, "b2": 75, "t": 4, "weight_per_meter": calculate_linear_weight(75, 75, 4)},
    "L75x75x5": {"b1": 75, "b2": 75, "t": 5, "weight_per_meter": calculate_linear_weight(75, 75, 5)},
    "L75x75x6": {"b1": 75, "b2": 75, "t": 6, "weight_per_meter": calculate_linear_weight(75, 75, 6)},
    "L75x75x8": {"b1": 75, "b2": 75, "t": 8, "weight_per_meter": calculate_linear_weight(75, 75, 8)},
    "L75x75x10": {"b1": 75, "b2": 75, "t": 10, "weight_per_meter": calculate_linear_weight(75, 75, 10)},
    "L75x75x12": {"b1": 75, "b2": 75, "t": 12, "weight_per_meter": calculate_linear_weight(75, 75, 12)},

    # 4-inch width bars (100 mm)
    "L100x100x2": {"b1": 100, "b2": 100, "t": 2, "weight_per_meter": calculate_linear_weight(100, 100, 2)},
    "L100x100x3": {"b1": 100, "b2": 100, "t": 3, "weight_per_meter": calculate_linear_weight(100, 100, 3)},
    "L100x100x4": {"b1": 100, "b2": 100, "t": 4, "weight_per_meter": calculate_linear_weight(100, 100, 4)},
    "L100x100x5": {"b1": 100, "b2": 100, "t": 5, "weight_per_meter": calculate_linear_weight(100, 100, 5)},
    "L100x100x6": {"b1": 100, "b2": 100, "t": 6, "weight_per_meter": calculate_linear_weight(100, 100, 6)},
    "L100x100x8": {"b1": 100, "b2": 100, "t": 8, "weight_per_meter": calculate_linear_weight(100, 100, 8)},
    "L100x100x10": {"b1": 100, "b2": 100, "t": 10, "weight_per_meter": calculate_linear_weight(100, 100, 10)},
    "L100x100x12": {"b1": 100, "b2": 100, "t": 12, "weight_per_meter": calculate_linear_weight(100, 100, 12)},

    # 5-inch width bars (125 mm)
    "L125x125x2": {"b1": 125, "b2": 125, "t": 2, "weight_per_meter": calculate_linear_weight(125, 125, 2)},
    "L125x125x3": {"b1": 125, "b2": 125, "t": 3, "weight_per_meter": calculate_linear_weight(125, 125, 3)},
    "L125x125x4": {"b1": 125, "b2": 125, "t": 4, "weight_per_meter": calculate_linear_weight(125, 125, 4)},
    "L125x125x5": {"b1": 125, "b2": 125, "t": 5, "weight_per_meter": calculate_linear_weight(125, 125, 5)},
    "L125x125x6": {"b1": 125, "b2": 125, "t": 6, "weight_per_meter": calculate_linear_weight(125, 125, 6)},
    "L125x125x8": {"b1": 125, "b2": 125, "t": 8, "weight_per_meter": calculate_linear_weight(125, 125, 8)},
    "L125x125x10": {"b1": 125, "b2": 125, "t": 10, "weight_per_meter": calculate_linear_weight(125, 125, 10)},
    "L125x125x12": {"b1": 125, "b2": 125, "t": 12, "weight_per_meter": calculate_linear_weight(125, 125, 12)},

    # 6-inch width bars (150 mm)
    "L150x150x2": {"b1": 150, "b2": 150, "t": 2, "weight_per_meter": calculate_linear_weight(150, 150, 2)},
    "L150x150x3": {"b1": 150, "b2": 150, "t": 3, "weight_per_meter": calculate_linear_weight(150, 150, 3)},
    "L150x150x4": {"b1": 150, "b2": 150, "t": 4, "weight_per_meter": calculate_linear_weight(150, 150, 4)},
    "L150x150x5": {"b1": 150, "b2": 150, "t": 5, "weight_per_meter": calculate_linear_weight(150, 150, 5)},
    "L150x150x6": {"b1": 150, "b2": 150, "t": 6, "weight_per_meter": calculate_linear_weight(150, 150, 6)},
    "L150x150x8": {"b1": 150, "b2": 150, "t": 8, "weight_per_meter": calculate_linear_weight(150, 150, 8)},
    "L150x150x10": {"b1": 150, "b2": 150, "t": 10, "weight_per_meter": calculate_linear_weight(150, 150, 10)},
    "L150x150x12": {"b1": 150, "b2": 150, "t": 12, "weight_per_meter": calculate_linear_weight(150, 150, 12)},
}
