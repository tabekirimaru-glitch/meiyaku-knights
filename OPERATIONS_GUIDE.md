# 片翼の盟約騎士団 ポータルサイト 操作ガイド

このドキュメントはAIアシスタント（Gemini、Claude等）がこのサイトを操作・更新するためのガイドです。

---

## 📁 プロジェクト構造

```
meiyaku-knights-portal/
├── index.html          # トップページ
├── community.html      # コミュニティページ（体験談投稿・閲覧）
├── judgments.html      # 判例データベース
├── child-cases.html    # 子供関連事件アーカイブ
├── media.html          # ユリちゃんの漫画・動画紹介
├── school-risk.html    # 学校リスク予報AI（Streamlitへのリンク）
├── admin.html          # 管理者ページ
├── style.css           # メインスタイルシート
├── script.js           # 共通JavaScript
│
├── data/
│   ├── judgments.json      # 判例データ
│   ├── child-cases.json    # 子供関連事件データ
│   ├── youtube.json        # YouTube動画データ
│   ├── experiences.json    # 体験談データ（現在は空）
│   └── recommendations.json # おすすめコンテンツ
│
├── images/              # 画像ファイル
├── scripts/             # データ収集スクリプト
│   ├── collect_data.py         # 判例データ収集
│   ├── collect_rss_news.py     # ニュース収集
│   └── collect_youtube.py      # YouTube動画収集
│
├── .github/workflows/
│   └── collect-data.yml  # 週1自動データ更新
│
└── streamlit_app.py     # 学校リスク予報AIアプリ
```

---

## 🔧 よくある操作

### 1. コンテンツの追加・編集

#### トップページのセクション編集
```
ファイル: index.html
```
- **セクションヘッダーのスタイル**: `.golden-title` クラスで黄色文字＋赤縁取り
- **背景透明化**: デスクトップ版はCSS内の `@media (min-width: 769px)` で設定

#### コミュニティページの編集
```
ファイル: community.html
```
- **ログインモーダル**: 965行目付近 `id="loginGate"`
- **支援バナー**: 1405行目付近 `class="support-banner-grid"`
- **サブスク説明セクション**: 支援バナーの下

### 2. 画像の追加

1. 画像を `images/` フォルダにコピー
2. HTMLで参照: `<img src="images/ファイル名.jpg">`

### 3. データの更新

#### 判例データ
```
ファイル: data/judgments.json
形式: 配列
項目: title, date, court, url, tags[], summary
```

#### YouTube動画（自動更新：週1回）
```
ファイル: data/youtube.json
形式: 配列
項目: id, title, thumbnail, publishedAt
```

### 4. デプロイ（GitHub Pagesへ反映）

```bash
git add -A
git commit -m "変更内容の説明"
git push origin main
```
※数分後に https://meiyaku-knights.com に反映

---

## 🔑 重要な設定

### Supabase設定
- **URL**: Supabaseダッシュボードで確認
- **テーブル**: posts, blocked_users, recommendations, school_risk_cache

### GitHub Secrets（自動更新用）
- `GEMINI_API_KEY`: 判例収集AI用
- `YOUTUBE_API_KEY`: YouTube動画取得用

### Google認証
- Supabaseの Site URL と Redirect URLs を正しく設定
- ブラウザ互換性: Brave/LINE等のアプリ内ブラウザでは警告表示あり

---

## 📝 よく使うプロンプト例

### セクションの追加
```
community.htmlの「ヒロの活動支援」セクションに、
新しいカードを追加してください。
タイトル: 〇〇
リンク先: https://...
画像: images/xxx.jpg
```

### スタイルの変更
```
index.htmlの「初めての方へ」セクションの
タイトルを大きくして、色を変えてください。
```

### データの手動更新
```
data/judgments.jsonに新しい判例を追加してください：
タイトル: 〇〇
日付: 2024-12-14
裁判所: 東京家庭裁判所
URL: https://...
タグ: 監護権, 面会交流
```

### デプロイ
```
変更をGitHub Pagesにデプロイしてください。
```

---

## ⚠️ 注意事項

1. **本番デプロイ前の確認**: ローカルでHTMLを開いて確認
2. **Supabase Site URL**: ローカルテスト時は変更が必要
3. **画像サイズ**: 大きすぎる画像は最適化を推奨
4. **JSONの編集**: 文法エラーに注意（カンマ、括弧）

---

## 📞 サポート

問題が発生した場合は、以下を確認してください：
- ブラウザのコンソール（F12 → Console）
- GitHubのActionsタブ（自動更新の失敗確認）
- Supabaseダッシュボード（データベースエラー）
