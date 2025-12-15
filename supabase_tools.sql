-- ============================================
-- GASツール配布機能用テーブル
-- ============================================

-- toolsテーブル作成
CREATE TABLE IF NOT EXISTS tools (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,                    -- ツール名（例: 盟約コックピット）
    version TEXT NOT NULL,                 -- バージョン（例: v5.3）
    update_info TEXT,                      -- 更新内容
    code_body TEXT,                        -- GASソースコード全文
    template_url TEXT,                     -- 配布用テンプレートURL
    banner_url TEXT,                       -- バナー画像URL
    is_active BOOLEAN DEFAULT true,        -- 表示/非表示
    display_order INTEGER DEFAULT 0,       -- 表示順
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 匿名ユーザーの読み取り許可（公開ページ用）
ALTER TABLE tools ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access" ON tools
    FOR SELECT USING (is_active = true);

CREATE POLICY "Allow all operations for authenticated users" ON tools
    FOR ALL USING (true);

-- 更新日時の自動更新トリガー
CREATE OR REPLACE FUNCTION update_tools_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tools_updated_at_trigger
    BEFORE UPDATE ON tools
    FOR EACH ROW
    EXECUTE FUNCTION update_tools_updated_at();

-- インデックス
CREATE INDEX IF NOT EXISTS idx_tools_active_order ON tools (is_active, display_order);

-- ============================================
-- 使い方:
-- 1. Supabaseダッシュボード → SQL Editor
-- 2. このスクリプトを貼り付けて実行
-- ============================================
