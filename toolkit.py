import numpy as np

class Toolkit:
    def __init__(self, segment):
        """
        Initialize the Toolkit object.

        Parameters:
        - segment (dict): Segment geometry containing base width, top width, height, and rwidth.
        """
        self.segment = segment

    def calculate_leg_length(self):
        """
        Calculate the length of the leg using Pythagoras theorem.

        Returns:
        - float: Length of the leg.
        """
        try:
            rwidth = self.segment['rwidth']
            height = self.segment['height']
        except KeyError as e:
            raise ValueError(f"Missing key in segment data: {e}")

        leg_length = round((rwidth**2 + height**2)**0.5, 4)
        return leg_length

    def calculate_diagonal_length(self):
        """
        Calculate the length of the diagonal using Pythagoras theorem.

        Returns:
        - float: Length of the diagonal.
        """
        try:
            base_width = self.segment['base_width']
            rwidth = self.segment['rwidth']
            height = self.segment['height']
        except KeyError as e:
            raise ValueError(f"Missing key in segment data: {e}")

        diagonal_length = round(((base_width - rwidth)**2 + height**2)**0.5, 4)
        return diagonal_length

    def calculate_main_belt(self):
        """
        Calculate the length of the belt at the joint of the two diagonals.

        Returns:
        - float: Length of the belt.
        """
        try:
            base_width = self.segment['base_width']
            rwidth = self.segment['rwidth']
            height = self.segment['height']
        except KeyError as e:
            raise ValueError(f"Missing key in segment data: {e}")

        diagonal_length = round(((base_width - rwidth)**2 + height**2)**0.5, 4)
        angle = np.arcsin(height / diagonal_length)  # in radians
        hc = (np.tan(angle)) * (base_width * 0.5)
        rc = rwidth * hc / height
        main_belt = base_width * 0.5 - rc

        return main_belt

    def wind_direction_factor(self, cross_section, wind_angle):
        """
        Calculate the wind direction factor based on cross-section type and wind angle.

        Args:
            cross_section (str): Cross-section type ('square' or 'triangular').
            wind_angle (float): Wind angle in degrees.

        Returns:
            float: Wind direction factor.
        """
        if cross_section.lower() == 'square':
            if wind_angle == 0:
                return 1.0
            elif wind_angle == 45:
                return 1.2
            else:
                raise ValueError("Unsupported wind angle for square cross-section.")
        elif cross_section.lower() == 'triangular':
            if wind_angle == 0:
                return 1.0
            elif wind_angle == 60:
                return 0.8
            elif abs(wind_angle) == 90:
                return 0.85
            else:
                raise ValueError("Unsupported wind angle for triangular cross-section.")
        else:
            raise ValueError("Invalid cross-section type. Use 'square' or 'triangular'.")
