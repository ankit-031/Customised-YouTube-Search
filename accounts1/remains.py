for index1, row in video_data.iterrows():
    print("index1")
    duration_str = row['Duration']
    if ':' in duration_str:
        duration_parts = duration_str.split(':')
        minutes = int(duration_parts[0])
        seconds = int(duration_parts[1])
        duration_iso = f"PT{minutes}M{seconds}S"
    else:
        duration_iso = duration_str

    duration_timedelta = pd.to_timedelta(duration_iso)
    # duration_timedelta = pd.to_timedelta(duration_str)
    video_data.at[index1, 'Duration'] = duration_timedelta
# video_data['Duration'] = video_data['Duration'].apply(parse_duration)
# video_data['Duration'] = pd.to_timedelta(video_data['Duration'])





    # print(video_data['Duration'])

    for index, row in video_data.iterrows():
        duration_str = row['Duration']
        print(duration_str)
        duration_str1 = parse_duration(duration_str)
        duration_timedelta = pd.to_timedelta(duration_str1)
        print(duration_timedelta)
        video_data.at[index, 'Duration'] = duration_timedelta

    video_data = video_data[video_data['Duration'] < pd.to_timedelta('10 minutes')]

    print(video_data)







    days = 0
    hours, minutes, seconds = 0, 0, 0

    # duration = duration.replace('PT', '')

    if 'D' in duration:
        days, duration = duration.split('D')
        days = int(days)

    if 'H' in duration:
        hours, duration = duration.split('H')
        hours = int(hours)

    if 'M' in duration:
        minutes, duration = duration.split('M')
        minutes = int(minutes)

    if 'S' in duration:
        seconds = int(duration.replace('S', ''))

    total_seconds = (days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60) + seconds
    print(f'seconds = {total_seconds}')
    return pd.to_timedelta(total_seconds, unit='s')