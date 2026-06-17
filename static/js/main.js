// JavaScript for ONE OK ROCK Lyrics Analysis App

document.addEventListener('DOMContentLoaded', () => {
    // 1. Asynchronous Like Button Functionality
    const likeButtons = document.querySelectorAll('.like-button');
    
    // ローカルストレージを使って同じ人が何度もいいねできないように簡易制御
    const likedInterpretations = JSON.parse(localStorage.getItem('liked_interps') || '[]');

    likeButtons.forEach(button => {
        const interpId = button.getAttribute('data-id');
        
        // 既にいいね済みの場合はスタイルを変更
        if (likedInterpretations.includes(interpId)) {
            setButtonLiked(button);
        }

        button.addEventListener('click', () => {
            if (likedInterpretations.includes(interpId)) {
                // 既にいいね済みの場合は処理しない
                return;
            }

            // 非同期リクエストを送信
            fetch(`/interpretation/${interpId}/like`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // いいね数の表示を更新
                    const countSpan = button.querySelector('.like-count');
                    if (countSpan) {
                        countSpan.textContent = data.likes;
                    }
                    
                    // ローカルストレージに保存し、ボタンの状態をいいね済みに変更
                    likedInterpretations.push(interpId);
                    localStorage.setItem('liked_interps', JSON.stringify(likedInterpretations));
                    setButtonLiked(button);
                    
                    // アニメーション効果の付与
                    button.classList.add('animate-pulse');
                    setTimeout(() => {
                        button.classList.remove('animate-pulse');
                    }, 500);
                } else {
                    console.error('Like failed:', data.message);
                }
            })
            .catch(err => {
                console.error('Error sending like:', err);
            });
        });
    });

    // いいね済みボタンのスタイル変更関数
    function setButtonLiked(button) {
        button.classList.add('btn-liked');
        button.style.borderColor = 'var(--accent-color)';
        button.style.color = 'var(--accent-color)';
        button.style.boxShadow = '0 0 10px rgba(255, 0, 85, 0.2)';
        button.setAttribute('disabled', 'true');
        // テキストを「共感しました」に変更
        const originalText = button.innerHTML;
        // 共感した (数) -> 共感しました (数)
        button.innerHTML = originalText.replace('共感した', '共感しました！');
    }

    // 2. Auto-dismiss Flash Messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
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
