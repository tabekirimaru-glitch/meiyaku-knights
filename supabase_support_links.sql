-- =============================================
-- 活動支援リンク管理テーブル
-- =============================================
-- Supabase SQL Editorでこのスクリプトを実行してください

-- 支援リンクテーブル
CREATE TABLE IF NOT EXISTS support_links (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    type TEXT NOT NULL,  -- 'twitch', 'ofuse', 'amazon_shop', 'amazon_wishlist', 'tiktok', 'twitcasting', 'twitch_donate', 'youtube'
    title TEXT NOT NULL,
    image_url TEXT,
    link_url TEXT NOT NULL,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS有効化
ALTER TABLE support_links ENABLE ROW LEVEL SECURITY;

-- 誰でも読める
CREATE POLICY "Anyone can read support links" ON support_links
    FOR SELECT USING (is_active = true);

-- 管理者は全操作可能
CREATE POLICY "Admin can manage support links" ON support_links
    FOR ALL USING (true);

-- 初期データ投入（プレースホルダー）
INSERT INTO support_links (type, title, image_url, link_url, display_order) VALUES
('twitch', 'Twitchサブスク支援', 'images/support-twitch.jpg', 'https://www.twitch.tv/meiyaku_knights', 1),
('ofuse', 'OFUSEメッセージ支援', 'images/support-ofuse.jpg', 'https://ofuse.me/meiyaku_knights', 2),
('amazon_shop', 'Amazonお買い物で支援', 'images/support-amazon.jpg', 'https://www.amazon.co.jp/?tag=meiyaku-22', 3),
('amazon_wishlist', 'ほしい物リストから差し入れ', 'images/support-amazon-wishlist.jpg', 'https://www.amazon.co.jp/hz/wishlist/ls/XXXXXXXX', 4),
('tiktok', 'TikTok投げ銭', '', 'https://www.tiktok.com/@meiyaku_knights', 10),
('twitcasting', 'ツイキャス投げ銭', '', 'https://twitcasting.tv/meiyaku_knights', 11),
('twitch_donate', 'Twitch投げ銭', '', 'https://www.twitch.tv/meiyaku_knights', 12),
('youtube', 'YouTube投げ銭', '', 'https://www.youtube.com/@meiyaku_knights', 13);

-- 確認
SELECT 'support_linksテーブル作成完了！' AS message;
