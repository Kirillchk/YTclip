def convert_time_string_to_tuple(time_string):
    # Split the string by ":"
    time_parts = time_string.split(':')

    # Convert parts to integers (pad with zeros if necessary)
    minutes = int(time_parts[0])# Second part is minutes (default 0)
    seconds = int(time_parts[1]) if len(time_parts) > 1 else 0
    # Return as tuple (hours, minutes, seconds)
    return (0, minutes, seconds)





