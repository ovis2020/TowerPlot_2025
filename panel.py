from toolkit import Toolkit  # Import your Toolkit class
from angle_bar import ANGLE_BARS_SI, ANGLE_BARS_IMPERIAL, ROUND_BARS_SI, ROUND_BARS_IMPERIAL

class Panel:

    def __init__(self, panel_type, segment, leg_bar, leg_type, diagonal_bar, diagonal_type, main_belt_bar, main_belt_type, cross_section, measurement_system):
        self.panel_type = panel_type
        self.segment = segment
        self.cross_section = cross_section
        self.leg_type = leg_type
        self.diagonal_type = diagonal_type
        self.main_belt_type = main_belt_type

        # Determine which bar dictionary to use based on bar type and measurement system
        if self.leg_type == "Angle Bar":
            bars = ANGLE_BARS_SI if measurement_system == "SI (Metric)" else ANGLE_BARS_IMPERIAL
        elif self.leg_type == "Round Bar":
            bars = ROUND_BARS_SI if measurement_system == "SI (Metric)" else ROUND_BARS_IMPERIAL
        else:
            raise ValueError("Invalid leg bar type. Must be 'Angle Bar' or 'Round Bar'.")

        # Extract dimensions from the dynamic bars dictionary
        try:
            self.leg_width = bars[leg_bar]['pa'] / 1000  # Convert mm to meters
        except KeyError as e:
            raise ValueError(f"Leg bar key {e} not found in the selected dictionary.") from e

        if self.diagonal_type == "Angle Bar":
            bars = ANGLE_BARS_SI if measurement_system == "SI (Metric)" else ANGLE_BARS_IMPERIAL
        elif self.diagonal_type == "Round Bar":
            bars = ROUND_BARS_SI if measurement_system == "SI (Metric)" else ROUND_BARS_IMPERIAL
        else:
            raise ValueError("Invalid diagonal bar type. Must be 'Angle Bar' or 'Round Bar'.")

        try:
            self.diagonal_width = bars[diagonal_bar]['pa'] / 1000  # Convert mm to meters
        except KeyError as e:
            raise ValueError(f"Diagonal bar key {e} not found in the selected dictionary.") from e

        if self.main_belt_type == "Angle Bar":
            bars = ANGLE_BARS_SI if measurement_system == "SI (Metric)" else ANGLE_BARS_IMPERIAL
        elif self.main_belt_type == "Round Bar":
            bars = ROUND_BARS_SI if measurement_system == "SI (Metric)" else ROUND_BARS_IMPERIAL
        else:
            raise ValueError("Invalid main belt bar type. Must be 'Angle Bar' or 'Round Bar'.")

        try:
            self.main_belt_width = bars[main_belt_bar]['pa'] / 1000  # Convert mm to meters
        except KeyError as e:
            raise ValueError(f"Main belt bar key {e} not found in the selected dictionary.") from e

        self.toolkit = Toolkit(segment)

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

        leg = self.leg_geometry()
        diagonal = self.diagonal_geometry()
        main_belt = self.main_belt_geometry()

        if self.leg_type == "Round Bar" or self.diagonal_type == "Round Bar" or self.main_belt_type == "Round Bar":
            # Projected area calculation for round bars
            round_projected_area = round(
                2 * (leg["leg_area"] if self.leg_type == "Round Bar" else 0) +
                2 * (diagonal["diagonal_area"] if self.diagonal_type == "Round Bar" else 0) +
                2 * (main_belt["main_belt_area"] if self.main_belt_type == "Round Bar" else 0),
                4
            )
        else:
            round_projected_area = 0

        if self.leg_type == "Angle Bar" or self.diagonal_type == "Angle Bar" or self.main_belt_type == "Angle Bar":
            # Projected area calculation for angle bars
            angle_projected_area = round(
                2 * (leg["leg_area"] if self.leg_type == "Angle Bar" else 0) +
                2 * (diagonal["diagonal_area"] if self.diagonal_type == "Angle Bar" else 0) +
                2 * (main_belt["main_belt_area"] if self.main_belt_type == "Angle Bar" else 0),
                4
            )
        else:
            angle_projected_area = 0

        return {
            "round_projected_area": round_projected_area,
            "angle_projected_area": angle_projected_area
        }


    def solidity_ratio(self):

        # Fetch projected areas
        projected_areas = self.projected_area()
        round_projected_area = projected_areas.get("round_projected_area", 0)
        angle_projected_area = projected_areas.get("angle_projected_area", 0)

        # Fetch gross area
        gross_area = self.segment.get("area", 0)
        
        # Validate gross area
        if gross_area <= 0:
            raise ValueError(f"Invalid or missing gross area in segment data for segment: {self.segment}")

        # Compute total projected area and solidity ratio
        total_projected_area = round_projected_area + angle_projected_area
        return round(total_projected_area / gross_area, 4)


    def cf(self):

        solidity_ratio = self.solidity_ratio()
        if self.cross_section.lower() == "triangular":
            return round(3.4 * solidity_ratio**2 - 4.7 * solidity_ratio + 3.4, 4)
        elif self.cross_section.lower() == "square":
            return round(4.0 * solidity_ratio**2 - 5.9 * solidity_ratio + 4.0, 4)
        else:
            raise ValueError("Invalid cross-section type.")

    def wind_direction_factor(self, cross_section, wind_angle):
        if cross_section.lower() == 'square':
            if wind_angle == 0:
                return 1.0
            elif wind_angle == 45:
                epsilon = self.solidity_ratio()
                return round(min(1 + 0.75 * epsilon, 1.2), 4)
        elif cross_section.lower() == 'triangular':
            if wind_angle == 0:
                return 1.0
            elif wind_angle == 60:
                return 0.80
            elif abs(wind_angle) == 90:
                return 0.85
        else:
            raise ValueError("Invalid cross-section type. Use 'square' or 'triangular'.")

    def effective_projected_area(self, cross_section):
        """
        Calculate the effective projected area for different wind angles based on cross-section type,
        using the summation of round and angle projected areas.

        Args:
            cross_section (str): The cross-section type ('square' or 'triangular').

        Returns:
            dict: Effective projected areas for each wind angle.
        """
        # Fetch force coefficient (cf) and projected areas
        cf = self.cf()
        projected_areas = self.projected_area()
        round_projected_area = projected_areas.get("round_projected_area", 0)
        angle_projected_area = projected_areas.get("angle_projected_area", 0)
        total_projected_area = round_projected_area + angle_projected_area  # Summatory of areas

        # Wind angles based on cross-section type
        wind_angles = [0, 45] if cross_section.lower() == 'square' else [0, 60, 90]
        epa_dict = {}

        # Calculate EPA for each wind angle
        for angle in wind_angles:
            df = self.wind_direction_factor(cross_section, angle)
            epa_dict[f'epa_{angle}'] = round(cf * df * total_projected_area, 4)

        return epa_dict


    def summary(self, cross_section):
        leg = self.leg_geometry()
        diagonal = self.diagonal_geometry()
        main_belt = self.main_belt_geometry()
        projected_area = self.projected_area()
        solidity_ratio = self.solidity_ratio()
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
            "effective_projected_area": epa
        }
