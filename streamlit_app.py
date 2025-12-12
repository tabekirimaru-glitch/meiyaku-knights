"""
学校リスク予報AI - Streamlit App
Gemini AI + Google Custom Search でリアルタイム検索・分析
子ども事件DB連携 + Supabaseキャッシュ + レート制限
"""

import streamlit as st
import google.generativeai as genai
import requests
import urllib.parse
import hashlib
from datetime import datetime, timedelta

# ページ設定
st.set_page_config(
    page_title="学校リスク予報AI",
    page_icon="🏫",
    layout="centered"
)

# --- セッションベースのレート制限 ---
MAX_SEARCHES_PER_SESSION = 10

if "search_count" not in st.session_state:
    st.session_state.search_count = 0

def check_rate_limit() -> bool:
    return st.session_state.search_count < MAX_SEARCHES_PER_SESSION

def increment_search_count():
    st.session_state.search_count += 1

# --- Google Custom Search API ---
def google_search(query: str, num_results: int = 5) -> list:
    """Google Custom Search APIで検索"""
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY", "")
        cx = st.secrets.get("GOOGLE_CX", "")
        
        if not api_key:
            st.error("❌ GOOGLE_API_KEY が設定されていません")
            return []
        if not cx:
            st.error("❌ GOOGLE_CX が設定されていません")
            return []
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cx,
            "q": query,
            "num": num_results,
            "lr": "lang_ja"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Unknown error")
            st.error(f"❌ Google API エラー: {error_msg}")
            return []
        
        data = response.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        return results
    except Exception as e:
        st.error(f"❌ 検索エラー: {str(e)}")
    return []

# Supabase読み込み
try:
    from supabase import create_client, Client
    supabase_available = True
except ImportError:
    supabase_available = False

# --- Supabase設定 ---
supabase = None
cache_enabled = False

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    if supabase_available:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        cache_enabled = True
except:
    pass

# キャッシュ関数
def generate_cache_key(school_name: str, prefecture: str) -> str:
    raw = f"{school_name}_{prefecture}".lower().strip()
    return hashlib.md5(raw.encode()).hexdigest()

def get_from_cache(search_key: str):
    if not cache_enabled or not supabase:
        return None
    try:
        response = supabase.table("school_risk_cache").select("*").eq("search_key", search_key).execute()
        if response.data and len(response.data) > 0:
            record = response.data[0]
            # アクセス回数更新
            supabase.table("school_risk_cache").update({
                "access_count": record.get("access_count", 0) + 1,
            }).eq("id", record["id"]).execute()
            return record
    except:
        pass
    return None

def save_to_cache(school_name: str, prefecture: str, search_key: str, ai_result: str, search_results: str):
    if not cache_enabled or not supabase:
        return
    try:
        supabase.table("school_risk_cache").upsert({
            "school_name": school_name,
            "prefecture": prefecture,
            "search_key": search_key,
            "ai_result": ai_result,
            "search_results": search_results,
            "updated_at": datetime.now().isoformat()
        }).execute()
    except:
        pass

# 子ども事件データ
@st.cache_data(ttl=3600)
def load_child_cases():
    try:
        url = "https://tabekirimaru-glitch.github.io/meiyaku-knights/data/child-cases.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def find_related_cases(cases: list, search_term: str, prefecture: str, limit: int = 5):
    results = []
    search_keywords = []
    if prefecture != "指定なし":
        search_keywords.append(prefecture.replace("県", "").replace("府", "").replace("都", ""))
    
    for keyword in ["市", "区", "町", "村"]:
        if keyword in search_term:
            idx = search_term.find(keyword)
            if idx > 0:
                search_keywords.append(search_term[:idx])
                break
    
    search_keywords.append(search_term)
    
    for case in cases:
        title = case.get("title", "")
        for keyword in search_keywords:
            if keyword and len(keyword) >= 2 and keyword in title:
                results.append(case)
                break
        if len(results) >= limit:
            break
    return results

# --- Gemini API設定 ---
model = None
api_available = False

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    
    available = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available.append(m.name)
    
    preferred = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
    selected = None
    for p in preferred:
        if p in available:
            selected = p
            break
    
    if not selected and available:
        selected = available[0]
    
    if selected:
        model = genai.GenerativeModel(selected)
        api_available = True
except:
    pass

