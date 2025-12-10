const fs = require('fs');

try {
    const raw = JSON.parse(fs.readFileSync('data/youtube_raw.json', 'utf8'));

    if (!raw.items) {
        console.error('No items found in raw data');
        process.exit(1);
    }

    const videos = raw.items.map(item => ({
        id: item.snippet.resourceId.videoId,
        title: item.snippet.title,
        thumbnail: item.snippet.thumbnails.medium?.url || item.snippet.thumbnails.default?.url,
        publishedAt: item.snippet.publishedAt
    }));

    fs.writeFileSync('data/youtube.json', JSON.stringify(videos, null, 2));
    console.log(`Saved ${videos.length} videos to data/youtube.json`);
} catch (e) {
    console.error(e);
}
