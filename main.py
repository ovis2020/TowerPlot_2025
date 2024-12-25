import curses
import json
from geometry import Geometry
from panel import Panel


def display_menu(stdscr, title, options):
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
    # Get user inputs using the curses menu
    tower_base_width = float(display_menu(stdscr, "Enter the tower base width in meters:", ["3", "4", "5", "6"]))
    top_width = float(display_menu(stdscr, "Enter the top width in meters:", ["1", "1.5", "2"]))
    height = float(display_menu(stdscr, "Enter the height in meters:", ["18", "24", "30", "36", "42", "48", "54", "60", "66", "72"]))
    variable_segments = int(display_menu(stdscr, "Enter the number of variable segments:", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]))
    constant_segments = int(display_menu(stdscr, "Enter the number of constant segments:", ["1", "2"]))
    cross_section = display_menu(stdscr, "Select cross-section type:", ["square", "triangular"])

    # Create a Geometry object and calculate segments
    geometry = Geometry(tower_base_width, top_width, height, variable_segments, constant_segments, cross_section)
    segments = geometry.calculate_segments()

    # Create panels based on segments
    panels = []
    for section_number, segment in enumerate(segments, start=1):
        panel = Panel(panel_type=1, segment=segment, leg_width=0.05, diagonal_width=0.05, main_belt_width=0.05)
        panel_summary = panel.summary(cross_section, 0)  # Assuming wind_angle is 0
        panel_summary["section_number"] = section_number  # Add section number to the summary
        panels.append(panel_summary)

    # Save summaries to a JSON file
    output_file = "panel_summaries.json"
    with open(output_file, "w") as f:
        json.dump(panels, f, indent=4)

    # Display completion message
    stdscr.clear()
    stdscr.addstr(0, 0, "Panel Summary:", curses.A_BOLD | curses.A_UNDERLINE)
    for i, panel in enumerate(panels):
        stdscr.addstr(i + 2, 0, f"Panel {panel['section_number']}: {panel}")
    stdscr.addstr(len(panels) + 3, 0, f"Summaries saved to '{output_file}'.")
    stdscr.addstr(len(panels) + 4, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
