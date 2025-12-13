-- =============================================
-- おすすめコンテンツ v2 - 拡張スキーマ
-- =============================================
-- Supabase SQL Editorで実行してください

-- 既存テーブルを削除して再作成（データがある場合はバックアップ推奨）
DROP TABLE IF EXISTS recommendations_v2;

-- 新しいおすすめコンテンツテーブル
CREATE TABLE recommendations_v2 (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- カテゴリ: book, youtube, music, encouragement
    category TEXT NOT NULL CHECK (category IN ('book', 'youtube', 'music', 'encouragement')),
    
    -- 共通フィールド
    title TEXT NOT NULL,
    url TEXT,
    image_url TEXT,
    description TEXT,
    tags TEXT[] DEFAULT '{}',
    
    -- 本専用
    summary TEXT,                    -- 要約
    target_audience TEXT,            -- どういった人に読んで欲しいか
    
    -- YouTube/音楽専用
    thumbnail_url TEXT,              -- サムネイル（自動取得）
    video_id TEXT,                   -- YouTube動画ID
    
    -- 励まし専用
    message TEXT,                    -- 励ましの言葉
    
    -- 管理
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- インデックス
CREATE INDEX idx_rec_v2_category ON recommendations_v2(category);
CREATE INDEX idx_rec_v2_tags ON recommendations_v2 USING GIN(tags);
CREATE INDEX idx_rec_v2_active ON recommendations_v2(is_active);
CREATE INDEX idx_rec_v2_created ON recommendations_v2(created_at DESC);

-- RLS有効化
ALTER TABLE recommendations_v2 ENABLE ROW LEVEL SECURITY;

-- 誰でも有効なコンテンツを読める
CREATE POLICY "Anyone can read active recommendations_v2" ON recommendations_v2
    FOR SELECT USING (is_active = true);

-- 管理者は全操作可能
CREATE POLICY "Admin can manage recommendations_v2" ON recommendations_v2
    FOR ALL USING (true);

SELECT 'おすすめコンテンツv2テーブル作成完了！' AS message;
