-- =============================================
-- 予約投稿機能追加（media_setsテーブルに追加）
-- =============================================
-- Supabase SQL Editorで実行してください

-- publish_at カラムがなければ追加
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'media_sets' AND column_name = 'publish_at'
    ) THEN
        ALTER TABLE media_sets ADD COLUMN publish_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
    END IF;
END $$;

-- 既存データにpublish_atを設定（NULLの場合は即時公開として現在時刻を設定）
UPDATE media_sets SET publish_at = NOW() WHERE publish_at IS NULL;

-- インデックス追加
CREATE INDEX IF NOT EXISTS idx_media_sets_publish ON media_sets(publish_at);

-- RLSポリシーの更新（公開日時を過ぎたものだけ表示）
DROP POLICY IF EXISTS "Anyone can read active media_sets" ON media_sets;
CREATE POLICY "Anyone can read published media_sets" ON media_sets
    FOR SELECT USING (is_active = true AND publish_at <= NOW());

SELECT '予約投稿機能追加完了！' AS message;
