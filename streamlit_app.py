"""
学校リスク予報AI - Streamlit App
Gemini AIが学校の安全性とリスク管理体制を分析します
子ども事件DB連携 + Google検索リンク機能付き
"""

import streamlit as st
import google.generativeai as genai
import requests
import urllib.parse
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="学校リスク予報AI",
    page_icon="🏫",
    layout="centered"
)

# 子ども事件データを読み込む
@st.cache_data(ttl=3600)  # 1時間キャッシュ
def load_child_cases():
    """GitHub Pagesから子ども事件データを取得"""
    try:
        url = "https://tabekirimaru-glitch.github.io/meiyaku-knights/data/child-cases.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

# 地域に関連する事件を検索
def find_related_cases(cases: list, search_term: str, prefecture: str, limit: int = 5):
    """学校名や都道府県から関連する事件を検索"""
    results = []
    
    # 検索キーワードを抽出（市区町村名など）
    search_keywords = []
    if prefecture != "指定なし":
        search_keywords.append(prefecture.replace("県", "").replace("府", "").replace("都", ""))
    
    # 学校名から地名を抽出（例：「横浜市立○○小学校」→「横浜」）
    for keyword in ["市", "区", "町", "村"]:
        if keyword in search_term:
            idx = search_term.find(keyword)
            if idx > 0:
                city_name = search_term[:idx]
                search_keywords.append(city_name)
                break
    
    # 学校名自体も検索
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

# Gemini API設定
model = None
api_available = False

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 利用可能なモデルを取得
    available = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available.append(m.name)
    
    # 優先順位でモデルを選択
    preferred_models = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro', 
        'models/gemini-pro',
        'models/gemini-1.0-pro'
    ]
    
    selected_model = None
    for pref in preferred_models:
        if pref in available:
            selected_model = pref
            break
    
    if not selected_model and available:
        selected_model = available[0]
    
    if selected_model:
        model = genai.GenerativeModel(selected_model)
        api_available = True
    else:
        st.warning(f"⚠️ 利用可能なモデルがありません")
        
