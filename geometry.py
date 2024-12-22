import numpy as np
from panel import Panel  # Import the Panel class

class Geometry:
    def __init__(self, tower_base_width, top_width, height, variable_segments, constant_segments, cross_section):
        """
        Initialize the Geometry object.

        Parameters:
        - tower_base_width (float): Width of the tower base.
        - top_width (float): Width of the tower top.
        - height (float): Height of the tower.
        - variable_segments (int): Number of variable-width segments.
        - constant_segments (int): Number of constant-width segments.
        - cross_section (str): Type of cross-section ('square' or 'triangular').
        """
        self.tower_base_width = tower_base_width
        self.top_width = top_width
        self.height = height
        self.variable_segments = variable_segments
        self.constant_segments = constant_segments
        self.cross_section = cross_section

    def calculate_segments(self):
        """
        Calculate the segments of the tower.

        Returns:
        - list: A list of segment dictionaries.
        """
        segments = []
        total_segments = self.variable_segments + self.constant_segments
        segment_height = self.height / total_segments

        for i in range(self.variable_segments):
            base_width = self.tower_base_width - (i * (self.tower_base_width - self.top_width) / self.variable_segments)
            top_width = self.tower_base_width - ((i + 1) * (self.tower_base_width - self.top_width) / self.variable_segments)
            segment = {
                "base_width": base_width,
                "top_width": top_width,
                "height": segment_height,
                "area": (base_width + top_width) * segment_height / 2,
                "rwidth": (base_width - top_width) / 2,
                "cross_section": cross_section
            }
            segments.append(segment)

        for _ in range(self.constant_segments):
            segment = {
                "base_width": self.top_width,
                "top_width": self.top_width,
                "height": segment_height,
                "area": self.top_width * segment_height,
                "rwidth": 0,
                "cross_section": cross_section
            }
            segments.append(segment)
        return segments

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

        if (cross_section.lower() == "square"):
            epa0 = round(cf * self.wind_direction_factor(cross_section, 0) * af, 4)
            epa45 = round(cf * self.wind_direction_factor(cross_section, 45) * af, 4)
            return {"epa0": epa0, "epa45": epa45}
        elif (cross_section.lower() == "triangular"):
            epa0 = round(cf * self.wind_direction_factor(cross_section, 0) * af, 4)
            epa60 = round(cf * self.wind_direction_factor(cross_section, 60) * af, 4)
            epa90 = round(cf * self.wind_direction_factor(cross_section, 90) * af, 4)
            return {"epa0": epa0, "epa60": epa60, "epa90": epa90}
        else:
            raise ValueError("Invalid cross-section type. Use 'square' or 'triangular'.")

# Input variables
tower_base_width = float(input("Enter the tower base width: "))
top_width = float(input("Enter the top width of the tower: "))
height = float(input("Enter the height of the tower: "))
variable_segments = int(input("Enter the number of variable segments: "))
constant_segments = int(input("Enter the number of constant segments: "))
cross_section = input("Enter the cross-section type (square/triangular): ")

# Create a Geometry object
geometry = Geometry(tower_base_width, top_width, height, variable_segments, constant_segments, cross_section)

# Calculate segments
segments = geometry.calculate_segments()

# Create panels and calculate their properties
panels = []

# Determine wind angle based on cross-section
wind_angle = 45 if geometry.cross_section == 'square' else 60

for i, segment in enumerate(segments):  # Unpack index and segment correctly
    try:
        panel_type = int(input("Please enter the panel type (e.g., 1): "))
        
        if panel_type == 1:

            # Get user inputs for the widths
            leg_width = float(input("Please enter the leg width:... "))
            diagonal_width = float(input("Please enter the diagonal width:.. "))
            main_belt = 0

            # Ensure inputs are valid
            if leg_width <= 0 or diagonal_width <= 0:
                print("Width values must be positive numbers. Please try again.")
                continue
            
            # Create a Panel object with user inputs
            panel = Panel(panel_type=panel_type, segment=segment, 
              leg_width=leg_width, diagonal_width=diagonal_width, main_belt_width=main_belt)


            # Append to the panels list
            panels.append(panel)
        
        if panel_type == 2:

            # Get user inputs for the widths
            leg_width = float(input("Please enter the leg width:... "))
            diagonal_width = float(input("Please enter the diagonal width:... "))
            main_belt = float(input("Please enter the main belt width:... "))

            # Ensure inputs are valid
            if leg_width <= 0 or diagonal_width <= 0:
                print("Width values must be positive numbers. Please try again.")
                continue
            
            # Create a Panel object with user inputs
            panel = Panel(panel_type=panel_type, segment=segment, 
              leg_width=leg_width, diagonal_width=diagonal_width, main_belt_width=main_belt)

            # Append to the panels list
            panels.append(panel)

        else:
            print("Invalid panel type. Only type 1 and 2 are supported currently.")


    except ValueError as e:
        print(f"Invalid input: {e}. Please enter numeric values.")

# Print a summary of all panels
if not panels:
    print("No valid panels were created.")
else:
    print("\nPanel Summary:")
    for i, panel in enumerate(panels):
        summary = panel.summary(panel.segment['cross_section'], wind_angle=wind_angle)
        print(f"Panel {i + 1} Summary:")
        print(f"  Base Width: {panel.segment['base_width']} meters")
        print(f"  Top Width: {panel.segment['top_width']} meters")
        print(f"  Height: {panel.segment['height']} meters")
        for key, value in summary.items():
            print(f"  {key}: {value}")

        print(f"  cross_section: {geometry.cross_section}")
        print()
