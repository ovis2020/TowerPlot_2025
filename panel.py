import numpy as np
from toolkit import Toolkit  # Import the Toolkit class
from typing import Dict, Union, Optional
from angle_bar import ANGLE_BARS  # Import ANGLE_BARS module

VALID_CROSS_SECTIONS = {'square', 'triangular'}
DECIMAL_PLACES = 4

class Panel:
    """A class representing a tower panel.

    Attributes:
        panel_type (int): The type of panel (e.g., 1 or 2).
        segment (dict): Geometric properties of the tower segment.
        angle_bar_type (str): The type of angle bar used (e.g., 'L50x50x5').
        main_belt_width (float): Width of the main belt.
    """

    def __init__(self, panel_type: int, segment: Dict, 
                 angle_bar_type: str, main_belt_width: float) -> None:
        if not isinstance(panel_type, int) or panel_type not in [1, 2]:
            raise ValueError("panel_type must be 1 or 2")
        if angle_bar_type not in ANGLE_BARS:
            raise ValueError(f"Invalid angle bar type: {angle_bar_type}")
        if not isinstance(main_belt_width, (int, float)):
            raise ValueError("Main belt width must be numeric")
            
        self.panel_type = panel_type
        self.segment = segment
        self.angle_bar = ANGLE_BARS[angle_bar_type]
        self.main_belt_width = float(main_belt_width)
        self.toolkit = Toolkit(segment)

    @property
    def leg_geometry(self) -> Dict:
        """Calculate the leg geometry.

        Returns:
            dict: Contains leg length, projected width, and leg area.
        
        Raises:
            ValueError: If calculation fails.
        """
        try:
            leg_length = self.toolkit.calculate_leg_length()
            projected_width = self.angle_bar["b1"] + self.angle_bar["b2"] - self.angle_bar["t"]
            leg_area = round(leg_length * (projected_width / 1000), 4)  # Convert mm to meters
            return {
                "leg_length": leg_length,
                "projected_width": projected_width,
                "leg_area": leg_area,
            }
        except Exception as e:
            raise ValueError(f"Failed to calculate leg geometry: {str(e)}")

    @property
    def diagonal_geometry(self) -> Dict:
        """Calculate the diagonal geometry.

        Returns:
            dict: Contains diagonal length, projected width, and diagonal area.
        
        Raises:
            ValueError: If calculation fails.
        """
        try:
            diagonal_length = self.toolkit.calculate_diagonal_length()
            projected_width = self.angle_bar["b1"] + self.angle_bar["b2"] - self.angle_bar["t"]
            diagonal_area = round(diagonal_length * (projected_width / 1000), 4)  # Convert mm to meters
            return {
                "diagonal_length": diagonal_length,
                "projected_width": projected_width,
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
        main_belt_area = round(main_belt_length * (self.main_belt_width / 1000), 4)  # Convert mm to meters

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

    def effective_projected_area(self, cross_section: str) -> Dict[str, float]:
        """Calculate effective projected area based on cross section type."""
        if cross_section.lower() not in VALID_CROSS_SECTIONS:
            raise ValueError(f"Cross-section must be one of {VALID_CROSS_SECTIONS}")
        
        cf = self.cf()
        af = self.projected_area()
        
        if cross_section.lower() == "square":
            epa0 = round(cf * self.wind_direction_factor(cross_section, 0) * af, DECIMAL_PLACES)
            epa45 = round(cf * self.wind_direction_factor(cross_section, 45) * af, DECIMAL_PLACES)
            return {"epa0": epa0, "epa45": epa45}
        else:  # triangular
            epa0 = round(cf * self.wind_direction_factor(cross_section, 0) * af, DECIMAL_PLACES)
            epa60 = round(cf * self.wind_direction_factor(cross_section, 60) * af, DECIMAL_PLACES)
            epa90 = round(cf * self.wind_direction_factor(cross_section, 90) * af, DECIMAL_PLACES)
            return {"epa0": epa0, "epa60": epa60, "epa90": epa90}

    def summary(self, cross_section: str, wind_angle: Optional[float] = None) -> Dict[str, Union[str, dict, float]]:
        """
        Generate a summary of all panel properties.

        Args:
            cross_section: Cross-section type ('square' or 'triangular')
            wind_angle: Wind angle in degrees

        Returns:
            Dictionary containing panel properties summary
        """
        if cross_section.lower() not in VALID_CROSS_SECTIONS:
            raise ValueError(f"Cross-section must be one of {VALID_CROSS_SECTIONS}")
            
        return {
            "panel_type": self.panel_type,
            "leg_geometry": self.leg_geometry(),
            "diagonal_geometry": self.diagonal_geometry(),
            "main_belt_geometry": self.main_belt_geometry(),
            "projected_area": self.projected_area(),
            "solidity_ratio": self.solidity_ratio(),
            "cf": self.cf(),
            "effective_projected_area": self.effective_projected_area(cross_section),
        }
