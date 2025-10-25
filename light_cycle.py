import requests
from datetime import datetime, timedelta, timezone

# --- Configuration for Southport, NC (Currently EDT = UTC-4) ---
API_URL = "https://api.sunrise-sunset.org/json"
LATITUDE = 33.92
LONGITUDE = -78.02
UTC_OFFSET = -4 
TIMEZONE_LABEL = "EDT (UTC-4)"

# --- ANSI Escape Codes Definitions ---
# \033[...m is the escape sequence for terminal formatting
RESET = '\033[0m'
BOLD = '\033[1m'

# Foreground Colors (Text Color)
FG_BLACK   = '\033[30m'
FG_WHITE   = '\033[97m' # Bright white for better contrast
FG_YELLOW  = '\033[93m'
FG_CYAN    = '\033[96m'
FG_MAGENTA = '\033[95m'

# Background Colors
BG_BLACK   = '\033[40m'
BG_BLUE    = '\033[44m'    # Deep Night/Nautical
BG_MAGENTA = '\033[45m'  # Astro Twilight
BG_CYAN    = '\033[46m'    # Civil Twilight
BG_YELLOW  = '\033[103m' # Bright Yellow/White for Daylight

def convert_seconds_to_hms(total_seconds):
    """Converts a total number of seconds into Hours, Minutes, and Seconds string."""
    if total_seconds is None:
        return "N/A"
        
    total_seconds = int(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}h {minutes:02}m {seconds:02}s"

def get_current_phase_color(current_time_only, local_times):
    """
    Determines the current phase of the day based on the current local time 
    and returns the corresponding color and status.
    """
    
    astro_b = local_times.get('astronomical_twilight_begin')
    civil_b = local_times.get('civil_twilight_begin')
    sunrise = local_times.get('sunrise')
    sunset = local_times.get('sunset')
    civil_e = local_times.get('civil_twilight_end')
    astro_e = local_times.get('astronomical_twilight_end')

    # Note on time comparison: Since the API returns times for a single day,
    # the comparison needs to handle the cycle wrapping midnight (astro_e -> astro_b).

    color_config = {"bg": BG_BLACK, "fg": FG_WHITE, "status": "Error/Unknown Phase"}

    # 1. Daylight (Sunrise to Sunset)
    if sunrise and sunset and sunrise <= current_time_only < sunset:
        color_config = {"bg": BG_YELLOW, "fg": FG_BLACK, "status": "☀️ FULL DAYLIGHT"}
    
    # 2. Dusk Twilights (Sunset to Astronomical End)
    elif sunset and current_time_only >= sunset:
        if civil_e and current_time_only < civil_e:
             # Civil Twilight End (Sunset to Civil End)
            color_config = {"bg": BG_CYAN, "fg": FG_BLACK, "status": "🏙️ Civil Twilight (Dusk)"}
        elif astro_e and current_time_only < astro_e:
            # Nautical & Astronomical Twilight (Civil End to Astro End)
            color_config = {"bg": BG_MAGENTA, "fg": FG_WHITE, "status": "🔭 Twilight"}
        else:
            # Night (After Astro End)
            color_config = {"bg": BG_BLACK, "fg": FG_CYAN, "status": "🌑 NIGHT TIME"}

    # 3. Dawn Twilights (Astronomical Begin to Sunrise)
    elif sunrise and current_time_only < sunrise:
        if civil_b and current_time_only >= civil_b:
            # Civil Twilight Begin (Civil Begin to Sunrise)
            color_config = {"bg": BG_CYAN, "fg": FG_BLACK, "status": "🏙️ Civil Twilight (Dawn)"}
        elif astro_b and current_time_only >= astro_b:
            # Astronomical Twilight (Astro Begin to Civil Begin)
            color_config = {"bg": BG_MAGENTA, "fg": FG_WHITE, "status": "🔭 Twilight"}
        else:
            # Night (Before Astro Begin)
            color_config = {"bg": BG_BLACK, "fg": FG_CYAN, "status": "🌑 NIGHT TIME"}

    return color_config

