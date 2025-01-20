from datetime import datetime
import pytz

def get_mst_time():
    try:
        # Define the Mountain Standard Time zone (MST)
        mst = pytz.timezone('America/Edmonton')  # Use 'America/Denver' if you prefer

        # Get the current time in UTC, then convert it to MST
        utc_now = datetime.now(pytz.utc)
        mst_now = utc_now.astimezone(mst)

        return mst_now.strftime('%Y-%m-%d %H:%M:%S')

    except pytz.UnknownTimeZoneError:
        return "Error: The timezone is not recognized."
    except Exception as e:
        return f"Error: {str(e)}"
