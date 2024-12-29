from toolkit import Toolkit  # Import your Toolkit class
from angle_bar import ANGLE_BARS_SI, ANGLE_BARS_IMPERIAL, ROUND_BARS_SI, ROUND_BARS_IMPERIAL

class Panel:
    
    def __init__(self, panel_type, segment, leg_bar, diagonal_bar, main_belt_bar, cross_section, measurement_system, bar_type):
        self.panel_type = panel_type
        self.segment = segment
        self.cross_section = cross_section
        self.bar_type = bar_type

        # Determine which bar dictionary to use based on bar type and measurement system
        if self.bar_type == "Angle Bar":
            bars = ANGLE_BARS_SI if measurement_system == "SI (Metric)" else ANGLE_BARS_IMPERIAL
        elif self.bar_type == "Round Bar":
            bars = ROUND_BARS_SI if measurement_system == "SI (Metric)" else ROUND_BARS_IMPERIAL
        else:
            raise ValueError("Invalid bar type. Must be 'Angle Bar' or 'Round Bar'.")

        # Extract dimensions from the dynamic bars dictionary
        try:
            self.leg_width = bars[leg_bar]['pa'] / 1000  # Convert mm to meters
            self.diagonal_width = bars[diagonal_bar]['pa'] / 1000  # Convert mm to meters
            self.main_belt_width = bars[main_belt_bar]['pa'] / 1000  # Convert mm to meters
        except KeyError as e:
            raise ValueError(f"Bar key {e} not found in the selected dictionary.") from e

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
        return round(
            2 * leg["leg_area"] + 2 * diagonal["diagonal_area"] + 2 * main_belt["main_belt_area"], 4
        )

    def solidity_ratio(self):
        gross_area = self.segment.get("area", 0)
        if gross_area <= 0:
            raise ValueError("Invalid or missing gross area in segment data.")
        projected_area = self.projected_area()
        return round(projected_area / gross_area, 4)

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
        cf = self.cf()
        af = self.projected_area()
        wind_angles = [0, 45] if cross_section.lower() == 'square' else [0, 60, 90]
        epa_dict = {}

        for angle in wind_angles:
            df = self.wind_direction_factor(cross_section, angle)
            epa_dict[f'epa_{angle}'] = round(cf * df * af, 4)

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
            "bar_type": self.bar_type,
            "leg_geometry": leg,
            "diagonal_geometry": diagonal,
            "main_belt_geometry": main_belt,
            "projected_area": projected_area,
            "solidity_ratio": solidity_ratio,
            "cf": cf_value,
            "effective_projected_area": epa
        }