except Exception as e:
    st.warning(f"⚠️ デモモードで動作中")

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e3a5f;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-score {
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .risk-low { background: #dcfce7; color: #166534; }
    .risk-medium { background: #fef9c3; color: #854d0e; }
    .risk-high { background: #fee2e2; color: #991b1b; }
    .info-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
    }
    .warning-card {
        background: #fef2f2;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc2626;
        margin: 0.5rem 0;
    }
    .ai-response {
        background: #f0f9ff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #bae6fd;
        line-height: 1.8;
    }
    .case-card {
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.5rem;
    }
    .case-card:hover {
        border-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<div class="main-header">🏫 学校リスク予報AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">学校名を入力して、AIによる安全性分析を確認</div>', unsafe_allow_html=True)

# 検索フォーム
col1, col2 = st.columns([3, 1])
with col1:
    school_name = st.text_input(
        "学校名を入力",
        placeholder="例：〇〇市立△△小学校",
        label_visibility="collapsed"
    )
with col2:
    search_button = st.button("🔍 調べる", type="primary", use_container_width=True)

# 都道府県選択（オプション）
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

# Gemini AIで分析
def analyze_school_with_gemini(school_name: str, prefecture: str) -> str:
    """Gemini AIを使って学校のリスク分析を行う"""
    
    location = f"{prefecture}の" if prefecture != "指定なし" else ""
    
    prompt = f"""
あなたは学校の安全性を分析する専門家AIです。
以下の学校について、公開情報に基づいてリスク分析を行ってください。

【分析対象】
{location}{school_name}

【分析項目】
1. 過去の事件・事故（報道された事例があれば）
2. 学校の対応・情報公開度（隠蔽体質の有無）
3. 地域の治安情報
4. いじめ・体罰などの問題報告
5. 保護者からの評判（口コミがあれば）

【出力形式】
## 🎯 総合リスク評価
[低リスク/中リスク/高リスク/情報不足] のいずれかを選び、理由を説明

## 📊 分析結果

### ✅ ポジティブな点
- （箇条書きで）

### ⚠️ 注意が必要な点
- （箇条書きで）

### 📝 補足情報
- （見つかった情報を記載。なければ「公開情報が限られています」と記載）

## 💡 保護者へのアドバイス
（1-2文で簡潔に）

---
※この分析は公開情報に基づくAI推測です。実際の状況は学校に直接お問い合わせください。
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ 分析中にエラーが発生しました: {str(e)}"

# デモ用の分析結果
def demo_analysis(school_name: str) -> str:
    return f"""
## 🎯 総合リスク評価
**情報不足** - 公開されている情報が限られているため、詳細な評価が困難です。

## 📊 分析結果

### ✅ ポジティブな点
- 特筆すべき重大事件の報道は確認されませんでした
- 一般的な公立学校としての運営が行われている可能性が高い

### ⚠️ 注意が必要な点
- 具体的なリスク情報は見つかりませんでした
- 詳細な安全対策については学校に直接確認が必要

### 📝 補足情報
- これはデモ表示です。Gemini APIを設定すると、実際のAI分析が行われます。

## 💡 保護者へのアドバイス
学校見学や説明会に参加し、実際の雰囲気や安全対策を確認することをお勧めします。

---
※この分析はデモ表示です。実際の運用時はAIが公開情報を分析します。
"""

# 検索実行
if search_button and school_name:
    with st.spinner("🤖 AIが情報を収集・分析中..."):
        if api_available:
            result = analyze_school_with_gemini(school_name, prefecture)
        else:
            import time
            time.sleep(2)  # デモ用の遅延
            result = demo_analysis(school_name)
    
    st.success(f"「{school_name}」の分析が完了しました")
    
    # 分析結果を表示
    st.markdown(result)
    
    # --- 子ども事件DB連携 ---
    st.divider()
    st.subheader("📰 周辺の子ども関連事件")
    
    child_cases = load_child_cases()
    related_cases = find_related_cases(child_cases, school_name, prefecture)
    
    if related_cases:
        st.info(f"この地域に関連する事件が **{len(related_cases)}件** 見つかりました")
        
        for case in related_cases:
            with st.container():
                st.markdown(f"""
                <div class="case-card">
                    <strong>📅 {case.get('date', '日付不明')}</strong><br>
                    {case.get('title', 'タイトルなし')[:80]}...
                </div>
                """, unsafe_allow_html=True)
        
        # 子ども事件DBへのリンク
        st.markdown(f"""
        <a href="https://tabekirimaru-glitch.github.io/meiyaku-knights/child-cases.html" target="_blank" 
           style="display: inline-block; background: #7c3aed; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; margin-top: 0.5rem;">
            📊 子ども事件DBで詳しく見る →
        </a>
        """, unsafe_allow_html=True)
    else:
        st.info("この地域に関連する事件データは見つかりませんでした")
    
    # --- Google検索リンク ---
    st.divider()
    st.subheader("🔍 もっと調べる")
    
    # Google検索クエリを生成
    search_query = urllib.parse.quote(f"{school_name} 事件 事故 いじめ")
    google_url = f"https://www.google.com/search?q={search_query}"
    
    news_query = urllib.parse.quote(f"{school_name}")
    news_url = f"https://www.google.com/search?q={news_query}&tbm=nws"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <a href="{google_url}" target="_blank" 
           style="display: block; background: #1e3a5f; color: white; padding: 0.75rem 1rem; border-radius: 8px; text-decoration: none; text-align: center;">
            🔍 Googleで検索
        </a>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <a href="{news_url}" target="_blank" 
           style="display: block; background: #059669; color: white; padding: 0.75rem 1rem; border-radius: 8px; text-decoration: none; text-align: center;">
            📰 ニュース検索
        </a>
        """, unsafe_allow_html=True)
    
    st.caption("※AIの分析で情報が見つからない場合は、上記リンクから直接検索してください")
    
    # 免責事項
    st.divider()
    st.markdown("""
    <div class="warning-card">
        <strong>⚠️ 重要な注意事項</strong><br>
        この結果はAIによる公開情報の分析に基づく参考情報です。
        実際の学校の安全性を保証するものではありません。
        最終的な判断はご自身で行い、必要に応じて学校や教育委員会に直接お問い合わせください。
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
