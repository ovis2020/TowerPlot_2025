import math
from toolkit import Toolkit
from angle_bar import ANGLE_BARS_SI, ANGLE_BARS_IMPERIAL, ROUND_BARS_SI, ROUND_BARS_IMPERIAL
from tables import table_2_6
from k_factors import K_factors  # Import the updated K_factors module


class Panel:

    def __init__(self, tower_data, panel_type, segment, leg_bar, leg_type, diagonal_bar, diagonal_type, main_belt_bar, main_belt_type, cross_section, measurement_system, exposure_category, z_height, ground_elevation):
        self.tower_data = tower_data
        self.panel_type = panel_type
        self.segment = segment
        self.cross_section = cross_section
        self.leg_type = leg_type
        self.diagonal_type = diagonal_type
        self.main_belt_type = main_belt_type
        self.exposure_category = exposure_category
        self.z_height = z_height
        self.ground_elevation = ground_elevation

        # Initialize K_factors instance for this panel
        self.k_factors = K_factors(
            exposure_category=exposure_category,
            z_height=z_height,
            crest_height=segment.get("crest_height", 10),  # Default crest height
            ground_elevation=ground_elevation
        )

        # Determine which bar dictionary to use based on bar type and measurement system
        if leg_type == "Angle Bar":
            bars = ANGLE_BARS_SI if measurement_system == "SI (Metric)" else ANGLE_BARS_IMPERIAL
        elif leg_type == "Round Bar":
            bars = ROUND_BARS_SI if measurement_system == "SI (Metric)" else ROUND_BARS_IMPERIAL
        else:
            raise ValueError("Invalid leg bar type. Must be 'Angle Bar' or 'Round Bar'.")

        try:
            self.leg_width = bars[leg_bar]['pa'] / 1000  # Convert mm to meters
        except KeyError as e:
            raise ValueError(f"Leg bar key {e} not found in the selected dictionary.") from e

        # Similar process for diagonal bars
        if diagonal_type == "Angle Bar":
            bars = ANGLE_BARS_SI if measurement_system == "SI (Metric)" else ANGLE_BARS_IMPERIAL
        elif diagonal_type == "Round Bar":
            bars = ROUND_BARS_SI if measurement_system == "SI (Metric)" else ROUND_BARS_IMPERIAL
        else:
            raise ValueError("Invalid diagonal bar type. Must be 'Angle Bar' or 'Round Bar'.")

        try:
            self.diagonal_width = bars[diagonal_bar]['pa'] / 1000  # Convert mm to meters
        except KeyError as e:
            raise ValueError(f"Diagonal bar key {e} not found in the selected dictionary.") from e

        # Main belt bars
        if main_belt_type == "Angle Bar":
            bars = ANGLE_BARS_SI if measurement_system == "SI (Metric)" else ANGLE_BARS_IMPERIAL
        elif main_belt_type == "Round Bar":
            bars = ROUND_BARS_SI if measurement_system == "SI (Metric)" else ROUND_BARS_IMPERIAL
        else:
            raise ValueError("Invalid main belt bar type. Must be 'Angle Bar' or 'Round Bar'.")

        try:
            self.main_belt_width = bars[main_belt_bar]['pa'] / 1000  # Convert mm to meters
        except KeyError as e:
            raise ValueError(f"Main belt bar key {e} not found in the selected dictionary.") from e

        self.toolkit = Toolkit(segment)

    # Use K_factors for Kz, Kzt, and Ke
    def calculateKz(self):
        """
        Calculate Kz using the K_factors module.
        """
        return self.k_factors.calculateKz()

    def calculateKzt(self):
        """
        Calculate Kzt using the K_factors module.
        """
        return self.k_factors.calculateKzt()

    def calculateKe(self):
        """
        Calculate Ke using the K_factors module.
        """
        return self.k_factors.calculateKe()

    ### Geometry Calculation Methods

    def leg_geometry(self):
        leg_length = self.toolkit.calculate_leg_length()
        return {
            "leg_length": leg_length,
            "leg_width": round(self.leg_width, 4),
            "leg_area": round(leg_length * self.leg_width, 4)
        }

    def diagonal_geometry(self):
        diagonal_length = self.toolkit.calculate_diagonal_length()
        return {
            "diagonal_length": diagonal_length,
            "diagonal_width": round(self.diagonal_width, 4),
            "diagonal_area": round(diagonal_length * self.diagonal_width, 4)
        }

    def main_belt_geometry(self):
        main_belt_length = self.toolkit.calculate_main_belt_length()
        return {
            "main_belt_length": main_belt_length,
            "main_belt_width": round(self.main_belt_width, 4),
            "main_belt_area": round(main_belt_length * self.main_belt_width, 4)
        }

    ### Summary

    def summary(self, cross_section):
        """
        Summarize panel properties and aerodynamic factors.
        """
        leg = self.leg_geometry()
        diagonal = self.diagonal_geometry()
        main_belt = self.main_belt_geometry()
        projected_area = self.projected_area()
        solidity_ratio = self.solidity_ratio()
        kz_value = self.calculateKz()
        kzt_value = self.calculateKzt()
        ke_value = self.calculateKe()
        cf_value = self.cf()
        epa = self.effective_projected_area(cross_section)

        return {
            "panel_type": self.panel_type,
            "leg_geometry": leg,
            "diagonal_geometry": diagonal,
            "main_belt_geometry": main_belt,
            "projected_area": projected_area,
            "solidity_ratio": solidity_ratio,
            "cf": cf_value,
            "kz": kz_value,
            "kzt": kzt_value,
            "ke": ke_value,
            "effective_projected_area": epa
        }
