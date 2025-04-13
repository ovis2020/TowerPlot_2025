def normalizeTowerDataKeys(data):
    return {
        "tower_base_width": float(data["Tower Base Width"]),
        "top_width": float(data["Top Width"]),
        "height": float(data["Height"]),
        "variable_segments": int(data["Variable Segments"]),
        "constant_segments": int(data["Constant Segments"]),
        "cross_section": data.get("Cross Section", "square").lower()
    }
