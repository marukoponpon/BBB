// JavaScript for ShindanMaker App

document.addEventListener('DOMContentLoaded', () => {
    // 1. Copy to Clipboard Functionality
    const copyBtn = document.getElementById('copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const textToCopy = copyBtn.getAttribute('data-clipboard-text');
            
            // クリップボードAPIを使用してコピー
            navigator.clipboard.writeText(textToCopy).then(() => {
                // コピー成功時のUIフィードバック
                const originalText = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fa-solid fa-check text-success"></i> コピーしました！';
                copyBtn.classList.add('btn-success-temporary');
                
                // 2秒後に元に戻す
                setTimeout(() => {
                    copyBtn.innerHTML = originalText;
                    copyBtn.classList.remove('btn-success-temporary');
                }, 2000);
            }).catch(err => {
                console.error('コピーに失敗しました:', err);
                alert('コピーに失敗しました。お手数ですが、テキストを選択して直接コピーしてください。');
            });
        });
    }

    // 2. X (Twitter) Share Functionality
    const shareXBtn = document.getElementById('share-x-btn');
    if (shareXBtn) {
        shareXBtn.addEventListener('click', () => {
            const title = shareXBtn.getAttribute('data-title');
            const name = shareXBtn.getAttribute('data-name');
            const result = shareXBtn.getAttribute('data-result');
            
            // ポストテキストの作成
            const postText = `【${title}】\n${result}\n\n`;
            // 現在のページのURL（診断結果のパーマリンク）
            const pageUrl = window.location.href;
            const hashtags = 'ShindanMaker,診断メーカー';
            
            // XインテントURLの構築
            const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(postText)}&url=${encodeURIComponent(pageUrl)}&hashtags=${encodeURIComponent(hashtags)}`;
            
            // 新しいタブでシェア画面を開く
            window.open(shareUrl, '_blank', 'noopener,noreferrer');
        });
    }

    // 3. Auto-dismiss Flash Messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        // 5秒後に自動的にフェードアウトして削除
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                msg.remove();
            }, 500);
        }, 5000);
    });
});
