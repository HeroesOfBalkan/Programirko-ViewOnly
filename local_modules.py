from googleapiclient.discovery import build

def youtube_search(search: str, max_results = 10):
    serv = build("youtube", "v3", developerKey = "nuh uh!")
    req = serv.search().list(part = "snippet", 
                            q = search, 
                            maxResults = max_results
                            )

    response = req.execute()


    result = []

    for i in response["items"]:
        tmp = {}
        if i["id"]["kind"] == "youtube#video" and (i["snippet"]["liveBroadcastContent"] == "none" or i["snippet"]["liveBroadcastContent"] == "upcoming"):
            tmp["videoID"] = i["id"].get("videoId")
            tmp["channelID"] = i["snippet"]["channelId"]
            tmp["videoTitle"] = i["snippet"]["title"]
            tmp["thumbnailURL"] = i["snippet"]["thumbnails"]["high"]["url"]
            tmp["channelName"] = i["snippet"]["channelTitle"]
            
            result.append(tmp)

    return result



def youtube_video(video: str):
    serv = build("youtube", "v3", developerKey = "nuh uh!")
    req = serv.videos().list(part = "snippet", id = video, maxResults = 1)

    response = req.execute()


    result = {}

    try:
        result["videoID"] = response["items"][0]["id"]
        result["channelID"] = response["items"][0]["snippet"]["channelId"]
        result["videoTitle"] = response["items"][0]["snippet"]["title"]
        result["desc"] = response["items"][0]["snippet"]["description"]
        result["channelName"] = response["items"][0]["snippet"]["channelTitle"]
    except Exception as e:
        print(f"Something happened: {e}")

    return result
