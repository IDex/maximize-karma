def hour_to_time(f):
    return f'{int(f // 1):02}:{int(round(f % 1 * 60)):02}'
