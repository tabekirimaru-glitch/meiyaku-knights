console.log('🚀🚀🚀 メインスクリプト開始 v1734137000 🚀🚀🚀');
        // ハンバーガーメニュー
        const hamburger = document.getElementById('hamburger');
        const headerNav = document.getElementById('headerNav');
        const menuOverlay = document.getElementById('menuOverlay');

        if (hamburger && headerNav && menuOverlay) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                headerNav.classList.toggle('active');
                menuOverlay.classList.toggle('active');
            });

            menuOverlay.addEventListener('click', () => {
                hamburger.classList.remove('active');
                headerNav.classList.remove('active');
                menuOverlay.classList.remove('active');
            });

            // メニューリンククリック時に閉じる
            headerNav.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => {
                    hamburger.classList.remove('active');
                    headerNav.classList.remove('active');
                    menuOverlay.classList.remove('active');
                });
            });
        }

        // アコーディオン
        function toggleAccordion(id) {
            document.getElementById(id).classList.toggle('active');
        }

        // 最新判例を表示
        async function loadLatestJudgments() {
            try {
                const response = await fetch('data/judgments.json');
                const data = await response.json();
                const latest = data.slice(-4).reverse();

                const container = document.getElementById('latest-judgments');
                container.innerHTML = latest.map(item => `
                    <div class="judgment-card-mini">
                        <div class="meta">📅 ${item.date} | 🏛️ ${item.court}</div>
                        <h4>${item.title}</h4>
                        <div class="tags">
                            ${item.tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    </div>
                `).join('');
            } catch (e) {
                console.error('判例読み込みエラー:', e);
            }
        }

        loadLatestJudgments();

        // ===== YouTube API Integration (PlaylistItems + Cache) =====
        const YOUTUBE_API_KEY = 'AIzaSyAfWkCf-skC5IGd40KTvf7IVdugt0mHvgU';
        const CHANNEL_HANDLE = '@meiyaku_knights';
        const CACHE_KEY = 'youtube_videos_cache';
        const CACHE_DURATION = 60 * 60 * 1000; // 1時間（ミリ秒）

        console.log('📺 YouTube: スクリプト初期化開始');

        // renderYouTubeVideos を先に定義
        function renderYouTubeVideos(videos) {
            console.log('📺 YouTube: renderYouTubeVideos 呼び出し', videos);
            const container = document.getElementById('youtube-carousel');
            if (!container) {
                console.error('📺 YouTube: youtube-carousel 要素が見つかりません');
                return;
            }
            container.innerHTML = videos.map(video => `
                <a href="https://www.youtube.com/watch?v=${video.id}" target="_blank" class="youtube-video-card">
                    <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
                    <div class="video-info">
                        <div class="video-title">${video.title}</div>
                        <div class="video-date">${new Date(video.publishedAt).toLocaleDateString('ja-JP')}</div>
                    </div>
                </a>
            `).join('');
            console.log('📺 YouTube: レンダリング完了');
        }

        window.loadYouTubeVideos = async function () {
            console.log('📺 YouTube: loadYouTubeVideos 開始');
            const container = document.getElementById('youtube-carousel');

            if (!container) return;

            // まずローカルJSONから読み込み（即時表示優先）
            try {
                const localRes = await fetch('data/youtube.json');
                if (localRes.ok) {
                    const localData = await localRes.json();
                    if (localData && localData.length > 0) {
                        renderYouTubeVideos(localData);
                        console.log('📺 YouTube: ローカルJSONから表示');
                        return;
                    }
                }
            } catch (e) {
                console.log('ローカルJSON読み込み失敗、APIを試行');
            }

            // キャッシュをチェック
            const cached = localStorage.getItem(CACHE_KEY);
            if (cached) {
                const { data, timestamp } = JSON.parse(cached);
                if (Date.now() - timestamp < CACHE_DURATION) {
                    renderYouTubeVideos(data);
                    console.log('📺 YouTube: キャッシュから読み込み');
                    return;
                }
            }

            try {
                // チャンネル情報を取得（forHandleで@ハンドルから検索）
                const channelRes = await fetch(
                    `https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle=${CHANNEL_HANDLE}&key=${YOUTUBE_API_KEY}`
                );
                const channelData = await channelRes.json();

                if (!channelData.items || channelData.items.length === 0) {
                    throw new Error('チャンネルが見つかりません');
                }

                const uploadsPlaylistId = channelData.items[0].contentDetails.relatedPlaylists.uploads;

                // PlaylistItems APIで最新動画を取得（コスト効率良）
                const videosRes = await fetch(
                    `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${uploadsPlaylistId}&maxResults=6&key=${YOUTUBE_API_KEY}`
                );
                const videosData = await videosRes.json();

                if (!videosData.items) {
                    throw new Error('動画が見つかりません');
                }

                const videos = videosData.items.map(item => ({
                    id: item.snippet.resourceId.videoId,
                    title: item.snippet.title,
                    thumbnail: item.snippet.thumbnails.medium?.url || item.snippet.thumbnails.default?.url,
                    publishedAt: item.snippet.publishedAt
                }));

                // キャッシュに保存
                localStorage.setItem(CACHE_KEY, JSON.stringify({
                    data: videos,
                    timestamp: Date.now()
                }));

                console.log('📺 YouTube: APIから取得＆キャッシュ保存');
                renderYouTubeVideos(videos);


            } catch (error) {
                console.error('YouTube API エラー:', error);

                // Fallback to local data
                console.log('Trying local fallback data...');
                try {
                    const fallbackRes = await fetch('data/youtube.json');
                    if (!fallbackRes.ok) throw new Error('Fallback not found');
                    const fallbackData = await fallbackRes.json();
                    renderYouTubeVideos(fallbackData);
                } catch (e2) {
                    container.innerHTML = `
                        <div style="text-align: center; padding: 1rem; color: #666;">
                            <p>動画を読み込めませんでした</p>
                            <a href="https://www.youtube.com/@meiyaku_knights" target="_blank" 
                               style="color: var(--primary-color);">YouTubeで見る →</a>
                        </div>
                    `;
                }
            }
        }


        // ページ読み込み時にキャッシュをクリアして新しく取得
        const oldCache = localStorage.getItem(CACHE_KEY);
        if (oldCache) {
            try {
                const { data } = JSON.parse(oldCache);
                // 空のキャッシュまたは無効なキャッシュがある場合はクリア
                if (!data || data.length === 0) {
                    localStorage.removeItem(CACHE_KEY);
                    console.log('📺 YouTube: 無効なキャッシュをクリア');
                }
            } catch (e) {
                localStorage.removeItem(CACHE_KEY);
            }
        }

        // 動画読み込み実行
        console.log('📍 チェックポイント1: YouTube読み込み前');
        window.loadYouTubeVideos();

        // ===== コミュニティUI JavaScript =====

        // タブ切り替え
        document.querySelectorAll('.community-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                // タブのアクティブ状態を切り替え
                document.querySelectorAll('.community-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // コンテンツの表示切り替え
                const targetTab = tab.dataset.tab;
                document.querySelectorAll('.community-tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                document.getElementById(`community-tab-${targetTab}`).classList.add('active');
            });
        });

        // タグチップの選択
        document.querySelectorAll('.tag-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                chip.classList.toggle('selected');
            });
        });

        // 画像プレビュー
        const imageInput = document.getElementById('image-upload');
        if (imageInput) {
            imageInput.addEventListener('change', function (e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        document.getElementById('image-preview').innerHTML =
                            `<img src="${e.target.result}" alt="プレビュー">`;
                    };
                    reader.readAsDataURL(file);
                }
            });
        }

        // フォーム送信（プレビュー）
        function handleFormSubmit(event) {
            event.preventDefault();

            const handleName = document.getElementById('handle-name').value;
            const prefecture = document.getElementById('prefecture').value;
            const court = document.getElementById('court').value;
            const phase = document.querySelector('input[name="phase"]:checked')?.value || '未選択';
            const experienceText = document.getElementById('experience-text').value;

            // 選択されたタグを収集
            const selectedTags = [];
            document.querySelectorAll('.tag-chip.selected').forEach(chip => {
                selectedTags.push(chip.dataset.tag);
            });

            // カスタムタグを追加
            const customTags = document.getElementById('custom-tags').value;
            if (customTags) {
                customTags.split(',').forEach(tag => {
                    selectedTags.push(tag.trim());
                });
            }

            // プレビュー表示
            alert(`【投稿プレビュー】\n\nハンドルネーム: ${handleName}\n都道府県: ${prefecture}\n裁判所: ${court || '未入力'}\nフェーズ: ${phase}\nタグ: ${selectedTags.join(', ') || 'なし'}\n\n本文:\n${experienceText}\n\n※認証機能実装後に実際の投稿が可能になります`);

            return false;
        }

        // TODO: AIフィルター処理（将来実装）
        console.log('📍 チェックポイント2: Community UI後');
        // function checkCommentWithAI(comment, userId) {
        //     // AIで不適切コメントをチェック
        //     // 3回検知でブロック処理
        //     // const userWarningCount = getUserWarningCount(userId);
        //     // if (isInappropriate && userWarningCount >= 3) {
        //     //     blockUser(userId);
        //     // }
        // }

        // ===== サバイバル・ナビ =====
        console.log('🧭 サバイバルナビ: スクリプト到達');
        var survivalNaviData = null;
        var survivalNaviPath = [];

        // グローバル関数：診断開始
        window.startSurvivalNavi = function () {
            console.log('診断開始ボタンクリック');
            var startArea = document.getElementById('naviStartArea');
            var startBtn = document.getElementById('naviStartBtn');
            var timeline = document.getElementById('naviTimeline');

            // ローディング状態を表示
            startBtn.classList.add('loading');
            startBtn.innerHTML = '⏳ 読み込み中...';

            if (!survivalNaviData) {
                fetch('data/survival-navi.json')
                    .then(function (res) {
                        if (!res.ok) throw new Error('Network error');
                        return res.json();
                    })
                    .then(function (data) {
                        survivalNaviData = data;
                        startArea.style.display = 'none';
                        timeline.style.display = 'block';
                        renderNaviQuestion('Q1');
                    })
                    .catch(function (err) {
                        console.error('データ読み込みエラー:', err);
                        startBtn.classList.remove('loading');
                        startBtn.innerHTML = '❌ 読み込み失敗 - 再試行';
                    });
            } else {
                survivalNaviPath = [];
                startArea.style.display = 'none';
                timeline.style.display = 'block';
                timeline.innerHTML = '';
                renderNaviQuestion('Q1');
            }
        }

        // 質問表示
        function renderNaviQuestion(qId) {
            var timeline = document.getElementById('naviTimeline');
            var q = survivalNaviData.questions[qId];
            if (!q) return;

            var stepIndex = survivalNaviPath.length + 1;
            var stepDiv = document.createElement('div');
            stepDiv.className = 'navi-step';
            stepDiv.dataset.qid = qId;

            var optionsHtml = '';
            for (var i = 0; i < q.options.length; i++) {
                optionsHtml += '<button class="navi-option" data-next="' + q.options[i].next + '" data-index="' + i + '">' + q.options[i].label + '</button>';
            }

            stepDiv.innerHTML = '<div class="navi-question"><span class="q-icon">Q' + stepIndex + '</span>' + q.text + '</div><div class="navi-options">' + optionsHtml + '</div>';

            if (survivalNaviPath.length === 0) {
                timeline.innerHTML = '';
            }
            timeline.appendChild(stepDiv);
            stepDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // 選択肢クリックイベント
            var buttons = stepDiv.querySelectorAll('.navi-option');
            buttons.forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var next = this.dataset.next;
                    var optIndex = this.dataset.index;

                    stepDiv.querySelectorAll('.navi-option').forEach(function (b) { b.classList.remove('selected'); });
                    this.classList.add('selected');
                    stepDiv.classList.add('answered');

                    survivalNaviPath.push({ qId: qId, optIndex: optIndex, next: next });

                    if (next.startsWith('End_')) {
                        renderNaviResult(next);
                    } else {
                        renderNaviQuestion(next);
                    }
                });
            });
        }

        // 診断結果表示
        function renderNaviResult(resultId) {
            var timeline = document.getElementById('naviTimeline');
            var result = survivalNaviData.results[resultId];
            if (!result) return;

            var videosHtml = '';
            for (var i = 0; i < result.videos.length; i++) {
                var v = result.videos[i];
                videosHtml += '<a href="' + v.url + '" target="_blank" class="navi-video-card"><div class="play-icon">▶</div><div class="video-title">' + v.title + '</div></a>';
            }

            var toolsHtml = '';
            if (result.tools.indexOf('judgments') !== -1) {
                toolsHtml += '<a href="judgments.html" class="navi-tool-btn judgments">📚 判例DBを見る</a>';
            }
            if (result.tools.indexOf('community') !== -1) {
                toolsHtml += '<a href="community.html" class="navi-tool-btn community">👥 コミュニティへ</a>';
            }

            var resultDiv = document.createElement('div');
            resultDiv.className = 'navi-result';
            resultDiv.innerHTML = '<div class="navi-result-header ' + result.phaseLevel + '"><h3>🔬 AI診断レポート</h3><div class="phase-label">現在のフェーズ: <strong>' + result.phase + '</strong></div></div><div class="navi-result-body"><div class="navi-advice">' + result.advice + '</div><div class="navi-videos"><h4>📺 今見るべき動画</h4>' + videosHtml + '</div><div class="navi-tools">' + toolsHtml + '</div><a href="' + survivalNaviData.marshmallowUrl + '" target="_blank" class="navi-marshmallow">✉️ 誰にも頼れない時はヒロに相談（マシュマロ）</a><div class="navi-footer-note">⚠️ 情報は常にアップデートされます。必ずYouTubeチャンネルで最新情報をチェックしてください</div></div>';

            timeline.appendChild(resultDiv);

            // リスタートボタン
            var restartBtn = document.createElement('div');
            restartBtn.className = 'navi-restart';
            restartBtn.textContent = '🔄 最初からやり直す';
            restartBtn.addEventListener('click', function () {
                survivalNaviPath = [];
                timeline.innerHTML = '';
                renderNaviQuestion('Q1');
            });
            timeline.appendChild(restartBtn);
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    
