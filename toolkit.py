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
        angle = np.arcsin(height/diagonal_length) #in radians
        hc = (np.tan(angle))*(base_width*0.5)
        rc = rwidth*hc/height
        main_belt = base_width*0.5 - rc

        return  main_belt
