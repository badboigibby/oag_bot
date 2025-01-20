from datetime import datetime
import pytz

def get_mst_time():
    try:
        # Define the Mountain Standard Time zone (MST)
        mst = pytz.timezone('America/Edmonton')  # MST/MDT depending on daylight saving time

        # Get the current time in UTC and convert it to MST
        utc_now = datetime.now(pytz.utc)  # Current UTC time
        mst_now = utc_now.astimezone(mst)  # Convert to MST

        # Format the time as a string and return
        return mst_now.strftime('%Y-%m-%d %H:%M:%S')

    except pytz.UnknownTimeZoneError:
        return "Error: The specified timezone is not recognized."
    except Exception as e:
        return f"Error: An unexpected error occurred - {str(e)}"

# Example usage
if __name__ == "__main__":
    print(get_mst_time())
