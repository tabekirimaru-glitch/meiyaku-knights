-- 学校リスク予報 キャッシュテーブル
-- Supabase SQL Editorで実行してください

-- キャッシュテーブル作成
CREATE TABLE IF NOT EXISTS school_risk_cache (
    id SERIAL PRIMARY KEY,
    school_name TEXT NOT NULL,
    prefecture TEXT,
    search_key TEXT UNIQUE NOT NULL,  -- 学校名+都道府県のハッシュ
    ai_result TEXT NOT NULL,          -- AIの分析結果
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 1    -- アクセス回数
);

-- インデックス作成（検索高速化）
CREATE INDEX IF NOT EXISTS idx_school_risk_search_key ON school_risk_cache(search_key);
CREATE INDEX IF NOT EXISTS idx_school_risk_school_name ON school_risk_cache(school_name);

-- RLS（Row Level Security）を有効化
ALTER TABLE school_risk_cache ENABLE ROW LEVEL SECURITY;

-- 公開読み取りポリシー（誰でも読める）
CREATE POLICY "Allow public read" ON school_risk_cache
    FOR SELECT USING (true);

-- サービスキーでのみ書き込み可能
CREATE POLICY "Allow service write" ON school_risk_cache
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow service update" ON school_risk_cache
    FOR UPDATE USING (true);

-- 古いキャッシュを削除する関数（30日以上古いもの）
CREATE OR REPLACE FUNCTION cleanup_old_cache()
RETURNS void AS $$
BEGIN
    DELETE FROM school_risk_cache 
    WHERE updated_at < NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;

-- コメント
COMMENT ON TABLE school_risk_cache IS '学校リスク予報AIの検索結果キャッシュ';
COMMENT ON COLUMN school_risk_cache.search_key IS '学校名+都道府県から生成したユニークキー';
COMMENT ON COLUMN school_risk_cache.ai_result IS 'Gemini AIの分析結果（マークダウン形式）';
COMMENT ON COLUMN school_risk_cache.access_count IS 'このキャッシュが参照された回数';
