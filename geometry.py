import curses
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
                "cross_section": self.cross_section
            }
            segments.append(segment)

        for _ in range(self.constant_segments):
            segment = {
                "base_width": self.top_width,
                "top_width": self.top_width,
                "height": segment_height,
                "area": self.top_width * segment_height,
                "rwidth": 0,
                "cross_section": self.cross_section
            }
            segments.append(segment)
        return segments


def display_menu(stdscr, title, options):
    """Display a menu and return the selected option."""
    curses.curs_set(0)
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title, curses.A_BOLD | curses.A_UNDERLINE)

        for idx, option in enumerate(options):
            x = 0
            y = idx + 2
            if idx == current_row:
                stdscr.addstr(y, x, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, f"  {option}")

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return options[current_row]

        stdscr.refresh()


def main(stdscr):
    # Input variables through curses menu
    tower_base_width = float(display_menu(stdscr, "Enter the tower base width:", ["10.0", "20.0", "30.0"]))
    top_width = float(display_menu(stdscr, "Enter the top width of the tower:", ["5.0", "10.0", "15.0"]))
    height = float(display_menu(stdscr, "Enter the height of the tower:", ["50.0", "60.0", "70.0"]))
    variable_segments = int(display_menu(stdscr, "Enter the number of variable segments:", ["1", "2", "3"]))
    constant_segments = int(display_menu(stdscr, "Enter the number of constant segments:", ["1", "2", "3"]))
    cross_section = display_menu(stdscr, "Select the cross-section type:", ["square", "triangular"])

    # Create Geometry object
    geometry = Geometry(tower_base_width, top_width, height, variable_segments, constant_segments, cross_section)

    # Calculate segments
    segments = geometry.calculate_segments()

    # Display segment summaries
    stdscr.clear()
    stdscr.addstr(0, 0, "Segment Details:", curses.A_BOLD | curses.A_UNDERLINE)

    for i, segment in enumerate(segments):
        stdscr.addstr(i + 2, 0, f"Segment {i + 1}: {segment}")

    stdscr.addstr(len(segments) + 3, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()


# Run curses application
curses.wrapper(main)
