from math import exp
from tables import table_2_4
from tables import table_2_5

class K_factors:
    def __init__(self, exposure_category, z_height, crest_height, ground_elevation):
        """
        Initialize the K_factors class.

        Args:
            exposure_category (str): Exposure category ("Exposure B", "Exposure C", or "Exposure D").
            z_height (float): Height above ground level in meters.
            crest_height (float): Height of the crest above surrounding terrain in meters.
            ground_elevation (float): Ground elevation above sea level in meters.
        """
        self.exposure_category = exposure_category
        self.z_height = z_height
        self.crest_height = crest_height
        self.ground_elevation = ground_elevation

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

    def calculateKzt(self):
        """
        Calculate the topographic factor Kzt.

        Returns:
            float: Topographic factor (Kzt).
        """
        try:
            # Retrieve parameters from Table 2-4 and Table 2-5
            ke = table_2_4["Ke"][self.exposure_category]  # Terrain constant
            kt = table_2_5["Topographic Category"]["2"]["Kt"]  # Topographic constant
            f = table_2_5["Topographic Category"]["2"]["f"]  # Height attenuation factor

            # Validate inputs
            if not isinstance(self.z_height, (int, float)) or self.z_height <= 0:
                raise ValueError(f"Invalid z_height: {self.z_height}. Must be a positive number.")
            if not isinstance(self.crest_height, (int, float)) or self.crest_height <= 0:
                raise ValueError(f"Invalid crest_height: {self.crest_height}. Must be a positive number.")

            # Calculate Kh and Kzt
            Kh = exp(f * self.z_height / self.crest_height)
            kzt = (1 + (ke * kt / Kh)) ** 2

            return round(kzt, 4)
        except KeyError as e:
            raise ValueError(f"Invalid exposure category '{self.exposure_category}'. Ensure it exists in Table 2-4.") from e
        except Exception as e:
            raise ValueError(f"Error calculating Kzt: {str(e)}")

    def calculateKz(self):
        """
        Calculate the velocity pressure coefficient Kz.

        Returns:
            float: Velocity pressure coefficient (Kz).
        """
        try:
            # Retrieve parameters from Table 2-4
            zg = table_2_4["zg"][self.exposure_category]  # Boundary layer height in meters
            alpha = table_2_4["alpha"][self.exposure_category]  # Velocity profile exponent
            Kzmin = table_2_4["Kzmin"][self.exposure_category]  # Minimum Kz value

            # Validate inputs
            if not isinstance(self.z_height, (int, float)) or self.z_height <= 0:
                raise ValueError(f"Invalid z_height: {self.z_height}. Must be a positive number.")

            # Calculate Kz using the formula: Kz = 2.01 * (z / zg)^(2 / alpha)
            Kz = 2.01 * (self.z_height / zg) ** (2 / alpha)

            # Ensure Kz is within valid bounds
            return round(min(max(Kz, Kzmin), 2.01), 4)
        except KeyError as e:
            raise ValueError(f"Invalid exposure category '{self.exposure_category}'. Ensure it exists in Table 2-4.") from e
        except Exception as e:
            raise ValueError(f"Error calculating Kz: {str(e)}")
