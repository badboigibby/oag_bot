from datetime import datetime
import pytz

def get_local_time(timezone='America/Edmonton', time_format='%Y-%m-%d %H:%M:%S'):
    """
    Get the current time in the specified timezone.

    Args:
        timezone (str): The desired timezone (default is 'America/Edmonton').
        time_format (str): The desired output format (default is '%Y-%m-%d %H:%M:%S').

    Returns:
        str: The current time formatted as a string, or an error message.
    """
    try:
        # Get the desired timezone
        local_tz = pytz.timezone(timezone)

        # Get the current time in UTC and convert to the desired timezone
        utc_now = datetime.now(pytz.utc)
        local_now = utc_now.astimezone(local_tz)

        # Format and return the time
        return local_now.strftime(time_format)

    except pytz.UnknownTimeZoneError:
        return f"Error: The specified timezone '{timezone}' is not recognized."
    except Exception as e:
        return f"Error: An unexpected error occurred - {str(e)}"

# Example usage
if __name__ == "__main__":
    print(get_local_time())  # Default: MST/MDT
    print(get_local_time('UTC'))  # UTC time
    print(get_local_time('Asia/Kolkata'))  # IST (Indian Standard Time)
    print(get_local_time('Invalid/Timezone'))  # Invalid timezone test
