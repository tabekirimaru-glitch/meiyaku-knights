-- =============================================
-- メディアセット管理用テーブル（漫画+ショート+ロング動画を1セットで管理）
-- =============================================
-- 使い方: SupabaseのSQL Editorで実行

-- メディアセットテーブル
CREATE TABLE IF NOT EXISTS media_sets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,                    -- セット名（例：「連れ去り解説 第1話」）
    manga_image_url TEXT,                   -- 漫画バナー画像URL
    short_video_url TEXT,                   -- ショート動画URL（タップで即再生）
    long_video_url TEXT,                    -- ロング動画URL（詳細リンク）
    display_order INT DEFAULT 0,            -- 表示順
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS有効化
ALTER TABLE media_sets ENABLE ROW LEVEL SECURITY;

-- ポリシー: 誰でもアクティブなセットを読める
CREATE POLICY "Anyone can read active media_sets" ON media_sets
    FOR SELECT USING (is_active = true);

-- ポリシー: 管理者は全て読める
CREATE POLICY "Admin can read all media_sets" ON media_sets
    FOR SELECT USING (true);

-- ポリシー: 管理者は追加・更新・削除できる
CREATE POLICY "Admin can insert media_sets" ON media_sets
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Admin can update media_sets" ON media_sets
    FOR UPDATE USING (true);

CREATE POLICY "Admin can delete media_sets" ON media_sets
    FOR DELETE USING (true);

-- インデックス
CREATE INDEX IF NOT EXISTS idx_media_sets_order ON media_sets(display_order);
CREATE INDEX IF NOT EXISTS idx_media_sets_active ON media_sets(is_active);

SELECT 'メディアセットテーブル作成完了！' AS message;
