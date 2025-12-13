-- ブロックされているユーザー一覧を確認
SELECT * FROM blocked_users;

-- 特定のフィンガープリントのブロックを解除する場合
-- DELETE FROM blocked_users WHERE fingerprint = 'fp_xxxxxx';

-- すべてのブロックを解除する場合（注意して使用）
-- DELETE FROM blocked_users;
