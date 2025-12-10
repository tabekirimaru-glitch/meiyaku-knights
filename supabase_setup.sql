-- =============================================
-- 投稿管理システム: Supabase テーブル作成SQL
-- =============================================
-- 使い方:
-- 1. Supabaseダッシュボードにログイン
-- 2. 左メニュー「SQL Editor」をクリック
-- 3. このSQLをコピー&ペースト
-- 4. 「Run」ボタンを押す
-- =============================================

-- 投稿テーブル
CREATE TABLE IF NOT EXISTS posts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    author_name TEXT NOT NULL,
    prefecture TEXT,
    phase TEXT,
    content TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    user_fingerprint TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ブロックユーザーテーブル
CREATE TABLE IF NOT EXISTS blocked_users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    fingerprint TEXT NOT NULL UNIQUE,
    reason TEXT,
    blocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security (RLS) を有効化
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE blocked_users ENABLE ROW LEVEL SECURITY;

-- ポリシー: 誰でも投稿を作成できる（INSERT）
CREATE POLICY "Anyone can insert posts" ON posts
    FOR INSERT WITH CHECK (true);

-- ポリシー: 承認済みの投稿のみ誰でも読める
CREATE POLICY "Anyone can read approved posts" ON posts
    FOR SELECT USING (status = 'approved');

-- ポリシー: 管理者は全ての投稿を読める（anon keyでも一時的に許可）
-- 本番環境ではservice_roleキーを使うか、認証を実装することを推奨
CREATE POLICY "Admin can read all posts" ON posts
    FOR SELECT USING (true);

-- ポリシー: 管理者は投稿を更新できる
CREATE POLICY "Admin can update posts" ON posts
    FOR UPDATE USING (true);

-- ポリシー: 誰でもブロックリストを読める（投稿前チェック用）
CREATE POLICY "Anyone can read blocked users" ON blocked_users
    FOR SELECT USING (true);

-- ポリシー: 管理者はブロックユーザーを追加できる
CREATE POLICY "Admin can insert blocked users" ON blocked_users
    FOR INSERT WITH CHECK (true);

-- インデックス（パフォーマンス向上）
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_blocked_fingerprint ON blocked_users(fingerprint);

-- 完了メッセージ
SELECT 'テーブル作成完了！' AS message;
