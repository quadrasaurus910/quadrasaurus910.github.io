# terminal_colors.py
# Demonstration of printing text with foreground and background colors
# using standard ANSI escape codes.

# --- ANSI Escape Codes Definitions ---
# The format for an ANSI code is: \033[<modifier>;<foreground>;<background>m
# Where \033 is the escape character, and 'm' marks the end of the sequence.

# Reset code (important to prevent colors from leaking into subsequent prints)
RESET = '\033[0m'

# --- Foreground Colors ---
FG_BLACK   = '\033[30m'
FG_RED     = '\033[31m'
FG_GREEN   = '\033[32m'
FG_YELLOW  = '\033[33m'
FG_BLUE    = '\033[34m'
FG_MAGENTA = '\033[35m'
FG_CYAN    = '\033[36m'
FG_WHITE   = '\033[37m'
# You can also use bright colors (e.g., 90-97)

# --- Background Colors ---
BG_BLACK   = '\033[40m'
BG_RED     = '\033[41m'
BG_GREEN   = '\033[42m'
BG_YELLOW  = '\033[43m'
BG_BLUE    = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN    = '\033[46m'
BG_WHITE   = '\033[47m'
# You can also use bright background colors (e.g., 100-107)

# --- Text Modifiers ---
BOLD = '\033[1m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'

def print_with_color(text, fg_color=FG_WHITE, bg_color=BG_BLACK, style=""):
    """
    Prints the given text using the specified ANSI foreground, background, and style codes.
    It automatically adds the RESET code at the end.
    """
    print(f"{style}{fg_color}{bg_color}{text}{RESET}")

def main():
    print("--- ANSI Terminal Color Demonstration ---")
    print("If your terminal supports ANSI codes, the text below will be colored.")
    print("If not, you will see strange characters like '[0m', or no change at all.")
    print("-" * 40)

    # Examples using different background colors
    print_with_color(" Standard Black Background ", bg_color=BG_BLACK, fg_color=FG_WHITE)
    print_with_color(" Important Warning (Red Background) ", bg_color=BG_RED, fg_color=FG_WHITE, style=BOLD)
    print_with_color(" Success Message (Green Background) ", bg_color=BG_GREEN, fg_color=FG_BLACK)
    print_with_color(" Information (Blue Background) ", bg_color=BG_BLUE, fg_color=FG_WHITE)
    
    # Example mixing background, foreground, and style
    code = BG_YELLOW + FG_RED + BOLD
    print(f"{code} ALERT: Check Configuration! {RESET}")

    # Example of a white background with black text
    print_with_color(" White Background Text ", bg_color=BG_WHITE, fg_color=FG_BLACK, style=UNDERLINE)

    print("-" * 40)
    print("Remember to always include the RESET code! The Python 'f-string' method makes it easy.")

if __name__ == "__main__":
    main()
