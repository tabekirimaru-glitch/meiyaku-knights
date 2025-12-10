-- =============================================
-- おすすめコンテンツ管理用テーブル
-- =============================================
-- 使い方: SupabaseのSQL Editorで実行

-- おすすめコンテンツテーブル
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    category TEXT NOT NULL CHECK (category IN ('book', 'youtube', 'music', 'quote')),
    title TEXT NOT NULL,
    author TEXT,           -- 著者、チャンネル名、アーティスト名など
    url TEXT,              -- リンク（本のAmazonリンク、YouTubeリンクなど）
    description TEXT,      -- 説明・コメント
    image_url TEXT,        -- サムネイル画像（任意）
    display_order INT DEFAULT 0,  -- 表示順
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS有効化
ALTER TABLE recommendations ENABLE ROW LEVEL SECURITY;

-- ポリシー: 誰でもアクティブなおすすめを読める
CREATE POLICY "Anyone can read active recommendations" ON recommendations
    FOR SELECT USING (is_active = true);

-- ポリシー: 管理者は全て読める
CREATE POLICY "Admin can read all recommendations" ON recommendations
    FOR SELECT USING (true);

-- ポリシー: 管理者は追加・更新・削除できる
CREATE POLICY "Admin can insert recommendations" ON recommendations
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Admin can update recommendations" ON recommendations
    FOR UPDATE USING (true);

CREATE POLICY "Admin can delete recommendations" ON recommendations
    FOR DELETE USING (true);

-- インデックス
CREATE INDEX IF NOT EXISTS idx_recommendations_category ON recommendations(category);
CREATE INDEX IF NOT EXISTS idx_recommendations_order ON recommendations(display_order);

-- サンプルデータ（任意）
INSERT INTO recommendations (category, title, author, url, description) VALUES
('book', '離婚調停・裁判 マニュアル', '森 公任', 'https://amazon.co.jp', '離婚手続きの基本がわかる一冊'),
('youtube', '離婚弁護士チャンネル', '弁護士法人XX', 'https://youtube.com/@example', '離婚問題の法律解説'),
('music', '負けないで', 'ZARD', null, '辛い時に聴くと元気が出る名曲'),
('quote', '明けない夜はない', 'シェイクスピア', null, '困難な状況でも希望を持ち続けよう');

SELECT 'おすすめテーブル作成完了！' AS message;
