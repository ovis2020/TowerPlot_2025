import curses
import json
from loadEngine.geometry import Geometry
from loadEngine.panel import Panel
from loadEngine.angle_bar import ANGLE_BARS_SI, ANGLE_BARS_IMPERIAL, ROUND_BARS_SI, ROUND_BARS_IMPERIAL

# Global variables for bar dictionaries
ANGLE_BARS = {}
ROUND_BARS = {}

def display_menu(stdscr, title, options):
    """
    Display a menu to the user with options to select.

    Args:
        stdscr: Curses standard screen object.
        title (str): Title of the menu.
        options (list): List of options to display.

    Returns:
        str: Selected option.
    """
    curses.curs_set(0)
    current_row = 0
    max_rows, max_cols = stdscr.getmaxyx()
    max_display_rows = max_rows - 4  # Reserve space for title and navigation instructions

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title, curses.A_BOLD | curses.A_UNDERLINE)

        # Determine the range of options to display
        start_idx = max(0, current_row - max_display_rows + 1)
        end_idx = min(len(options), start_idx + max_display_rows)

        for idx, option in enumerate(options[start_idx:end_idx]):
            x = 0
            y = idx + 2
            if idx + start_idx == current_row:
                stdscr.addstr(y, x, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, f"  {option}")

        # Navigation instructions
        stdscr.addstr(max_rows - 2, 0, "Use UP/DOWN arrows to navigate, ENTER to select.")

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return options[current_row]

        stdscr.refresh()

def select_bar_type(stdscr, title, bar_options):
    """
    Select a bar type from the given bar options.

    Args:
        stdscr: Curses standard screen object.
        title (str): Title of the menu.
        bar_options (dict): Dictionary of bar options.

    Returns:
        str: Selected bar key.
    """
    return display_menu(stdscr, title, list(bar_options.keys()))

def main(stdscr):
    global ANGLE_BARS, ROUND_BARS

    # Choose between SI and Imperial systems
    measurement_system = display_menu(
        stdscr,
        "Select the measurement system:",
        ["SI (Metric)", "Imperial"]
    )

    # Set ANGLE_BARS and ROUND_BARS based on the chosen system
    if measurement_system == "SI (Metric)":
        ANGLE_BARS = ANGLE_BARS_SI
        ROUND_BARS = ROUND_BARS_SI
    else:
        ANGLE_BARS = ANGLE_BARS_IMPERIAL
        ROUND_BARS = ROUND_BARS_IMPERIAL

    # Collect tower data inputs from the user
    tower_base_width = float(display_menu(stdscr, "Enter the tower base width in meters:", ["3", "4", "5", "6"]))
    top_width = float(display_menu(stdscr, "Enter the top width in meters:", ["1", "1.5", "2"]))
    height = float(display_menu(stdscr, "Enter the height in meters:", ["18", "24", "30", "36", "42", "48", "54", "60", "66", "72"]))
    variable_segments = int(display_menu(stdscr, "Enter the number of variable segments:", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]))
    constant_segments = int(display_menu(stdscr, "Enter the number of constant segments:", ["1", "2"]))
    cross_section = display_menu(stdscr, "Select cross-section type:", ["square", "triangular"])

    # Create Geometry object and tower data
    geometry = Geometry(tower_base_width, top_width, height, variable_segments, constant_segments, cross_section)
    tower_data = geometry.initiate_tower_data()

    # Create panels based on segments
    panels = []
    for section_number, segment in enumerate(tower_data["segment_list"], start=1):
        # Get bar type choice (Angle or Round)
        leg_type = display_menu(
            stdscr,
            f"Select leg bar type for Panel {section_number}:",
            ["Angle Bar", "Round Bar"]
        )
        diagonal_type = display_menu(
            stdscr,
            f"Select diagonal bar type for Panel {section_number}:",
            ["Angle Bar", "Round Bar"]
        )
        main_belt_type = display_menu(
            stdscr,
            f"Select main belt bar type for Panel {section_number}:",
            ["Angle Bar", "Round Bar"]
        )

        # Get bar choices based on type
        leg_bar = select_bar_type(stdscr, f"Select leg bar for Panel {section_number}:", ANGLE_BARS if leg_type == "Angle Bar" else ROUND_BARS)
        diagonal_bar = select_bar_type(stdscr, f"Select diagonal bar for Panel {section_number}:", ANGLE_BARS if diagonal_type == "Angle Bar" else ROUND_BARS)
        main_belt_bar = select_bar_type(stdscr, f"Select main belt bar for Panel {section_number}:", ANGLE_BARS if main_belt_type == "Angle Bar" else ROUND_BARS)

        panel = Panel(
            tower_data=tower_data,
            panel_type=1,
            segment=segment,
            leg_bar=leg_bar,
            leg_type=leg_type,
            diagonal_bar=diagonal_bar,
            diagonal_type=diagonal_type,
            main_belt_bar=main_belt_bar,
            main_belt_type=main_belt_type,
            cross_section=cross_section,
            measurement_system=measurement_system,
            exposure_category=tower_data["exposure_category"],
            z_height=segment["z_height"],
            ground_elevation=0.0  # Set default ground elevation
        )

        panel_summary = panel.summary(cross_section)
        panel_summary["section_number"] = section_number
        panels.append(panel_summary)

    # Save summaries to JSON
    with open("panel_summaries.json", "w") as f:
        json.dump(panels, f, indent=4)

    with open("tower_data.json", "w") as f:
        json.dump(tower_data, f, indent=4)

    stdscr.addstr(len(panels) + 2, 0, "Data saved successfully.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
