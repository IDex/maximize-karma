def hour_to_time(f):
    return f'{int(f // 1)}:{int(round(f % 1 * 60))}'
