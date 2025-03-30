# utils.py

def normalizeTowerDataKeys(data):
    return {
        "Tower_Base_Width": float(data["Tower Base Width"]),
        "Top_Width": float(data["Top Width"]),
        "Height": float(data["Height"]),
        "Variable_Segments": int(data["Variable Segments"]),
        "Constant_Segments": int(data["Constant Segments"]),
    }
