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
    
    def projected_area(self):
        """
        Calculate the projected area for round and angle bars in the panel.

        Returns:
            dict: A dictionary containing the projected areas for round and angle bars.
        """
        # Calculate geometry for legs, diagonals, and main belts
        leg = self.leg_geometry()
        diagonal = self.diagonal_geometry()
        main_belt = self.main_belt_geometry()

        # Initialize projected areas
        round_projected_area = 0
        angle_projected_area = 0

        # Calculate projected area for round bars
        if self.leg_type == "Round Bar":
            round_projected_area += 2 * leg["leg_area"]
        if self.diagonal_type == "Round Bar":
            round_projected_area += 2 * diagonal["diagonal_area"]
        if self.main_belt_type == "Round Bar":
            round_projected_area += 2 * main_belt["main_belt_area"]

        # Calculate projected area for angle bars
        if self.leg_type == "Angle Bar":
            angle_projected_area += 2 * leg["leg_area"]
        if self.diagonal_type == "Angle Bar":
            angle_projected_area += 2 * diagonal["diagonal_area"]
        if self.main_belt_type == "Angle Bar":
            angle_projected_area += 2 * main_belt["main_belt_area"]

        # Return the results
        return {
            "round_projected_area": round(round_projected_area, 4),
            "angle_projected_area": round(angle_projected_area, 4),
        }
    
    def solidity_ratio(self):
        """
        Calculate the solidity ratio of the panel.

        Returns:
            float: Solidity ratio (total projected area / gross area).
        """
        projected_areas = self.projected_area()
        round_projected_area = projected_areas.get("round_projected_area", 0)
        angle_projected_area = projected_areas.get("angle_projected_area", 0)

        # Fetch gross area
        gross_area = self.segment.get("area", 0)  # `area` should be provided in the segment dictionary

        # Validate gross area
        if gross_area <= 0:
            raise ValueError(f"Invalid or missing gross area in segment data for segment: {self.segment}")

        # Compute total projected area and solidity ratio
        total_projected_area = round_projected_area + angle_projected_area
        return round(total_projected_area / gross_area, 4)
    
    def cf(self):
        """
        Calculate the force coefficient based on the solidity ratio.

        Returns:
            float: Force coefficient.
        """
        solidity_ratio = self.solidity_ratio()

        if self.cross_section.lower() == "triangular":
            return round(3.4 * solidity_ratio**2 - 4.7 * solidity_ratio + 3.4, 4)
        elif self.cross_section.lower() == "square":
            return round(4.0 * solidity_ratio**2 - 5.9 * solidity_ratio + 4.0, 4)
        else:
            raise ValueError("Invalid cross-section type. Use 'square' or 'triangular'.")

    def reduction_round_factor(self):
        """
        Calculate the reduction factor (Rr) for round bars based on the solidity ratio.

        Returns:
            float: Reduction factor (Rr).
        """
        # Calculate the solidity ratio
        solidity_ratio = self.solidity_ratio()

        # Calculate Rr using the formula provided
        rr = 0.57 - 0.14 * solidity_ratio + 0.86 * (solidity_ratio ** 2) - 0.24 * (solidity_ratio ** 3)

        # Ensure Rr does not exceed 1
        rr = min(rr, 1.0)

        return round(rr, 4)


    def effective_projected_area(self, cross_section):
        """
        Calculate the effective projected area (EPA) for different wind angles based on the cross-section type.

        Args:
            cross_section (str): The cross-section type ("square" or "triangular").

        Returns:
            dict: Effective projected areas for each wind angle.
        """
        # Normalize and validate the cross-section type
        cross_section = cross_section.lower().strip()
        valid_cross_sections = ["square", "triangular"]
        if cross_section not in valid_cross_sections:
            raise ValueError(
                f"Invalid cross-section type '{cross_section}'. Must be one of {valid_cross_sections}."
            )

        # Ensure cross_section exists in table_2_6
        if cross_section not in table_2_6:
            raise ValueError(f"Cross-section '{cross_section}' not found in table_2_6.")

        # Fetch force coefficient (Cf) and projected areas
        cf = self.cf()
        rr = self.reduction_round_factor()
        projected_areas = self.projected_area()
        round_projected_area = projected_areas.get("round_projected_area", 0)
        angle_projected_area = projected_areas.get("angle_projected_area", 0)
        total_projected_area = angle_projected_area + (round_projected_area * rr)  # Total projected area

        # Get wind angles from Table 2-6 for the given cross-section
        wind_angles = table_2_6[cross_section].keys()

        # Calculate EPA for each wind angle
        epa_dict = {}
        for angle_key in wind_angles:
            # Retrieve Df from Table 2-6
            df_value = table_2_6[cross_section][angle_key]["Df"]

            # Handle None or formula-based Df values
            if df_value is None:
                if cross_section == "square" and angle_key == "45":  # Dynamic calculation for square at 45°
                    epsilon = self.solidity_ratio()
                    df_value = min(1 + 0.75 * epsilon, 1.2)  # Calculate dynamically
                else:
                    raise ValueError(f"Df is undefined for {cross_section} at {angle_key}°.")

            # Calculate EPA
            epa = cf * df_value * total_projected_area
            epa_dict[f'epa_{angle_key}°'] = round(epa, 4)  # Add angle in ° as part of the key

        return epa_dict

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
