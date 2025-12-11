"""
学校リスク予報AI - Streamlit App
AIが学校の安全性とリスク管理体制を分析します
"""

import streamlit as st
import json
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="学校リスク予報AI",
    page_icon="🏫",
    layout="centered"
)

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
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        padding: 1rem;
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

# 検索実行
if search_button and school_name:
    with st.spinner("AIが情報を収集・分析中..."):
        import time
        time.sleep(2)  # デモ用の遅延
    
    # デモ用の結果表示
    st.success(f"「{school_name}」の分析が完了しました")
    
    # リスクスコア（デモ）
    import random
    risk_score = random.randint(30, 85)
    
    if risk_score < 40:
        risk_class = "risk-low"
        risk_label = "低リスク"
        risk_emoji = "✅"
    elif risk_score < 65:
        risk_class = "risk-medium"
        risk_label = "中リスク"
        risk_emoji = "⚠️"
    else:
        risk_class = "risk-high"
        risk_label = "高リスク"
        risk_emoji = "🚨"
    
    st.markdown(f"""
    <div class="risk-score {risk_class}">
        {risk_emoji} リスクスコア: {risk_score}/100<br>
        <span style="font-size: 1.2rem;">{risk_label}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 分析結果
    st.subheader("📊 分析結果")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("過去の事件・事故", f"{random.randint(0, 5)}件", "直近5年")
    with col2:
        st.metric("口コミ評価", f"{random.uniform(2.5, 4.5):.1f}/5.0", "Google評価")
    with col3:
        st.metric("不審者情報", f"{random.randint(0, 10)}件", "周辺500m")
    
    # 詳細情報
    st.subheader("📋 詳細情報")
    
    with st.expander("🔍 発見された関連ニュース", expanded=True):
        st.markdown("""
        <div class="info-card">
            <strong>※デモ表示</strong><br>
            実際の運用時は、AIがニュース記事やSNS投稿から
            学校に関連する情報を自動収集・分析します。
        </div>
        """, unsafe_allow_html=True)
        st.info("この機能は現在開発中です。実際のニュース検索はまもなく実装予定。")
    
    with st.expander("⚠️ リスク要因"):
        st.markdown("""
        - 過去の報道事例の有無
        - 学校の対応・情報公開度
        - 地域の治安情報
        - 保護者からの口コミ
        """)
    
    with st.expander("✅ ポジティブ要因"):
        st.markdown("""
        - セキュリティ設備の充実度
        - 地域との連携活動
        - 安全対策の取り組み
        """)
    
    # 免責事項
    st.divider()
    st.markdown("""
    <div class="warning-card">
        <strong>⚠️ ご注意</strong><br>
        この結果はAIによる自動生成であり、参考情報です。
        最終的な判断はご自身で行い、必要に応じて学校や自治体に直接お問い合わせください。
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
