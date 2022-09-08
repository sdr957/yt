################# pytube to download youtube video############
import pandas as pd
from pytube import YouTube
import csv
from collections import defaultdict


###############
csv_file=open('yt.csv','w')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Title','Thumbnail','url_link','Views','likes','Number of comments','commentss'])
link="https://www.youtube.com/watch?v=82fPl5l0vXY"
youtube1=YouTube(link)



# print(youtube1.channel_id)
# print(youtube1.video_id)
title=youtube1.title
thumbnail=youtube1.thumbnail_url
url_link=youtube1.embed_url

print('#################################################')

############# comment and replies using youtube data api  ###########
from googleapiclient.discovery import build

api_key = 'AIzaSyAIjlkNdsYbdrTdnc-_5MeZ4qAGpKvuFic'
video_id = '82fPl5l0vXY'

youtube = build('youtube', 'v3',
                developerKey=api_key)


def video_details():

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()

    request1 = youtube.commentThreads().list(
        part="snippet,replies",
        order='relevance',
        videoId=video_id
    )
    response1 = request1.execute()
    # print(response1)

    # print(response)
    for item in response['items']:
        views=item['statistics']['viewCount']
        likes=item['statistics']['likeCount']
        comments=item['statistics']['commentCount']


    print('###########################')


    ######################################## Extracting comments
    dictt=defaultdict(dict)
    comm={}
    for item in response1['items']:

        commentor = item['snippet']['topLevelComment']['snippet']["authorDisplayName"]
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        totalReplyCount = item['snippet']['totalReplyCount']

        comm.update({commentor:comment})
        dictt[commentor]=comment

        # print(commentor, ':>', comment, totalReplyCount)

        if totalReplyCount > 0:
            for reply in item['replies']['comments']:
                replies = reply['snippet']['textDisplay']
                replier = reply['snippet']['authorDisplayName']
                # print(replier, "==>", replies)
                # dictt[comment]=replies
    csv_writer.writerow([title, thumbnail, url_link, views, likes, comments, dictt],encoding="utf-8")



    # print(dictt)
        # if 'nextPageToken' in response:
        #     video_response = youtube.commentThreads().list(
        #         part='snippet,replies',
        #         videoId=video_id
        #     ).execute()
        # else:
        #     break

                # for k, v in dictt.items():
                #     print(k, ':>>', v)


video_details()
