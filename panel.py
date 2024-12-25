from toolkit import Toolkit  # Import your Toolkit class

class Panel:
    def __init__(self, panel_type, segment, leg_width, diagonal_width, main_belt_width):
        self.panel_type = panel_type
        self.segment = segment
        self.leg_width = leg_width
        self.diagonal_width = diagonal_width
        self.main_belt_width = main_belt_width
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
        main_belt_length = self.toolkit.calculate_main_belt()
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
        return round(self.projected_area() / gross_area, 4)

    def cf(self):
        solidity_ratio = self.solidity_ratio()
        if self.segment['cross_section'] == "triangular":
            return round(3.4 * solidity_ratio**2 - 4.7 * solidity_ratio + 3.4, 4)
        elif self.segment['cross_section'] == "square":
            return round(4.0 * solidity_ratio**2 - 5.9 * solidity_ratio + 4.0, 4)

    def effective_projected_area(self, cross_section, wind_angle):
        cf = self.cf()
        af = self.projected_area()
        df = self.toolkit.wind_direction_factor(cross_section, wind_angle)
        return round(cf * df * af, 4)

    def summary(self, cross_section, wind_angle):
        return {
            "panel_type": self.panel_type,
            "leg_geometry": self.leg_geometry(),
            "diagonal_geometry": self.diagonal_geometry(),
            "main_belt_geometry": self.main_belt_geometry(),
            "projected_area": self.projected_area(),
            "solidity_ratio": self.solidity_ratio(),
            "cf": self.cf(),
            "effective_projected_area": self.effective_projected_area(cross_section, wind_angle)
        }
