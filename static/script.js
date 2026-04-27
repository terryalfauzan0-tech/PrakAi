document.addEventListener('DOMContentLoaded', () => {
    const analyzeForm = document.getElementById('analyze-form');
    const tiktokUrlInput = document.getElementById('tiktok-url');
    const analyzeBtn = document.getElementById('analyze-btn');
    const errorMessage = document.getElementById('error-message');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const themeToggle = document.getElementById('theme-toggle');
    const resetBtn = document.getElementById('reset-btn');

    // Stats elements
    const statComments = document.getElementById('stat-comments');
    const statBuyers = document.getElementById('stat-buyers');
    const statProduction = document.getElementById('stat-production');
    const recText = document.getElementById('rec-text');
    const keywordList = document.getElementById('keyword-list');
    const commentsList = document.getElementById('comments-list');

    let sentimentChart = null;
    let allComments = [];

    // Dark Mode Toggle
    themeToggle.addEventListener('click', () => {
        const body = document.body;
        const icon = themeToggle.querySelector('i');
        
        if (body.getAttribute('data-theme') === 'dark') {
            body.removeAttribute('data-theme');
            icon.classList.replace('fa-sun', 'fa-moon');
        } else {
            body.setAttribute('data-theme', 'dark');
            icon.classList.replace('fa-moon', 'fa-sun');
        }
    });

    // Form Submission
    analyzeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = tiktokUrlInput.value.trim();

        if (!url) {
            showError("Silakan masukkan link TikTok yang valid.");
            return;
        }

        // Reset UI
        hideError();
        results.classList.add('hidden');
        loading.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (response.ok) {
                renderResults(data.data);
            } else {
                showError(data.detail || "Terjadi kesalahan saat menganalisis.");
            }
        } catch (error) {
            showError("Gagal terhubung ke server. Pastikan backend berjalan.");
            console.error(error);
        } finally {
            loading.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    function renderResults(data) {
        results.classList.remove('hidden');
        
        // Update Stats
        statComments.textContent = formatNumber(data.analytics.total);
        statBuyers.textContent = formatNumber(data.business_estimate.estimated_buyers);
        statProduction.textContent = formatNumber(data.business_estimate.production_recommendation);
        
        // Recommendations & Insights
        recText.textContent = data.smart_recommendation;

        // Keywords
        keywordList.innerHTML = '';
        data.keyword_insight.forEach(kw => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = kw;
            keywordList.appendChild(tag);
        });

        // Sentiment Chart
        renderChart(data.analytics.categories);

        // Comments
        allComments = data.comments;
        renderComments(allComments);
    }

    function renderChart(categories) {
        const ctx = document.getElementById('sentimentPieChart').getContext('2d');
        
        if (sentimentChart) {
            sentimentChart.destroy();
        }

        const labels = Object.keys(categories);
        const values = Object.values(categories);
        
        const colors = [
            '#10b981', // Success (Ingin Beli)
            '#3b82f6', // Info (Tidak Beli)
            '#ef4444', // Danger (Negatif)
            '#f59e0b'  // Warning (Pertanyaan)
        ];

        sentimentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors,
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: getComputedStyle(document.body).getPropertyValue('--text-main'),
                            padding: 20,
                            font: { size: 12 }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }

    function renderComments(comments) {
        commentsList.innerHTML = '';
        
        if (comments.length === 0) {
            commentsList.innerHTML = '<p style="text-align:center; color:var(--text-muted);">Tidak ada komentar yang ditemukan.</p>';
            return;
        }

        comments.forEach((c, index) => {
            if (index >= 200) return; // Limit UI rendering for performance
            const div = document.createElement('div');
            const catClass = c.category.toLowerCase().replace(/\s+/g, '-');
            div.className = `comment-item cat-${catClass}`;
            
            div.innerHTML = `
                <div class="comment-text">${c.text}</div>
                <div class="comment-meta">
                    <span class="badge ${getBadgeClass(c.category)}">${c.category}</span>
                    <span class="confidence-score">Confidence: ${c.confidence}%</span>
                </div>
            `;
            commentsList.appendChild(div);
        });
        
        if (comments.length > 200) {
            const more = document.createElement('p');
            more.style.textAlign = 'center';
            more.style.color = 'var(--text-muted)';
            more.style.padding = '1rem';
            more.textContent = `... dan ${comments.length - 200} komentar lainnya dianalisis di sistem.`;
            commentsList.appendChild(more);
        }
    }

    function getBadgeClass(cat) {
        if (cat === 'Positif Ingin Beli') return 'badge-success';
        if (cat === 'Positif Tidak Beli') return 'badge-info';
        if (cat === 'Negatif') return 'badge-danger';
        return 'badge-warning';
    }

    // Filtering
    document.querySelector('.filters').addEventListener('click', (e) => {
        if (!e.target.classList.contains('badge')) return;

        document.querySelectorAll('.filters .badge').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');

        const filter = e.target.textContent;
        if (filter === 'Semua') {
            renderComments(allComments);
        } else {
            const filtered = allComments.filter(c => c.category.includes(filter));
            renderComments(filtered);
        }
    });

    // Helpers
    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.style.opacity = '1';
    }

    function hideError() {
        errorMessage.textContent = '';
        errorMessage.style.opacity = '0';
    }

    function formatNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }

    resetBtn.addEventListener('click', () => {
        results.classList.add('hidden');
        tiktokUrlInput.value = '';
        tiktokUrlInput.focus();
    });
});
