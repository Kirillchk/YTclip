def convert_time_string_to_seconds(time_string):
    if time_string is None:
        return None
    try:
        time_parts = time_string.split(':')
        if len(time_parts) == 0 or len(time_parts) > 2:
            return None
        minutes = int(time_parts[0])
        seconds = int(time_parts[1]) if len(time_parts) > 1 else 0
        return minutes * 60 + seconds
    except (ValueError, IndexError):
        return None
