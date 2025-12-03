# 片翼の盟約騎士団 トップページ - 使用方法ガイド

## 📁 ファイル構成

```
meiyaku-knights-portal/
├── index.html       (メインHTML)
├── style.css        (スタイルシート)
└── script.js        (JavaScript)
```

---

## 🚀 使用方法

### 方法1：ローカルで確認（推奨）

1. **ブラウザで開く**
   - `index.html` をダブルクリック
   - または右クリック → 「プログラムから開く」→ ブラウザを選択

2. **スマホ表示の確認**
   - ブラウザのデベロッパーツールを開く（F12キー）
   - デバイスツールバーを表示（Ctrl + Shift + M）
   - iPhone や Android などのプリセットを選択

### 方法2：WordPressへの統合

#### オプションA：固定ページとして追加

1. **WordPress管理画面にログイン**
   - `https://www.meiyaku-knights.jp/wp-admin/`

2. **新規固定ページ作成**
   - 「固定ページ」 → 「新規追加」
   - タイトル: 「ホーム」または「トップページ」

3. **HTMLをコピペ**
   - エディターを「テキストエディター」または「コードエディター」に切り替え
   - `index.html` の `<body>` タグ内のコンテンツをコピー
   - WordPressに貼り付け

4. **CSSを追加**
   - 「外観」 → 「カスタマイズ」 → 「追加CSS」
   - `style.css` の内容をすべてコピペ

5. **JavaScriptを追加**
   - プラグイン「Simple Custom CSS and JS」などをインストール
   - または子テーマの `footer.php` に以下を追加：
   ```html
   <script>
   // script.js の内容をここにコピペ
   </script>
   ```

6. **トップページに設定**
   - 「設定」 → 「表示設定」
   - 「ホームページの表示」を「固定ページ」に変更
   - 作成したページを選択

#### オプションB：カスタムテンプレートとして追加

1. **ファイルマネージャーにアクセス**
   - ConoHa WING管理画面
   - 「サイト管理」 → 「ファイルマネージャー」

2. **子テーマフォルダに移動**
   - `public_html/` → `wp-content/` → `themes/` → `[使用中のテーマ]-child/`
   - 子テーマがない場合は作成が必要

3. **ファイルをアップロード**
   - `front-page.php` として `index.html` の内容を保存
   - `style.css` の内容を子テーマの `style.css` に追記
   - `script.js` を子テーマフォルダにアップロード

4. **functions.php で JavaScript を読み込み**
   ```php
   function enqueue_custom_scripts() {
       wp_enqueue_script('custom-script', get_stylesheet_directory_uri() . '/script.js', array(), '1.0', true);
   }
   add_action('wp_enqueue_scripts', 'enqueue_custom_scripts');
   ```

---

## 🎨 カスタマイズ方法

### 色の変更

`style.css` の `:root` セクションを編集：

```css
:root {
    --primary-color: #1e3a8a;    /* メインカラー */
    --secondary-color: #f59e0b;  /* アクセントカラー */
    --accent-color: #06b6d4;     /* 強調カラー */
}
```

### リンクの追加・変更

`index.html` のリンク部分を編集：

```html
<a href="あなたのURL" target="_blank" class="btn btn-primary">
    ボタンテキスト
</a>
```

### カードの追加

`.cards-grid` セクションに新しいカードを追加：

```html
<a href="リンク先" class="card">
    <div class="card-icon">🎯</div>
    <h3 class="card-title">タイトル</h3>
    <p class="card-description">説明文</p>
    <div class="card-tags">
        <span class="tag">タグ1</span>
    </div>
</a>
```

---

## 📱 スマホ対応の特徴

### 設計のポイント

- **大きなタップ領域**：最低44×44pxのボタンサイズ
- **読みやすいフォント**：本文16px以上
- **シンプルなナビゲーション**：階層を浅く
- **カード型レイアウト**：タップしやすいデザイン
- **レスポンシブグリッド**：画面サイズに自動調整

### 対応ブレークポイント

- **デスクトップ**：1200px以上
- **タブレット**：768px〜1199px
- **スマホ**：480px〜767px
- **小型スマホ**：479px以下

---

## ✨ 主な機能

### インタラクティブ要素

- **スムーススクロール**：ページ内リンクで滑らかにスクロール
- **フェードインアニメーション**：スクロールで要素が表示
- **ホバーエフェクト**：カードが浮き上がる
- **ヘッダー固定**：スクロールしてもヘッダーが表示

### SEO対応

- メタディスクリプション設定済み
- セマンティックHTML使用
- 適切な見出し構造（h1〜h4）

---

## 🔧 トラブルシューティング

### CSSが反映されない

1. ブラウザキャッシュをクリア（Ctrl + F5）
2. `style.css` のパスが正しいか確認
3. WordPressの場合、追加CSSに貼り付けたか確認

### JavaScriptが動作しない

1. ブラウザのコンソールでエラーを確認（F12 → Console）
2. `script.js` のパスが正しいか確認
3. jQuery競合の可能性（WordPressプラグインなど）

### スマホ表示が崩れる

1. `viewport` メタタグが設定されているか確認
2. max-width を使用して画像がはみ出ないようにする
3. デベロッパーツールでモバイル表示を確認

---

## 📝 次のステップ

### 完成させるべき項目

- [ ] リソースセクションのリンクを実際のURLに変更
- [ ] 判決データベースページの作成
- [ ] お問い合わせフォームの追加
- [ ] プライバシーポリシーページの作成
- [ ] Googleアナリティクスの設定

### 将来追加する機能

- [ ] AIチャットボット統合
- [ ] Googleマップ連携
- [ ] コミュニティ投稿フォーム
- [ ] 検索機能の強化

---

## 📞 サポート

このガイドで不明な点があれば、いつでもお知らせください！
