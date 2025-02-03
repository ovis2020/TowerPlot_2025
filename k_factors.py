from math import exp
from tables import table_2_4, table_2_5

class K_factors:
    def __init__(self, tower_data):
        """
        Initialize the K_factors class using the tower_data dictionary.

        Args:
            tower_data (dict): Dictionary containing all tower-related properties.
        """
        self.tower_data = tower_data

        # Extract relevant values from tower_data
        self.exposure_category = tower_data.get("exposure_category", "Exposure C")
        self.crest_height = tower_data.get("crest_height", 0)  # Default crest height
        self.ground_elevation = tower_data.get("ground_elevation", 0)  # Default ground elevation
        self.segment_list = tower_data.get("segment_list", [])  # Get the list of segments

    def calculateKe(self):
        """
        Calculate the ground elevation factor (Ke).

        Returns:
            float: Ground elevation factor (Ke).
        """
        try:
            # Validate ground elevation
            if not isinstance(self.ground_elevation, (int, float)) or self.ground_elevation < 0:
                raise ValueError(f"Invalid ground elevation: {self.ground_elevation}. Must be a non-negative number.")

            # Calculate Ke using the formula Ke = e^(-0.000119 * z_s)
            ke = exp(-0.000119 * self.ground_elevation)
            return round(ke, 4)
        except Exception as e:
            raise ValueError(f"Error calculating Ke: {str(e)}")

    def calculateKzt(self, z_height):
        """
        Calculate the topographic factor Kzt for a given segment.

        Args:
            z_height (float): Height above ground level in meters.

        Returns:
            float: Topographic factor (Kzt).
        """
        try:
            # Retrieve parameters from Table 2-4 and Table 2-5
            ke = table_2_4["Ke"][self.exposure_category]  # Terrain constant
            kt = table_2_5["Topographic Category"]["2"]["Kt"]  # Topographic constant
            f = table_2_5["Topographic Category"]["2"]["f"]  # Height attenuation factor

            # Validate inputs
            if not isinstance(z_height, (int, float)) or z_height <= 0:
                raise ValueError(f"Invalid z_height: {z_height}. Must be a positive number.")

            if not isinstance(self.crest_height, (int, float)) or self.crest_height <= 0:
                raise ValueError(f"Invalid crest_height: {self.crest_height}. Must be a positive number.")

            # Calculate Kh and Kzt
            Kh = exp(f * z_height / self.crest_height)
            kzt = (1 + (ke * kt / Kh)) ** 2

            return round(kzt, 4)
        except KeyError as e:
            raise ValueError(f"Invalid exposure category '{self.exposure_category}'. Ensure it exists in Table 2-4.") from e
        except Exception as e:
            raise ValueError(f"Error calculating Kzt: {str(e)}")

    def calculateKz(self, z_height):
        """
        Calculate the velocity pressure coefficient Kz for a given segment.

        Args:
            z_height (float): Height above ground level in meters.

        Returns:
            float: Velocity pressure coefficient (Kz).
        """
        try:
            # Retrieve parameters from Table 2-4
            zg = table_2_4["zg"][self.exposure_category]  # Boundary layer height in meters
            alpha = table_2_4["alpha"][self.exposure_category]  # Velocity profile exponent
            Kzmin = table_2_4["Kzmin"][self.exposure_category]  # Minimum Kz value

            # Validate inputs
            if not isinstance(z_height, (int, float)) or z_height <= 0:
                raise ValueError(f"Invalid z_height: {z_height}. Must be a positive number.")

            # Calculate Kz using the formula: Kz = 2.01 * (z / zg)^(2 / alpha)
            Kz = 2.01 * (z_height / zg) ** (2 / alpha)

            # Ensure Kz is within valid bounds
            return round(min(max(Kz, Kzmin), 2.01), 4)
        except KeyError as e:
            raise ValueError(f"Invalid exposure category '{self.exposure_category}'. Ensure it exists in Table 2-4.") from e
        except Exception as e:
            raise ValueError(f"Error calculating Kz: {str(e)}")

    def get_factors_summary(self):
        """
        Get a list of dictionaries containing Kz, Kzt, and Ke values for each segment.

        Returns:
            list: A list of dictionaries, each containing Kz, Kzt, and Ke for a segment.
        """
        ke = self.calculateKe()
        factors_summary = []

        for segment in self.segment_list:
            
            z_height = segment.get("z_height")  # not use any with deafult. 

            factors_summary.append({
                "segment_number": segment.get("segment_number", "N/A"),
                "Kz": self.calculateKz(z_height),
                "Kzt": self.calculateKzt(z_height),
                "Ke": ke
            })

        return factors_summary
