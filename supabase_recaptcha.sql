-- =============================================
-- reCAPTCHA v3 対応 - postsテーブル拡張
-- =============================================
-- Supabase SQL Editorで実行してください

-- recaptcha_token カラムを追加（既にある場合はスキップ）
ALTER TABLE posts ADD COLUMN IF NOT EXISTS recaptcha_token TEXT;

SELECT 'reCAPTCHA token カラム追加完了！' AS message;
