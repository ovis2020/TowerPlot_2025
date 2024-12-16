import numpy as np
from toolkit import Toolkit  # Import the Toolkit class

class Panel:
    def __init__(self, panel_type, segment, leg_width, diagonal_width, main_belt_width):
        self.panel_type = panel_type
        self.segment = segment
        self.leg_width = leg_width
        self.diagonal_width = diagonal_width
        self.main_belt_width = main_belt_width
        self.toolkit = Toolkit(segment)  # Initialize Toolkit with segment data

    def leg_geometry(self):
        leg_length = self.toolkit.calculate_leg_length()  # Use Toolkit to calculate leg length
        leg_area = round(leg_length * self.leg_width, 4)

        return {
            "leg_length": leg_length,
            "leg_width": round(self.leg_width, 4),
            "leg_area": leg_area
        }

    def diagonal_geometry(self):
        diagonal_length = self.toolkit.calculate_diagonal_length()
        diagonal_area = round(diagonal_length * self.diagonal_width, 4)

        return {
            "diagonal_length": diagonal_length,
            "diagonal_width": round(self.diagonal_width, 4),
            "diagonal_area": diagonal_area
        }
    
    def main_belt_geometry(self):
        main_belt_length = self.toolkit.calculate_main_belt()
        main_belt_area = round(main_belt_length * self.main_belt_width, 4)

        return {
            "main_belt": main_belt_length,
            "main_belt_width": round(self.main_belt_width, 4),
            "main_belt_area": main_belt_area
        }

    def projected_area(self):
        leg = self.leg_geometry()
        diagonal = self.diagonal_geometry()
        main_belt = self.main_belt_geometry()

        return round(2 * leg["leg_area"] + 2 * diagonal["diagonal_area"] + 2 * main_belt["main_belt_area"], 4)

    def solidity_ratio(self):
        gross_area = self.segment.get("area", 0)
        projected_area = self.projected_area()
        return round(projected_area / gross_area, 4)

    def cf(self):

        solidity_ratio = self.solidity_ratio()

        if self.segment['cross_section'] == "triangular":
            cf = round(3.4 * solidity_ratio**2 - 4.7 * solidity_ratio + 3.4, 4)
        else:
            cf = round(4.0 * solidity_ratio**2 - 5.9 * solidity_ratio +4, 4)
            
        return cf

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

    def effective_projected_area(self, cross_section, wind_angle):
        cf = self.cf()
        df = self.wind_direction_factor(cross_section, wind_angle)
        af = self.projected_area()

        return round(cf * df * af, 4)

    def summary(self, cross_section, wind_angle):
        leg = self.leg_geometry()
        diagonal = self.diagonal_geometry()
        main_belt = self.main_belt_geometry()
        projected_area = self.projected_area()
        solidity_ratio = self.solidity_ratio()
        cf_value = self.cf()
        epa = self.effective_projected_area(cross_section, wind_angle)

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
