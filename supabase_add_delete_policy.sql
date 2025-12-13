-- =============================================
-- 削除・ブロック解除用のRLSポリシー追加
-- =============================================
-- このSQLをSupabaseのSQL Editorで実行してください

-- 投稿の削除ポリシー
CREATE POLICY "Admin can delete posts" ON posts
    FOR DELETE USING (true);

-- ブロックユーザーの削除ポリシー（ブロック解除用）
CREATE POLICY "Admin can delete blocked users" ON blocked_users
    FOR DELETE USING (true);

-- ステータスに 'flagged' を追加するため、既存のチェック制約を変更
ALTER TABLE posts DROP CONSTRAINT IF EXISTS posts_status_check;
ALTER TABLE posts ADD CONSTRAINT posts_status_check 
    CHECK (status IN ('pending', 'approved', 'rejected', 'flagged'));

-- 完了メッセージ
SELECT '削除・ブロック解除ポリシーを追加しました！' AS message;
