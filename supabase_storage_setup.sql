-- =============================================
-- Supabase Storage バケット設定
-- =============================================
-- ⚠️ このSQLでは Storage バケットは作成できません！
-- 以下の手順で Supabase Dashboard から作成してください：
--
-- 1. Supabase Dashboard にログイン
-- 2. 左メニュー「Storage」をクリック
-- 3. 「New bucket」ボタンをクリック
-- 4. 以下の設定で作成：
--    - Name: media-images
--    - Public bucket: ✅ ON（チェックを入れる）
-- 5. 「Create bucket」をクリック
--
-- 作成後、以下のSQLを実行してアップロードを許可：
-- =============================================

-- Storage ポリシー: 誰でもアップロード可能
CREATE POLICY "Anyone can upload media images"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'media-images');

-- Storage ポリシー: 誰でも閲覧可能
CREATE POLICY "Anyone can view media images"
ON storage.objects FOR SELECT
USING (bucket_id = 'media-images');

-- Storage ポリシー: 削除も許可（管理用）
CREATE POLICY "Anyone can delete media images"
ON storage.objects FOR DELETE
USING (bucket_id = 'media-images');

SELECT 'Storage ポリシー設定完了！' AS message;
