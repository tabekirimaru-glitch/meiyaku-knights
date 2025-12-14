"""
YouTube Data Collection Script
YouTube Data API v3 を使って最新動画情報を取得
"""

import os
import json
import requests

# 設定
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UC_YFzkuNqO5a_3-qE1QqTrw"  # @meiyaku_knights のチャンネルID
MAX_RESULTS = 10

def get_uploads_playlist_id():
    """チャンネルのアップロード動画プレイリストIDを取得"""
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "key": YOUTUBE_API_KEY,
        "id": CHANNEL_ID,
        "part": "contentDetails"
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error getting channel info: {response.status_code}")
        print(response.text)
        return None
    
    data = response.json()
    if data.get("items"):
        return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return None

def get_latest_videos(playlist_id):
    """プレイリストから最新動画を取得"""
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "key": YOUTUBE_API_KEY,
        "playlistId": playlist_id,
        "part": "snippet",
        "maxResults": MAX_RESULTS
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error getting videos: {response.status_code}")
        print(response.text)
        return []
    
    data = response.json()
    videos = []
    
    for item in data.get("items", []):
        snippet = item["snippet"]
        thumbnails = snippet.get("thumbnails", {})
        thumb = thumbnails.get("medium", {}).get("url") or thumbnails.get("default", {}).get("url")
        
        if snippet.get("title") != "Private video" and snippet.get("title") != "Deleted video":
            videos.append({
                "id": snippet["resourceId"]["videoId"],
                "title": snippet["title"],
                "thumbnail": thumb,
                "publishedAt": snippet["publishedAt"]
            })
    
    return videos

def main():
    if not YOUTUBE_API_KEY:
        print("Error: YOUTUBE_API_KEY environment variable not set")
        return
    
    print("🎬 YouTube データ収集開始...")
    
    # プレイリストID取得
    playlist_id = get_uploads_playlist_id()
    if not playlist_id:
        print("Error: Could not get uploads playlist ID")
        return
    
    print(f"📋 プレイリストID: {playlist_id}")
    
    # 最新動画取得
    videos = get_latest_videos(playlist_id)
    print(f"📹 取得動画数: {len(videos)}")
    
    # 保存
    output_path = "data/youtube.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 保存完了: {output_path}")
    
    # 確認用に最新動画タイトルを表示
    if videos:
        print(f"📺 最新動画: {videos[0]['title']}")

if __name__ == "__main__":
    main()
