# TimeWastedOnline Project
# Paul Yunsuk Paik
# ppaik4311@gmail.com
# 02/02/2022
# This script will parse records.

import re
import os
import pandas as pd

START_OF_BLOCK = '<div class="mdl-grid"><div class="header-cell mdl-cell mdl-cell--12-col"><p class="mdl-typography--title">YouTube<br></p></div><div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">'
END_OF_BLOCK = '<div class=\"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right\">'
DELETED_VIDEO_INFORMATION = 'https://myaccount.google.com/activitycontrols'
KOREAN_AM = '오전'

data_dict = {'video_url':[],
             'video_title':[],
             'channel_name':[],
             'accessed_time':[]}

# Read raw data, parse data, and convert to Pandas DataFrame.
with open(f'{os.getcwd()}/data_set/Takeout/Youtube/History/view_history.html') as file:
    for line in file:
        break_down_list = line.split(START_OF_BLOCK)
        # Breakdown information block and parse data.
        for data_block in break_down_list:
            tmp_parsed_string = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data_block)
            if tmp_parsed_string:
                video_url = tmp_parsed_string.group()
                # If Youtube video URL is still valid in the logs, parse out data containing video title and channel name. Modify data_block for further parsing.
                if DELETED_VIDEO_INFORMATION not in video_url:
                    data_block = data_block.replace(f'<a href=\"{tmp_parsed_string.group()}\">', '')
                    video_title_end_index = data_block.find('</a>')
                    video_title = data_block[:video_title_end_index]
                    data_block = data_block.replace(video_title, '')
                    data_block = data_block[data_block.find('<br>'):]
                    data_block = data_block[data_block.find('\">') + 2:]
                    channel_name = data_block[:data_block.find('<')]
                    # There were some cases where the video_url name and video_title were the same with no channel name. This is the case where the video is no longer available.
                    if video_url != video_title and channel_name != "":
                        # Parse out time information when video was viewed.
                        data_block = data_block.replace(f'{channel_name}</a><br>', '')
                        raw_accessed_time = data_block[:data_block.find('<')]
                        tmp_time = raw_accessed_time.split(" ")
                        if tmp_time[3] == KOREAN_AM:
                            tmp_time[3] = "AM"
                        else:
                            tmp_time[3] = "PM"
                        # Massage time information and update dictionary only if meeting criteria.
                        if len(tmp_time) == 6:
                            data_dict['video_url'].append(video_url)
                            data_dict['video_title'].append(video_title)
                            data_dict['channel_name'].append(channel_name)
                            accessed_time = f"{tmp_time[1].replace('.', '-')}{tmp_time[2].replace('.', '-')}{tmp_time[0].strip('.')} {tmp_time[4]} {tmp_time[3]}"
                            data_dict['accessed_time'].append(accessed_time)

# Organize record data frame for youtube view records.
# I have only filtered out results based number of access time. If I saw a channel more than twice,
# I consider it to be intentional.
yt_records_df = pd.DataFrame(data_dict)
yt_records_df = yt_records_df.groupby(by='channel_name', as_index=False).nunique()
yt_records_df = yt_records_df.sort_values(by='accessed_time', ascending=False)
yt_records_df = yt_records_df[yt_records_df['accessed_time'] >= 2]
yt_records_df = yt_records_df.rename(columns={'video_url':'#_of_unique_urls', 'video_title':'#_of_unique_video_titles', 'accessed_time':'#_of_accessed_time'})
yt_records_df = yt_records_df.reset_index(drop=True)

# Explore methods to sort out channel category information and more details.