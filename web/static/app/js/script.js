document.querySelectorAll('.ajax-like-for-post').forEach(button => {
    // likeボタンが押下されたら実行
    button.addEventListener('click', e => {
        // もしログインしていなかったらログイン画面に遷移
        if ("{{ user.is_authenticated }}" === "False") {
            window.location.href = '{% url "account_login" %}';
        }
        // イベントのデフォルトの動作をキャンセル
        e.preventDefault();
        // 各種変数に代入
        const tweetPk = button.getAttribute('data-tweet-pk');
        const url = '{% url "like_tweet" %}';
        const formData = new FormData();
        formData.append('tweet_pk', tweetPk);
        // fetchAPIでPOST送信
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {'X-CSRFToken': '{{ csrf_token }}'}
        }).then(response => {
            return response.json();
        }).then(response => {
            const counter = button.nextElementSibling;
            const icon = button.querySelector('.like-for-post-icon');
            counter.textContent = response.tweet_likes;
            if (response.method === 'create') {
                icon.classList.remove('far');
                icon.classList.add('fas');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
            }
        }).catch(error => {
            console.log(error);
        });
    });
});