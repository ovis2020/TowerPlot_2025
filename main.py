import curses
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
    tower_base_width = float(display_menu(stdscr, "Enter the tower base width:", ["3000", "4000", "5000"]))
    top_width = float(display_menu(stdscr, "Enter the top width:", ["1000", "1500", "2000"]))
    height = float(display_menu(stdscr, "Enter the height:", ["20000", "30000", "40000"]))
    variable_segments = int(display_menu(stdscr, "Enter the number of variable segments:", ["1", "2", "3"]))
    constant_segments = int(display_menu(stdscr, "Enter the number of constant segments:", ["1", "2"]))
    cross_section = display_menu(stdscr, "Select cross-section type:", ["square", "triangular"])

    geometry = Geometry(tower_base_width, top_width, height, variable_segments, constant_segments, cross_section)
    segments = geometry.calculate_segments()

    panels = []
    for segment in segments:
        panel = Panel(panel_type=1, segment=segment, leg_width=0.05, diagonal_width=0.05, main_belt_width=0.05)
        panels.append(panel)

    stdscr.clear()
    stdscr.addstr(0, 0, "Panel Summary:", curses.A_BOLD | curses.A_UNDERLINE)
    for i, panel in enumerate(panels):
        stdscr.addstr(i + 2, 0, f"Panel {i + 1}: {panel.summary(cross_section, 0)}")
    stdscr.addstr(len(panels) + 3, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
