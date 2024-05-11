const loadComments = async (post_id) => {
    $('#comments').empty();
    $.ajax({
        url: 'http://127.0.0.1:5000/comments?post_id=' + post_id,
        type: 'GET',
        contentType: 'application/json',
        success: function(data) {
            data.forEach((comment) => {
                $('#comments').append(
                    `<div class="comment__item">
                        <div class="comment__header">
                            <img src='${comment.commented_by.avatar}' class="comment__avatar" />
                            <div class="comment__user">${comment.commented_by.name}</div>
                            <span class="comment__time">${comment.created_at}</span>
                        </div>
                        <div class="comment__content">${comment.content}</div>
                        <div class="comment__footer">
                            <div class="comment__like" onclick="likeComment(${comment.id})">
                                <i class="far fa-thumbs-up"></i>
                                <span>${comment.liked_by.length}</span>
                            </div>
                            <div class="comment__reply" onclick="replyComment(${comment.id})">
                                <i class="far fa-comment"></i>
                                <span class="comment-footer__span">Reply</span>
                            </div>
                        </div>
                        <div class="separate comment-item__separate"></div>
                    </div>`
                );
            });
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

const cryptocurrency = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/post/cryptocurrency', 
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error('Server responded with an error!');
        }
        const data = await response.json();
        if (data !== null){
            $('#trending-token').empty();
            $('#trending-token').append(
                `<div class="trending-token__header">
                    <div class="trending-token__header--title">Trending Tokens</div>
                </div>`
            );
            data.forEach((token) => {
                $('#trending-token').append(
                    `<div class="trending-token__item">
                        <div class="trending-token__item--rank">${token.rank}</div>
                        <img src="https://s2.coinmarketcap.com/static/img/coins/64x64/${token.id}.png" alt="${token.name}" class="trending-token__item--image">
                        <div class="trending-token__item--name">${token.name}</div>
                        <div class="trending-token__item--slug">${token.slug}</div>
                    </div>`
                );
            });
        } else {
            console.log('Error');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

$(document).ready(() => {
    cryptocurrency();
});