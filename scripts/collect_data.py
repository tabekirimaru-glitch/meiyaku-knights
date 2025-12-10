#!/usr/bin/env python3
"""
Gemini APIを使用した判例・事件データ自動収集スクリプト
毎週GitHub Actionsで実行され、新しいデータを収集してJSONを更新します
"""

import os
import json
import re
from datetime import datetime
import google.generativeai as genai

# Gemini API設定
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# データファイルパス
DATA_DIR = 'data'
JUDGMENTS_FILE = os.path.join(DATA_DIR, 'judgments.json')
CHILD_CASES_FILE = os.path.join(DATA_DIR, 'child-cases.json')

def load_existing_data(filepath):
    """既存のJSONデータを読み込む"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(filepath, data):
    """JSONデータを保存"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(data)} items to {filepath}")

def extract_json_from_response(text):
    """レスポンスからJSON配列を抽出"""
    # コードブロック内のJSONを探す
    json_match = re.search(r'```(?:json)?\s*(\[[\s\S]*?\])\s*```', text)
    if json_match:
        return json_match.group(1)
    # コードブロックなしでJSON配列を探す
    json_match = re.search(r'\[[\s\S]*\]', text)
    if json_match:
        return json_match.group(0)
    return None

def collect_judgments():
    """判例データを収集"""
    print("📚 判例データを収集中...")
    
    existing = load_existing_data(JUDGMENTS_FILE)
    existing_urls = {item.get('url', '') for item in existing}
    
    prompt = """日本の家庭裁判所の最新の判決・事例を5件収集してください。

【収集条件】
- カテゴリ: 親権、監護者指定、子の引き渡し、面会交流、連れ去り
- 期間: 2023年〜現在
- 実在する判例・事例のみ（法律事務所の解決事例も可）

【出力形式】
以下のJSON配列形式で出力してください：

```json
[
  {
    "date": "YYYY-MM-DD",
    "court": "〇〇家庭裁判所",
    "title": "事例のタイトル（30文字程度）",
    "tags": ["親権", "父親", "認容"],
    "summary": "事例の概要（100文字程度）",
    "url": "https://実際のURL"
  }
]
```

【タグの例】
親権, 監護者指定, 面会交流, 子の引き渡し, 連れ去り, 父親, 母親, 認容, 却下, 和解, 調停, 審判, 訴訟, DV, モラハラ, 乳幼児, 小学生以上"""

    try:
        response = model.generate_content(prompt)
        json_str = extract_json_from_response(response.text)
        
        if not json_str:
            print("⚠️ JSONが見つかりませんでした")
            return
        
        new_items = json.loads(json_str)
        
        # 重複チェック
        added_count = 0
        max_id = max([item.get('id', 0) for item in existing], default=0)
        
        for item in new_items:
            if item.get('url') not in existing_urls:
                max_id += 1
                item['id'] = max_id
                item['collected_at'] = datetime.now().isoformat()
                existing.append(item)
                added_count += 1
        
        if added_count > 0:
            save_data(JUDGMENTS_FILE, existing)
            print(f"✅ {added_count}件の新しい判例を追加しました")
        else:
            print("ℹ️ 新しい判例はありませんでした")
            
    except Exception as e:
        print(f"❌ 判例収集エラー: {e}")

def collect_child_cases():
    """子供関連事件データを収集"""
    print("👶 子供関連事件データを収集中...")
    
    existing = load_existing_data(CHILD_CASES_FILE)
    existing_urls = {item.get('url', '') for item in existing}
    
    prompt = """日本で最近報道された子供に関する事件・事例を10件収集してください。

【収集条件】
- カテゴリ: 虐待事件、ネグレクト、家庭内暴力、離婚に伴う事件
- 期間: 2024年〜現在の最新ニュース
- 実際のニュース記事から収集（NHK、朝日新聞、読売新聞、毎日新聞、共同通信など）

【出力形式】
以下のJSON配列形式で出力してください：

```json
[
  {
    "date": "YYYY-MM-DD",
    "location": "〇〇県",
    "title": "事例のタイトル（30文字程度）",
    "tags": ["虐待", "実父", "逮捕", "乳幼児"],
    "summary": "事例の概要（100文字程度）",
    "url": "https://実際のニュースURL",
    "source": "ニュース媒体名"
  }
]
```

【locationの形式】
必ず「〇〇県」「〇〇府」「東京都」「北海道」の形式で記載

【タグの例】
- 事件種別: 虐待, ネグレクト, 暴行, 傷害, 死亡事件, 心中, 性的虐待, 監禁
- 加害者: 実父, 実母, 継父, 継母, 内縁, 交際相手, 祖父母, 親族
- 被害者: 乳幼児, 小学生, 中学生, 高校生, 複数
- 結果: 逮捕, 書類送検, 起訴, 保護, 死亡, 重傷
- 機関: 児童相談所, 警察, 学校, 病院, 近隣通報"""

    try:
        response = model.generate_content(prompt)
        json_str = extract_json_from_response(response.text)
        
        if not json_str:
            print("⚠️ JSONが見つかりませんでした")
            return
        
        new_items = json.loads(json_str)
        
        # 重複チェック
        added_count = 0
        max_id = max([item.get('id', 0) for item in existing], default=0)
        
        for item in new_items:
            if item.get('url') not in existing_urls:
                max_id += 1
                item['id'] = max_id
                item['collected_at'] = datetime.now().isoformat()
                existing.append(item)
                added_count += 1
        
        if added_count > 0:
            save_data(CHILD_CASES_FILE, existing)
            print(f"✅ {added_count}件の新しい事件を追加しました")
        else:
            print("ℹ️ 新しい事件はありませんでした")
            
    except Exception as e:
        print(f"❌ 事件収集エラー: {e}")

def main():
    print("=" * 50)
    print(f"🤖 データ収集開始: {datetime.now().isoformat()}")
    print("=" * 50)
    
    # データディレクトリ確認
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 判例データ収集
    collect_judgments()
    
    # 子供関連事件データ収集
    collect_child_cases()
    
    print("=" * 50)
    print("✅ データ収集完了!")
    print("=" * 50)

if __name__ == "__main__":
    main()