# カスタムCSS（ダークモード対応）
st.markdown("""
<style>
    .main-header { font-size: 1.8rem; font-weight: 800; color: #1e3a5f; text-align: center; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1rem; color: #64748b; text-align: center; margin-bottom: 2rem; }
    .search-result { background: #1e293b; padding: 0.75rem; border-radius: 8px; border: 1px solid #334155; margin-bottom: 0.5rem; }
    .search-result a { color: #60a5fa; text-decoration: none; font-weight: 600; }
    .search-result a:hover { text-decoration: underline; }
    .search-result p { color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem; }
    .cache-badge { background: #22c55e; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; }
    .warning-card { background: #7f1d1d; padding: 1rem; border-radius: 8px; border-left: 4px solid #f87171; margin: 0.5rem 0; color: #fecaca !important; }
    .warning-card strong { color: #fca5a5 !important; }
    .case-card { background: #1e293b; padding: 0.75rem; border-radius: 8px; border: 1px solid #334155; margin-bottom: 0.5rem; color: #e2e8f0 !important; }
    .case-card strong { color: #93c5fd !important; }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<div class="main-header">🏫 学校リスク予報AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">学校名を入力して、AIによる安全性分析を確認</div>', unsafe_allow_html=True)

# 検索フォーム
col1, col2 = st.columns([3, 1])
with col1:
    school_name = st.text_input("学校名を入力", placeholder="例：〇〇市立△△小学校", label_visibility="collapsed")
with col2:
    search_button = st.button("🔍 調べる", type="primary", use_container_width=True)

prefecture = st.selectbox(
    "都道府県（オプション）",
    ["指定なし"] + [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
        "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
        "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
        "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
        "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
        "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ],
    label_visibility="collapsed"
)

st.divider()

# AI分析関数
def analyze_with_search_results(school_name: str, prefecture: str, search_results: list) -> str:
    """Google検索結果を元にGeminiで分析"""
    location = f"{prefecture}の" if prefecture != "指定なし" else ""
    
    # 検索結果をテキスト化
    search_text = ""
    for i, r in enumerate(search_results, 1):
        search_text += f"{i}. {r['title']}\n   URL: {r['link']}\n   概要: {r['snippet']}\n\n"
    
    if not search_text:
        search_text = "検索結果が見つかりませんでした。"
    
    prompt = f"""
あなたは学校の安全性と教育環境を分析する専門家AIです。
以下のGoogle検索結果を元に、{location}{school_name}の詳細分析を行ってください。

【Google検索結果】
{search_text}

【分析項目】親の視点で以下を詳しく分析してください：

1. **安全性・事件情報**
   - 過去の事件・事故・いじめ報道
   - 学校の対応姿勢（隠蔽傾向 or 透明性）

2. **地域の治安**
   - 不審者情報の有無
   - 通学路の安全性
   - 周辺の犯罪発生状況

3. **教育環境**
   - 学力水準・進学実績（情報があれば）
   - 部活動の充実度
   - 特別支援・発達障害への対応

4. **保護者の評判**
   - 口コミサイトでの評価
   - 先生の評判
   - PTA活動の負担感

5. **子育て環境**
   - 学童保育の状況
   - 周辺の習い事・塾
   - 地域コミュニティの活発さ

【出力形式】
## 🎯 総合評価
[安心/注意必要/要警戒/情報不足] と理由を1-2文で

## 🚨 安全性・事件情報
（発見された記事はURLを含めて記載。なければ「重大な事件報道は見つかりませんでした」）

## 🏘️ 地域の治安
- 不審者情報: 
- 通学路: 
- 周辺治安: 

## 📚 教育環境
- 学力: 
- 部活: 
- 特別支援: 

## 👨‍👩‍👧 保護者の評判
（口コミ情報があれば記載）

## 🏠 子育て環境
- 学童: 
- 習い事・塾: 

## 💡 この学校を検討中の保護者へ
（2-3文のアドバイス）

## 🔗 参考にしたURL
（検索で見つかった重要なURLを箇条書き）

---
※この分析は{datetime.now().strftime('%Y年%m月%d日')}時点のGoogle検索結果に基づく参考情報です。
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ 分析中にエラーが発生しました: {str(e)}"

def demo_analysis(school_name: str) -> str:
    return f"""
## 🎯 総合リスク評価
**情報不足** - Google検索APIが設定されていないため、デモモードで動作しています。

## 📰 発見された記事・情報
Streamlit SecretsにGOOGLE_API_KEYとGOOGLE_CXを設定すると、実際のGoogle検索結果を表示できます。

## 📊 分析結果
（デモ表示）

## 💡 保護者へのアドバイス
学校見学や説明会に参加して確認することをお勧めします。
"""

# 検索実行
if search_button and school_name:
    if not check_rate_limit():
        st.error(f"⚠️ 検索回数の上限（{MAX_SEARCHES_PER_SESSION}回）に達しました。")
    else:
        search_key = generate_cache_key(school_name, prefecture)
        
        # キャッシュ確認
        cached = get_from_cache(search_key)
        
        if cached:
            st.success(f"「{school_name}」の分析結果を表示")
            st.markdown('<span class="cache-badge">⚡ キャッシュから取得</span>', unsafe_allow_html=True)
            result = cached.get("ai_result", "")
            
            # 保存された検索結果を表示
            if cached.get("search_results"):
                st.subheader("🔍 Google検索結果")
                st.markdown(cached.get("search_results", ""))
        else:
            increment_search_count()
            remaining = MAX_SEARCHES_PER_SESSION - st.session_state.search_count
            
            with st.spinner("🔍 多角的に情報収集中..."):
                # 親目線の多角的なクエリで検索
                queries = [
                    f"{school_name} 事件 いじめ",
                    f"{school_name} 口コミ 評判",
                    f"{school_name} 不審者 治安"
                ]
                
                all_results = []
                seen_links = set()
                
                for q in queries:
                    results = google_search(q, num_results=3)
                    for r in results:
                        if r["link"] not in seen_links:
                            all_results.append(r)
                            seen_links.add(r["link"])
            
            # 検索結果を表示
            if all_results:
                st.subheader("🔍 Google検索結果")
                search_results_html = ""
                for r in all_results[:8]:  # 最大8件表示
                    search_results_html += f"""
                    <div class="search-result">
                        <a href="{r['link']}" target="_blank">{r['title']}</a>
                        <p>{r['snippet'][:150]}...</p>
                    </div>
                    """
                st.markdown(search_results_html, unsafe_allow_html=True)
            else:
                st.info("Google検索結果が見つかりませんでした（APIキー未設定またはヒットなし）")
            
            with st.spinner("🤖 AIが分析中..."):
                if api_available and all_results:
                    result = analyze_with_search_results(school_name, prefecture, all_results)
                    # キャッシュ保存
                    save_to_cache(school_name, prefecture, search_key, result, search_results_html if all_results else "")
                else:
                    result = demo_analysis(school_name)
            
            st.success(f"「{school_name}」の分析が完了しました")
            if remaining > 0:
                st.caption(f"残り検索回数: {remaining}回")
        
        # AI分析結果を表示
        st.divider()
        st.subheader("📊 AI分析結果")
        st.markdown(result)
        
        # --- 子ども事件DB連携 ---
        st.divider()
        st.subheader("📰 子ども事件DBから")
        
        child_cases = load_child_cases()
        related_cases = find_related_cases(child_cases, school_name, prefecture)
        
        if related_cases:
            st.info(f"関連する事件が **{len(related_cases)}件** 見つかりました")
            for case in related_cases:
                st.markdown(f"""
                <div class="case-card">
                    <strong>📅 {case.get('date', '日付不明')}</strong><br>
                    {case.get('title', 'タイトルなし')[:80]}...
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <a href="https://tabekirimaru-glitch.github.io/meiyaku-knights/child-cases.html" target="_blank" 
               style="display: inline-block; background: #7c3aed; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none;">
                📊 子ども事件DBで詳しく見る →
            </a>
            """, unsafe_allow_html=True)
        else:
            st.info("この地域の関連事件は見つかりませんでした")
        
        # 免責事項
        st.divider()
        st.markdown("""
        <div class="warning-card">
            <strong>⚠️ 重要な注意事項</strong><br>
            この結果はAIによる公開情報の分析に基づく参考情報です。
            実際の学校の安全性を保証するものではありません。
            最終的な判断はご自身で行ってください。
        </div>
        """, unsafe_allow_html=True)

elif search_button and not school_name:
    st.warning("学校名を入力してください")

# フッター
st.divider()
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem;">
    © 2025 片翼の盟約騎士団 | 
    <a href="https://tabekirimaru-glitch.github.io/meiyaku-knights/" target="_blank">サイトに戻る</a>
</div>
""", unsafe_allow_html=True)
