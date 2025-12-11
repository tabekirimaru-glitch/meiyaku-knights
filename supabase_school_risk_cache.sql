-- 学校リスク予報 キャッシュテーブル（v2: 検索結果保存対応）
-- Supabase SQL Editorで実行してください

-- 既存テーブルがある場合は削除（初回のみ）
-- DROP TABLE IF EXISTS school_risk_cache;

-- キャッシュテーブル作成
CREATE TABLE IF NOT EXISTS school_risk_cache (
    id SERIAL PRIMARY KEY,
    school_name TEXT NOT NULL,
    prefecture TEXT,
    search_key TEXT UNIQUE NOT NULL,
    ai_result TEXT NOT NULL,
    search_results TEXT,  -- Google検索結果HTML
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 1
);

-- インデックス
CREATE INDEX IF NOT EXISTS idx_school_risk_search_key ON school_risk_cache(search_key);

-- RLS有効化
ALTER TABLE school_risk_cache ENABLE ROW LEVEL SECURITY;

-- 全操作許可（公開API用）
DROP POLICY IF EXISTS "Allow all operations" ON school_risk_cache;
CREATE POLICY "Allow all operations" ON school_risk_cache FOR ALL USING (true);

-- search_results カラムがない場合は追加
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'school_risk_cache' AND column_name = 'search_results'
    ) THEN
        ALTER TABLE school_risk_cache ADD COLUMN search_results TEXT;
    END IF;
END $$;
