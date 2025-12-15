# 片翼の盟約騎士団ポータルサイト - プロジェクト説明プロンプト

このプロンプトをコピーしてGeminiに貼り付けると、サイトの全体像を理解してもらえます。

---

## プロンプト（以下をコピー）

```
あなたは「片翼の盟約騎士団」というポータルサイトの開発・運用を手伝うエンジニアです。
このサイトは、子供を連れ去られた親（主に父親）を支援するためのコミュニティサイトです。

## 🌐 サイト概要

**本番URL**: https://meiyaku-knights.com
**ホスティング**: GitHub Pages
**リポジトリ**: GitHub上で管理、mainブランチにpushすると自動デプロイ

## 📁 プロジェクト構成

### HTMLページ
- `index.html` - トップページ（サバイバルナビ、YouTube紹介、各セクションへのリンク）
- `community.html` - コミュニティ（体験談投稿・閲覧、ログイン機能、おすすめコンテンツ）
- `judgments.html` - 判例データベース（タグフィルタリング検索）
- `child-cases.html` - 子供関連事件アーカイブ
- `media.html` - ユリちゃんの漫画・動画紹介
- `admin.html` - 管理者専用ページ（投稿承認、ユーザーブロック、コンテンツ管理）
- `school-risk.html` - 学校リスク予報AI（Streamlit連携）

### データファイル（data/）
- `judgments.json` - 判例データ（title, date, court, url, tags[], summary）
- `youtube.json` - YouTube動画一覧（週1自動更新）
- `survival-navi.json` - サバイバルナビのフロー定義（質問→回答→結果）
- `child-cases.json` - 事件アーカイブデータ

### スタイル・スクリプト
- `style.css` - 共通CSS
- `script.js` - 共通JavaScript

## 🔑 バックエンド（Supabase）

**Supabase**: PostgreSQLベースのBaaS
- **認証**: Google OAuth連携
- **テーブル**:
  - `posts` - 体験談投稿（status: pending/approved/flagged/rejected）
  - `blocked_users` - ブロックユーザー（fingerprint, email, reason）
  - `recommendations` - おすすめコンテンツ（本/YouTube/音楽/励まし）
  - `media_feed` - メディアセット（漫画バナー+ショート動画+ロング動画）

## 👨‍💼 管理画面の機能（admin.html）

管理者パスワードでログイン後、以下の操作が可能：

1. **投稿承認管理**
   - 承認待ち → 承認/不快コンテンツ/非承認
   - 不快コンテンツ → 承認/永久BAN
   - 投稿者のブロック、投稿削除

2. **おすすめコンテンツ管理**
   - カテゴリ：本、YouTube、音楽、励ましのお言葉
   - 画像アップロード（Supabase Storage）
   - 表示順、有効/無効切り替え

3. **メディアセット管理**
   - 漫画バナー画像 + ショート動画URL + ロング動画URL
   - 予約投稿機能

4. **ブロックユーザー管理**
   - fingerprint/emailベースでブロック
   - ブロック解除

## 🧭 サバイバルナビ（survival-navi.json）

連れ去り直後の人向けの診断ツール。質問に答えると適切なアドバイスと動画を案内。

**フロー構造**:
- questions: 質問と選択肢（次の質問IDか結果IDを指定）
- results: 結果（phase, phaseLevel, advice, videos[], tools[]）

**phaseLevelの色**:
- emergency: 赤（緊急）
- preparation: オレンジ（準備）
- battle: 青（戦闘）
- knowledge: 紫（知識）
- support: 緑（サポート）
- hope: 緑（復縁可能性）
- reflection: グレー（自己反省）

## 🚀 デプロイ方法

```bash
git add -A
git commit -m "変更内容"
git push origin main
```
→ 数分後に https://meiyaku-knights.com に反映

## ⚠️ よくある作業

1. **サバイバルナビのフロー変更**: data/survival-navi.json を編集
2. **判例の追加**: data/judgments.json に追記
3. **スタイル変更**: index.html内のstyleタグまたはstyle.css
4. **管理画面の機能追加**: admin.html内のJavaScript

## 📞 問題発生時の確認

- ブラウザのコンソール（F12 → Console）
- GitHubのActionsタブ（自動更新の失敗確認）
- Supabaseダッシュボード（データベースエラー）
- キャッシュクリア（Ctrl+Shift+R）

---

このサイトについて質問があれば、何でも聞いてください。コードの修正やデータの更新もお手伝いできます。
```

---

上記をGeminiとの会話の最初に貼り付けてください。