def generate_day_graphic():
    """
    Fetches sun data and generates the colored terminal graphic.
    """
    print(f"\n--- Day Cycle Graphic for Southport, NC ({TIMEZONE_LABEL}) ---")

    # 1. Prepare and make API request
    params = {"lat": LATITUDE, "lng": LONGITUDE, "formatted": 0}
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"\nAPI Connection Error: {e}")
        return

    if data.get("status") != "OK":
        print(f"\nAPI Data Error: {data.get('status')}")
        return

    results = data["results"]
    offset_delta = timedelta(hours=UTC_OFFSET)
    local_times = {}

    # 2. Process all UTC times into local time.
    time_points = {
        "sunrise": "🌅 Rise", 
        "sunset": "🌇 Set",
        "solar_noon": "☀️ Noon",
        "civil_twilight_begin": "Civil Beg",
        "civil_twilight_end": "Civil End",
        "astronomical_twilight_begin": "Astro Beg",
        "astronomical_twilight_end": "Astro End"
    }
    
    # Store local time objects and formatted strings
    local_time_strings = {}
    for key, label in time_points.items():
        time_str = results.get(key)
        if time_str:
            try:
                utc_dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                local_dt = utc_dt + offset_delta
                local_times[key] = local_dt.time() # Store time object for comparison
                local_time_strings[key] = local_dt.strftime('%I:%M %p') # Store formatted string for display
            except Exception:
                local_times[key] = None
                local_time_strings[key] = "N/A"

    # 3. Determine current time and phase
    # Get current UTC time and convert it to local time for the current date
    current_utc_dt = datetime.now(timezone.utc)
    current_local_dt = current_utc_dt + offset_delta
    current_time_only = current_local_dt.time()
    
    color_data = get_current_phase_color(current_time_only, local_times)
    
    # 4. Generate the Terminal Graphic (2 rows of color)
    terminal_width = 75 # Fixed width for the graphic
    
    # Header: Shows current status
    header_text = f" CURRENT PHASE: {color_data['status']} "
    padding_length = (terminal_width - len(header_text)) // 2
    header_bar = color_data['bg'] + color_data['fg'] + ( " " * padding_length) + header_text + (" " * (terminal_width - len(header_text) - padding_length)) + RESET
    
    # Current Time Row
    time_text = f" Local Time: {current_local_dt.strftime('%A, %B %d, %Y - %I:%M:%S %p')} "
    padding_length = (terminal_width - len(time_text)) // 2
    time_bar = color_data['bg'] + color_data['fg'] + ( " " * padding_length) + time_text + (" " * (terminal_width - len(time_text) - padding_length)) + RESET
    
    print("\n" + header_bar)
    print(time_bar)

    # 5. Display Stats Table
    print("\n" + BOLD + "--- Day Event Schedule (Local Time) ---" + RESET)
    
    # Define order for display
    display_order = [
        "astronomical_twilight_begin", "civil_twilight_begin", "sunrise", 
        "solar_noon", "sunset", "civil_twilight_end", "astronomical_twilight_end"
    ]
    
    time_data_line = ""
    # Assemble the times into a clean single row for the "stats" row
    for key in display_order:
        label = time_points[key]
        time = local_time_strings.get(key, "N/A")
        
        # Highlight the current phase's boundary markers (e.g., if it's civil twilight, highlight civil_b and sunrise/set)
        highlight = ""
        if (key == 'sunrise' and color_data['status'] == "☀️ FULL DAYLIGHT") or \
           (key == 'sunset' and color_data['status'] == "🏙️ Civil Twilight (Dusk)") or \
           (key.endswith('_twilight_begin') and "Dawn" in color_data['status']) or \
           (key.endswith('_twilight_end') and "Dusk" in color_data['status']):
            highlight = FG_YELLOW + BOLD
            
        time_data_line += f"| {highlight}{label}: {time:<10}{RESET} "

    print(time_data_line + "|")
    
    # Display day length
    day_length_hms = convert_seconds_to_hms(results.get("day_length"))
    print(f"\n{BOLD}⏳ Day Length:{RESET} {day_length_hms}")

# Execute the graphic generator
if __name__ == "__main__":
    generate_day_graphic()
