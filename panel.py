import numpy as np
from toolkit import Toolkit  # Import the Toolkit class
from typing import Dict

class Panel:
    """A class representing a tower panel.

    Attributes:
        panel_type (int): The type of panel (e.g., 1 or 2).
        segment (dict): Geometric properties of the tower segment.
        leg_width (float): Width of the leg.
        diagonal_width (float): Width of the diagonal braces.
        main_belt_width (float): Width of the main belt.
    """

    def __init__(self, panel_type: int, segment: Dict, 
                 leg_width: float, diagonal_width: float, 
                 main_belt_width: float) -> None:
        if not isinstance(panel_type, int) or panel_type not in [1, 2]:
            raise ValueError("panel_type must be 1 or 2")
        if not all(isinstance(x, (int, float)) for x in [leg_width, diagonal_width, main_belt_width]):
            raise ValueError("Width values must be numeric")
            
        self.panel_type = panel_type
        self.segment = segment
        self.leg_width = float(leg_width)
        self.diagonal_width = float(diagonal_width)
        self.main_belt_width = float(main_belt_width)
        self.toolkit = Toolkit(segment)

    @property
    def leg_geometry(self) -> Dict:
        """Calculate the leg geometry.

        Returns:
            dict: Contains leg length, leg width, and leg area.
        
        Raises:
            ValueError: If calculation fails.
        """
        try:
            leg_length = self.toolkit.calculate_leg_length()
            leg_area = round(leg_length * self.leg_width, 4)
            return {
                "leg_length": leg_length,
                "leg_width": round(self.leg_width, 4),
                "leg_area": leg_area,
            }
        except Exception as e:
            raise ValueError(f"Failed to calculate leg geometry: {str(e)}")

    @property
    def diagonal_geometry(self) -> Dict:
        """Calculate the diagonal geometry.

        Returns:
            dict: Contains diagonal length, diagonal width, and diagonal area.
        
        Raises:
            ValueError: If calculation fails.
        """
        try:
            diagonal_length = self.toolkit.calculate_diagonal_length()
            diagonal_area = round(diagonal_length * self.diagonal_width, 4)
            return {
                "diagonal_length": diagonal_length,
                "diagonal_width": round(self.diagonal_width, 4),
                "diagonal_area": diagonal_area,
            }
        except Exception as e:
            raise ValueError(f"Failed to calculate diagonal geometry: {str(e)}")

    def main_belt_geometry(self):
        """
        Calculate the main belt geometry.

        Returns:
            dict: Contains main belt length, main belt width, and main belt area.
        """
        main_belt_length = self.toolkit.calculate_main_belt()
        main_belt_area = round(main_belt_length * self.main_belt_width, 4)

        return {
            "main_belt_length": main_belt_length,
            "main_belt_width": round(self.main_belt_width, 4),
            "main_belt_area": main_belt_area,
        }

    def projected_area(self):
        """
        Calculate the total projected area of the panel.

        Returns:
            float: Total projected area.
        """
        leg = self.leg_geometry()
        diagonal = self.diagonal_geometry()
        main_belt = self.main_belt_geometry()

        return round(
            2 * leg["leg_area"]
            + 2 * diagonal["diagonal_area"]
            + 2 * main_belt["main_belt_area"],
            4,
        )

    def solidity_ratio(self):
        """
        Calculate the solidity ratio of the panel.

        Returns:
            float: Solidity ratio.
        """
        gross_area = self.segment.get("area", 0)
        if gross_area <= 0:
            raise ValueError("Invalid or missing gross area in segment data.")
        return round(self.projected_area() / gross_area, 4)

    def cf(self):
        """
        Calculate the force coefficient (cf) based on the solidity ratio.

        Returns:
            float: Force coefficient.
        """
        solidity_ratio = self.solidity_ratio()

        if self.segment["cross_section"] == "triangular":
            return round(3.4 * solidity_ratio**2 - 4.7 * solidity_ratio + 3.4, 4)
        elif self.segment["cross_section"] == "square":
            return round(4.0 * solidity_ratio**2 - 5.9 * solidity_ratio + 4.0, 4)
        else:
            raise ValueError("Invalid cross-section type.")

    def wind_direction_factor(self, cross_section, wind_angle):
        """
        Calculate the wind direction factor based on cross-section type and wind angle.

        Args:
            cross_section (str): Cross-section type ('square' or 'triangular').
            wind_angle (float): Wind angle in degrees.

        Returns:
            float: Wind direction factor.
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
            raise ValueError("Invalid cross-section type. Use 'square' or 'triangular'.")

    def effective_projected_area(self, cross_section, wind_angle=None):
        """
        Calculate the effective projected area.

        Args:
            cross_section (str): Cross-section type ('square' or 'triangular').
            wind_angle (float, optional): Wind angle in degrees.

        Returns:
            dict: Effective projected areas for relevant wind angles.
        """
        cf = self.cf()
        af = self.projected_area()

        if cross_section.lower() == "square":
            epa0 = round(cf * self.wind_direction_factor(cross_section, 0) * af, 4)
            epa45 = round(cf * self.wind_direction_factor(cross_section, 45) * af, 4)
            return {"epa0": epa0, "epa45": epa45}
        elif cross_section.lower() == "triangular":
            epa0 = round(cf * self.wind_direction_factor(cross_section, 0) * af, 4)
            epa60 = round(cf * self.wind_direction_factor(cross_section, 60) * af, 4)
            epa90 = round(cf * self.wind_direction_factor(cross_section, 90) * af, 4)
            return {"epa0": epa0, "epa60": epa60, "epa90": epa90}
        else:
            raise ValueError("Invalid cross-section type.")

    def summary(self, cross_section, wind_angle=None):
        """
        Generate a summary of all panel properties.

        Args:
            cross_section (str): Cross-section type ('square' or 'triangular').
            wind_angle (float, optional): Wind angle in degrees.

        Returns:
            dict: Summary of panel properties.
        """
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
            "effective_projected_area": epa,
        }
