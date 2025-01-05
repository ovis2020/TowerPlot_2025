import math
from toolkit import Toolkit
from angle_bar import ANGLE_BARS_SI, ANGLE_BARS_IMPERIAL, ROUND_BARS_SI, ROUND_BARS_IMPERIAL
from tables import table_2_4


class Panel:

    def __init__(self, panel_type, segment, leg_bar, leg_type, diagonal_bar, diagonal_type, main_belt_bar, main_belt_type, cross_section, measurement_system, exposure_category, z_height):
        self.panel_type = panel_type
        self.segment = segment
        self.cross_section = cross_section
        self.leg_type = leg_type
        self.diagonal_type = diagonal_type
        self.main_belt_type = main_belt_type
        self.exposure_category = exposure_category
        self.z_height = z_height

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

    # Method to calculate the effective projected area of the panel

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


    ### Solidity Ratio

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

    ### Force Coefficient (Cf)

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

    def calculateKz(self, exposure_category, z_height):
        """
        Calculate the velocity pressure coefficient Kz.

        Args:
            exposure_category (str): Exposure category ("Exposure B", "Exposure C", or "Exposure D").
            z_height (float): Height above ground level in meters.

        Returns:
            float: Velocity pressure coefficient (Kz).
        """
        try:
            # Retrieve parameters from Table 2-4
            zg = table_2_4["zg"][exposure_category]  # Boundary layer height in meters
            alpha = table_2_4["alpha"][exposure_category]  # Exponent for velocity profile
            Kzmin = table_2_4["Kzmin"][exposure_category]  # Minimum Kz value

            # Validate z_height
            if not isinstance(z_height, (int, float)) or z_height <= 0:
                raise ValueError(f"Invalid z_height: {z_height}. Must be a positive number.")

            # Calculate Kz using the formula: Kz = 2.01 * (z / zg)^(2 / alpha)
            Kz = 2.01 * (z_height / zg) ** (2 / alpha)

            # Ensure Kz is not below the minimum or above the maximum allowed
            return round(min(max(Kz, Kzmin), 2.01), 4)
        except KeyError as e:
            raise ValueError(f"Invalid exposure category '{exposure_category}'. Valid options are: {list(table_2_4['zg'].keys())}") from e
        except Exception as e:
            raise ValueError(f"Error calculating Kz: {str(e)}")

    def wind_direction_factor(self, cross_section, wind_angle):
        """
        Calculate the wind direction factor (Df) based on cross-section type and wind angle.

        Args:
            cross_section (str): The cross-section type ("square" or "triangular").
            wind_angle (int): The wind angle in degrees.

        Returns:
            float: Wind direction factor (Df).
        """
        if cross_section.lower() == "square":
            if wind_angle == 0:
                return 1.0
            elif wind_angle == 45:
                epsilon = self.solidity_ratio()
                return round(min(1 + 0.75 * epsilon, 1.2), 4)
        elif cross_section.lower() == "triangular":
            if wind_angle == 0:
                return 1.0
            elif wind_angle == 60:
                return 0.80
            elif abs(wind_angle) == 90:
                return 0.85
        else:
            raise ValueError("Invalid cross-section type. Must be 'square' or 'triangular'.")

    def effective_projected_area(self, cross_section):
        """
        Calculate the effective projected area (EPA) for different wind angles based on the cross-section type.

        Args:
            cross_section (str): The cross-section type ("square" or "triangular").

        Returns:
            dict: Effective projected areas for each wind angle.
        """
        # Fetch force coefficient (Cf) and projected areas
        cf = self.cf()
        projected_areas = self.projected_area()
        round_projected_area = projected_areas.get("round_projected_area", 0)
        angle_projected_area = projected_areas.get("angle_projected_area", 0)
        total_projected_area = round_projected_area + angle_projected_area  # Total projected area

        # Define wind angles based on cross-section type
        if cross_section.lower() == "square":
            wind_angles = [0, 45]
        elif cross_section.lower() == "triangular":
            wind_angles = [0, 60, 90]
        else:
            raise ValueError("Invalid cross-section type. Must be 'square' or 'triangular'.")

        # Calculate EPA for each wind angle
        epa_dict = {}
        for angle in wind_angles:
            wind_direction_factor = self.wind_direction_factor(cross_section, angle)
            epa_dict[f'epa_{angle}'] = round(cf * wind_direction_factor * total_projected_area, 4)

        return epa_dict
    
    ### Summary

    def summary(self, cross_section):
        leg = self.leg_geometry()
        diagonal = self.diagonal_geometry()
        main_belt = self.main_belt_geometry()
        projected_area = self.projected_area()
        solidity_ratio = self.solidity_ratio()
        kz_value = self.calculateKz(self.exposure_category, self.z_height)
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
            "effective_projected_area": epa
        }
