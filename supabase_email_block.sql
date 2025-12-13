-- =============================================
-- ブロック機能拡張: メールアドレスベースのブロック追加
-- =============================================
-- 使い方:
-- 1. Supabaseダッシュボードにログイン
-- 2. 左メニュー「SQL Editor」をクリック
-- 3. このSQLをコピー&ペースト
-- 4. 「Run」ボタンを押す
-- =============================================

-- blocked_users テーブルに blocked_email カラムを追加
ALTER TABLE blocked_users ADD COLUMN IF NOT EXISTS blocked_email TEXT;

-- blocked_email にインデックスを追加（検索高速化）
CREATE INDEX IF NOT EXISTS idx_blocked_email ON blocked_users(blocked_email);

-- ユニーク制約を変更（fingerprint OR email のどちらかでブロック可能に）
-- 既存のユニーク制約を削除（存在する場合）
ALTER TABLE blocked_users DROP CONSTRAINT IF EXISTS blocked_users_fingerprint_key;

-- fingerprint はNULLを許可するように変更
ALTER TABLE blocked_users ALTER COLUMN fingerprint DROP NOT NULL;

-- posts テーブルに user_email カラムを追加（投稿者のメールを保存）
ALTER TABLE posts ADD COLUMN IF NOT EXISTS user_email TEXT;

-- 完了メッセージ
SELECT 'メールベースブロック機能の拡張が完了しました！' AS message;
