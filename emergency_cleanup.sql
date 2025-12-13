-- =============================================
-- 緊急: 投稿とブロックを削除するSQL
-- =============================================
-- Supabase SQL Editorでこれを実行してください

-- 1. 現在の投稿を確認
SELECT id, title, author_name, status, created_at FROM posts;

-- 2. すべての投稿を削除（コメント解除して実行）
DELETE FROM posts;

-- 3. ブロックユーザーも全削除（コメント解除して実行）
DELETE FROM blocked_users;

-- 確認
SELECT 'すべての投稿とブロックを削除しました！' AS message;
