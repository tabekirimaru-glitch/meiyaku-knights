import json

try:
    with open('data/youtube_raw.json', 'r', encoding='utf-8') as f:
        raw = json.load(f)
    
    videos = []
    if 'items' in raw:
        for item in raw['items']:
            snippet = item['snippet']
            thumbnails = snippet.get('thumbnails', {})
            thumb = thumbnails.get('medium', {}).get('url') or thumbnails.get('default', {}).get('url')
            
            videos.append({
                'id': snippet['resourceId']['videoId'],
                'title': snippet['title'],
                'thumbnail': thumb,
                'publishedAt': snippet['publishedAt']
            })
            
    with open('data/youtube.json', 'w', encoding='utf-8') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(videos)} videos to data/youtube.json")

except Exception as e:
    print(f"Error: {e}")
