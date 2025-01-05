class Geometry:
    
    VALID_CROSS_SECTIONS = {'square', 'triangular'}

    def __init__(self, tower_base_width, top_width, height, variable_segments, constant_segments, cross_section):
        self.tower_base_width = tower_base_width
        self.top_width = top_width
        self.height = height
        self.variable_segments = variable_segments
        self.constant_segments = constant_segments
        self.cross_section = cross_section.lower()

        self._validate_inputs()

    def _validate_inputs(self):
        if self.tower_base_width <= 0 or self.top_width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive numbers")
        if not isinstance(self.variable_segments, int) or not isinstance(self.constant_segments, int):
            raise ValueError("Segment counts must be integers")
        if self.variable_segments < 0 or self.constant_segments < 0:
            raise ValueError("Segment counts must be non-negative")
        if self.cross_section not in self.VALID_CROSS_SECTIONS:
            raise ValueError(f"Cross section must be one of {self.VALID_CROSS_SECTIONS}")
        if self.tower_base_width <= self.top_width:
            raise ValueError("Base width must be greater than top width")

    def calculate_segments(self):
        """
        Calculate the segments of the tower.

        Returns:
        - list: A list of segment dictionaries.
        """
        segments = []
        total_segments = self.variable_segments + self.constant_segments
        segment_height = self.height / total_segments

        # Calculate variable-width segments
        for i in range(self.variable_segments):
            base_width = self.tower_base_width - (i * (self.tower_base_width - self.top_width) / self.variable_segments)
            top_width = self.tower_base_width - ((i + 1) * (self.tower_base_width - self.top_width) / self.variable_segments)
            segment = {
                "base_width": base_width,
                "top_width": top_width,
                "height": segment_height,
                "area": (base_width + top_width) * segment_height / 2,  # Trapezoid area formula
                "rwidth": (base_width - top_width) / 2,  # Reduction in width per side
                "cross_section": self.cross_section,
                "z_height": i * segment_height + segment_height / 2  # Midpoint height of the segment
            }
            segments.append(segment)

        # Calculate constant-width segments
        for i in range(self.constant_segments):
            segment = {
                "base_width": self.top_width,
                "top_width": self.top_width,
                "height": segment_height,
                "area": self.top_width * segment_height,  # Rectangle area formula
                "rwidth": 0,  # No reduction in width
                "cross_section": self.cross_section,
                "z_height": (self.variable_segments + i) * segment_height + segment_height / 2  # Midpoint height
            }
            segments.append(segment)

        return segments


    def initiate_tower_data(self):
        
        tower_data = {
            "Tower Base Width": self.tower_base_width,
            "Top Width": self.top_width,
            "Height": self.height,
            "Variable Segments": self.variable_segments,
            "Constant Segments": self.constant_segments,
            "Cross Section": self.cross_section,
            "importance_factor": 1.0,
            "exposure_category": "Exposure C",
            "basic_wind_speed_service": 33.33,
            "basic_wind_speed_ultimate": 44.44,
        }

        return tower_data
        