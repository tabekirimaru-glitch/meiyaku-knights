#!/usr/bin/env python3
"""
RSSフィードから子供関連事件ニュースを収集するスクリプト
実際のニュース記事URLを取得し、キーワードでフィルタリング
"""

import os
import json
import feedparser
from datetime import datetime
from urllib.parse import urlparse

# データファイルパス
DATA_DIR = 'data'
CHILD_CASES_FILE = os.path.join(DATA_DIR, 'child-cases.json')

# RSSフィード一覧（日本のニュースソース）
RSS_FEEDS = [
    {"url": "https://news.google.com/rss/search?q=児童虐待&hl=ja&gl=JP&ceid=JP:ja", "source": "Google News"},
    {"url": "https://news.google.com/rss/search?q=子ども+事件&hl=ja&gl=JP&ceid=JP:ja", "source": "Google News"},
    {"url": "http://www3.nhk.or.jp/rss/news/cat0.xml", "source": "NHK"},
    {"url": "https://mainichi.jp/rss/etc/mainichi-flash.rss", "source": "毎日新聞"},
    {"url": "https://www.asahi.com/rss/asahi/newsheadlines.rdf", "source": "朝日新聞"},
]

# メインキーワード（少なくとも1つ必須）- 緩和
MAIN_KEYWORDS = ["虐待", "ネグレクト", "児童", "子ども", "子供", "児童相談所", "保護", "幼児", "乳児", "小学生", "園児"]

# サブキーワード（事件性を示す）
SUB_KEYWORDS = ["傷害", "逮捕", "死亡", "暴行", "事件", "容疑", "送検", "起訴", "殺害", "遺体"]

def load_existing_data():
    """既存のJSONデータを読み込む"""
    if os.path.exists(CHILD_CASES_FILE):
        with open(CHILD_CASES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """JSONデータを保存"""
    with open(CHILD_CASES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(data)} items to {CHILD_CASES_FILE}")

def is_relevant_article(title, summary=""):
    """記事が子供関連事件に関係するかチェック"""
    text = (title + " " + summary).lower()
    
    # メインキーワードが1つ以上含まれているか
    has_main = any(kw in text for kw in MAIN_KEYWORDS)
    
    if not has_main:
        return False
    
    # サブキーワードも含まれていればより確実
    has_sub = any(kw in text for kw in SUB_KEYWORDS)
    
    # メインキーワードだけでもOK、サブがあればボーナス
    return True

def extract_tags(title, summary=""):
    """タイトルと概要からタグを抽出"""
    text = title + " " + summary
    tags = []
    
    # メインキーワードからタグ抽出
    for kw in MAIN_KEYWORDS:
        if kw in text:
            tags.append(kw)
    
    # サブキーワードからタグ抽出
    for kw in SUB_KEYWORDS:
        if kw in text:
            tags.append(kw)
    
    # 加害者タグ
    if "父" in text or "父親" in text:
        tags.append("実父")
    if "母" in text or "母親" in text:
        tags.append("実母")
    if "継父" in text:
        tags.append("継父")
    if "継母" in text:
        tags.append("継母")
    if "交際相手" in text:
        tags.append("交際相手")
    
    return list(set(tags))  # 重複除去

def parse_date(entry):
    """RSSエントリから日付を抽出"""
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        return datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6]).strftime('%Y-%m-%d')
    return datetime.now().strftime('%Y-%m-%d')

def collect_from_rss():
    """RSSフィードから記事を収集"""
    print("📡 RSSフィードから子供関連事件を収集中...")
    
    existing = load_existing_data()
    existing_urls = {item.get('url', '') for item in existing}
    
    new_items = []
    max_id = max([item.get('id', 0) for item in existing], default=0)
    
    for feed_info in RSS_FEEDS:
        try:
            print(f"  🔍 {feed_info['source']}...")
            feed = feedparser.parse(feed_info['url'])
            
            for entry in feed.entries:
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                url = entry.get('link', '')
                
                # 既存URLはスキップ
                if url in existing_urls:
                    continue
                
                # 関連記事かチェック
                if not is_relevant_article(title, summary):
                    continue
                
                max_id += 1
                new_item = {
                    "id": max_id,
                    "date": parse_date(entry),
                    "title": title[:50],  # 50文字に制限
                    "summary": summary[:150] if summary else title,  # 150文字に制限
                    "url": url,
                    "source": feed_info['source'],
                    "tags": extract_tags(title, summary),
                    "collected_at": datetime.now().isoformat()
                }
                new_items.append(new_item)
                existing_urls.add(url)
                
        except Exception as e:
            print(f"  ❌ {feed_info['source']}エラー: {e}")
    
    if new_items:
        existing.extend(new_items)
        save_data(existing)
        print(f"✅ {len(new_items)}件の新しい記事を追加しました")
    else:
        print("ℹ️ 新しい記事はありませんでした")
    
    return len(new_items)

def main():
    print("=" * 50)
    print(f"🤖 RSS収集開始: {datetime.now().isoformat()}")
    print("=" * 50)
    
    os.makedirs(DATA_DIR, exist_ok=True)
    collect_from_rss()
    
    print("=" * 50)
    print("✅ RSS収集完了!")
    print("=" * 50)

if __name__ == "__main__":
    main()
