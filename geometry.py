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
        segments = []
        total_segments = self.variable_segments + self.constant_segments
        segment_height = self.height / total_segments

        for i in range(self.variable_segments):
            base_width = self.tower_base_width - (i * (self.tower_base_width - self.top_width) / self.variable_segments)
            top_width = self.tower_base_width - ((i + 1) * (self.tower_base_width - self.top_width) / self.variable_segments)
            segments.append({
                "base_width": base_width,
                "top_width": top_width,
                "height": segment_height,
                "area": (base_width + top_width) * segment_height / 2,
                "rwidth": (base_width - top_width) / 2,
                "cross_section": self.cross_section
            })

        for _ in range(self.constant_segments):
            segments.append({
                "base_width": self.top_width,
                "top_width": self.top_width,
                "height": segment_height,
                "area": self.top_width * segment_height,
                "rwidth": 0,
                "cross_section": self.cross_section
            })

        return segments
