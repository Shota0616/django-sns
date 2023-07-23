function addLikeButtonEvent(button) {
    // likeボタンが押下されたら実行
    button.addEventListener('click', e => {
        // もしログインしていなかったらログイン画面に遷移
        const is_authenticated = button.getAttribute('data-is-authenticated');
        const account_login = button.getAttribute('data-account-login');
        if (is_authenticated === "False") {
            window.location.href = account_login;
        }
        // イベントのデフォルトの動作をキャンセル
        e.preventDefault();
        // 各種変数に代入
        const tweetPk = button.getAttribute('data-tweet-pk');
        const url = button.getAttribute('data-tweet-like-tweet-url');
        const csrf_token = button.getAttribute('data-csrf-token');
        const formData = new FormData();
        formData.append('tweet_pk', tweetPk);
        // fetchAPIでPOST送信
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {'X-CSRFToken': csrf_token}
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
}

// 無限スクロール
var isLoading = false;

function loadMoreTweets() {
    if (!isLoading) {
        isLoading = true;
        var tweetContainer = document.querySelector('.tweet-container');
        var nextPage = tweetContainer.getAttribute('data-next-page');

        if (nextPage !== null) {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', window.location.pathname + '?page=' + nextPage, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    var parser = new DOMParser();
                    var data = parser.parseFromString(xhr.responseText, 'text/html');
                    var newTweetsContainer = data.querySelector('.tweet-container');
                    var newTweets = newTweetsContainer.innerHTML;
                    tweetContainer.insertAdjacentHTML('beforeend', newTweets);
                    tweetContainer.setAttribute('data-next-page', newTweetsContainer.getAttribute('data-next-page'));
                    isLoading = false;

                    // 新しいツイートに対していいねボタンのイベントリスナーを再設定
                    document.querySelectorAll('.ajax-like-for-post').forEach(button => {
                        addLikeButtonEvent(button);
                    });
                } else if (xhr.readyState === XMLHttpRequest.DONE) {
                    isLoading = false;
                }
            };
            xhr.send();
        }
    }
}

function handleScroll() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 300) {
        loadMoreTweets();
    }
}


// 最初にドキュメントが読み込まれたら実行する
window.addEventListener('DOMContentLoaded', function(){
    // likeボタンのイベントリスナーを登録
    document.querySelectorAll('.ajax-like-for-post').forEach(button => {
        addLikeButtonEvent(button);
    });
});

window.addEventListener('scroll', handleScroll);