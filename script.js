// ===========================
// スライダー機能
// ===========================
let currentSlideIndex = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

function showSlide(index) {
    // インデックスの範囲チェック
    if (index >= slides.length) {
        currentSlideIndex = 0;
    } else if (index < 0) {
        currentSlideIndex = slides.length - 1;
    } else {
        currentSlideIndex = index;
    }

    // すべてのスライドとドットを非アクティブに
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));

    // 現在のスライドとドットをアクティブに
    slides[currentSlideIndex].classList.add('active');
    dots[currentSlideIndex].classList.add('active');
}

function changeSlide(direction) {
    showSlide(currentSlideIndex + direction);
}

function currentSlide(index) {
    showSlide(index);
}

// 自動スライド（5秒ごと）
setInterval(() => {
    changeSlide(1);
}, 5000);

// ===========================
// 統計カウンターアニメーション
// ===========================
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2秒
        const increment = target / (duration / 16); // 60fps
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current).toLocaleString();
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString();
            }
        };

        updateCounter();
    });
}

// ===========================
// スクロール時のアニメーション
// ===========================
const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');

            // 統計セクションが表示されたらカウンターアニメーション開始
            if (entry.target.classList.contains('stats-section')) {
                animateCounters();
                observer.unobserve(entry.target); // 一度だけ実行
            }
        }
    });
}, observerOptions);

// ===========================
// ページロード時の処理
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    // アニメーション対象の要素を監視
    const cards = document.querySelectorAll('.card');
    const resourceCategories = document.querySelectorAll('.resource-category');
    const statCards = document.querySelectorAll('.stat-card');
    const statsSection = document.querySelector('.stats-section');

    // カードのアニメーション設定
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });

    // リソースカテゴリーのアニメーション設定
    resourceCategories.forEach((category, index) => {
        category.style.opacity = '0';
        category.style.transform = 'translateY(20px)';
        category.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(category);
    });

    // 統計カードのアニメーション設定
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.15}s, transform 0.6s ease ${index * 0.15}s`;
    });

    // 統計セクションを監視
    if (statsSection) {
        observer.observe(statsSection);
    }

    // ヒーローセクションのアニメーション
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        setTimeout(() => {
            heroContent.style.opacity = '0';
            heroContent.style.transform = 'translateY(30px)';
            heroContent.style.transition = 'opacity 1s ease, transform 1s ease';

            setTimeout(() => {
                heroContent.style.opacity = '1';
                heroContent.style.transform = 'translateY(0)';
            }, 100);
        }, 300);
    }
});

// ===========================
// スムーススクロール
// ===========================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');

        // 空のハッシュは除外
        if (href === '#' || href.startsWith('http')) return;

        e.preventDefault();

        const target = document.querySelector(href);
        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ===========================
// ヘッダーのスクロール効果
// ===========================
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.2)';
    } else {
        header.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
    }

    lastScroll = currentScroll;
});

// ===========================
// 外部リンクに target="_blank" を自動付与
// ===========================
document.querySelectorAll('a[href^="http"]').forEach(link => {
    if (!link.hasAttribute('target')) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    }
});

// ===========================
// 「準備中」カードのクリック防止
// ===========================
document.querySelectorAll('.card-coming-soon').forEach(card => {
    card.addEventListener('click', (e) => {
        e.preventDefault();
        alert('この機能は現在準備中です。もうしばらくお待ちください。');
    });
});

// ===========================
// パララックス効果（軽量版）
// ===========================
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const videoOverlay = document.querySelector('.video-overlay');

    if (videoOverlay) {
        const opacity = Math.min(0.8 + (scrolled / 1000), 0.95);
        videoOverlay.style.opacity = opacity;
    }
});

// ===========================
// モバイルメニュー対応（将来用）
// ===========================
// ハンバーガーメニューが追加された場合に使用
const menuToggle = document.getElementById('menuToggle');
const headerNav = document.querySelector('.header-nav');

if (menuToggle && headerNav) {
    menuToggle.addEventListener('click', () => {
        headerNav.classList.toggle('active');
        menuToggle.classList.toggle('active');
    });
}
