table_2_3 = {
    "Risk Categories": {
        "I": "Low hazard to human life in the event of failure.",
        "II": "Structures not included in Categories I, III, or IV.",
        "III": "Substantial hazard to human life in the event of failure.",
        "IV": "Essential facilities and critical infrastructure."
    },
    "Importance Factors (I)": {
        "Wind Loads": {
            "I": 0.87,
            "II": 1.0,
            "III": 1.15,
            "IV": 1.15
        },
        "Ice Loads": {
            "I": 0.80,
            "II": 1.0,
            "III": 1.25,
            "IV": 1.25
        },
        "Seismic Loads": {
            "I": 1.0,
            "II": 1.0,
            "III": 1.25,
            "IV": 1.5
        }
    },
    "Notes": [
        "Risk Category definitions are from Section 2.2 of the standard.",
        "Importance factors are used to adjust loads for structures based on their risk category.",
        "Ensure consistency between risk categorization and site-specific conditions."
    ]
}

table_2_4 = {
    "zg": {
        "Exposure B": 366,  # in meters
        "Exposure C": 274,
        "Exposure D": 213
    },
    "alpha": {
        "Exposure B": 7.0,
        "Exposure C": 9.5,
        "Exposure D": 11.5
    },
    "Kzmin": {
        "Exposure B": 0.7,
        "Exposure C": 0.85,
        "Exposure D": 1.03
    },
    "Ke": {
        "Exposure B": 0.9,
        "Exposure C": 1.00,
        "Exposure D": 1.10
    },
    
    "Notes": [
        "zg: Nominal height of atmospheric boundary layer in feet.",
        "alpha: Exponent of the velocity pressure profile equation.",
        "Kzmin: Minimum value of the velocity pressure coefficient, Kz."
    ]
}

