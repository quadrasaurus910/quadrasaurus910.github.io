import requests
from datetime import datetime, timedelta

# --- Configuration for Southport, NC ---
API_URL = "https://api.sunrise-sunset.org/json"

# Southport, NC Coordinates and Offset (EDT is UTC-4)
LATITUDE = 33.92
LONGITUDE = -78.02
UTC_OFFSET = -4 
TIMEZONE_LABEL = "EDT (UTC-4)"

def convert_seconds_to_hms(total_seconds):
    """Converts a total number of seconds into Hours, Minutes, and Seconds string."""
    if total_seconds is None:
        return "N/A"
        
    total_seconds = int(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}h {minutes:02}m {seconds:02}s"

def get_sun_times():
    """
    Fetches sunrise, sunset, and twilight times from the sunrise-sunset.org API,
    converts them to local time, and displays the results.
    """
    print(f"--- Sun Events for Southport, NC ({TIMEZONE_LABEL}) ---")

    # 1. Prepare API parameters
    # 'formatted=0' returns times in ISO 8601 format and day_length in seconds.
    params = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0
    }

    print(f"📍 Coordinates: {LATITUDE}° N, {abs(LONGITUDE)}° W")
    
    # 2. Make the API request
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred while connecting to the API: {e}")
        return

    # 3. Process and display results
    if data.get("status") == "OK":
        results = data["results"]
        
        # Define the keys we want to display and their corresponding labels
        time_points = {
            "sunrise": "🌅 Sunrise",
            "sunset": "🌇 Sunset",
            "solar_noon": "☀️ Solar Noon",
            "civil_twilight_begin": "🏙️ Civil Twilight Begin (Official)",
            "civil_twilight_end": "🌃 Civil Twilight End (Official)",
            "nautical_twilight_begin": "⚓ Nautical Twilight Begin",
            "nautical_twilight_end": "⚓ Nautical Twilight End",
            "astronomical_twilight_begin": "🔭 Astronomical Twilight Begin",
            "astronomical_twilight_end": "🔭 Astronomical Twilight End"
        }

        offset_delta = timedelta(hours=UTC_OFFSET)
        
        print("\n--- Event Times (Local Wall Clock Time) ---")
        
        # Function to convert and print time
        def print_local_time(label, time_str):
            try:
                # Parse the ISO 8601 time string (e.g., 2025-10-25T05:47:04+00:00)
                # Ensure compatibility by replacing Z with +00:00 for the parser
                utc_time = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                
                # Convert from UTC to local time by applying the offset
                local_time = utc_time + offset_delta
                
                # Format for display (e.g., 05:47:04 AM)
                print(f"{label:<40}: {local_time.strftime('%I:%M:%S %p')}")
                
            except (ValueError, AttributeError, TypeError):
                print(f"{label:<40}: Error parsing time value.")

        # Display all time points
        for key, label in time_points.items():
            if key in results:
                print_local_time(label, results[key])
        
        # Display day length converted to H:M:S
        day_length_hms = convert_seconds_to_hms(results.get("day_length"))
        print(f"\n{'⏳ Total Day Length':<40}: {day_length_hms}")

    else:
        print(f"\nAPI Error: Request failed. Status: {data.get('status')}. Please check your configuration.")

# Execute the function
if __name__ == "__main__":
    get_sun_times()
