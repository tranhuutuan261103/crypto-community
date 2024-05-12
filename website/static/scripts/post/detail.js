const loadComments = async (post_id) => {
    $('#comments').empty();
    $.ajax({
        url: 'http://127.0.0.1:5000/comments?post_id=' + post_id,
        type: 'GET',
        contentType: 'application/json',
        success: function(data) {
            console.log('Success:', data);
            data.forEach((comment) => {
                if (comment.parent_comment_id === null){
                    $('#comments').append(
                        `<div class="comment__item">
                            <div class="comment__header">
                                <img src='${comment.commented_by.avatar}' class="comment__avatar" />
                                <div class="comment__user">${comment.commented_by.name}</div>
                                <span class="comment__time">${comment.created_at}</span>
                            </div>
                            <div class="comment__content">${comment.content}</div>
                            <div class="comment__footer">
                                <div id="comment-${comment.id}__like" 
                                    class="comment__like ${comment.liked_by_me === true ? "comment__liked" : ""}" 
                                    onclick="likeComment('${comment.id}')"
                                >
                                    <i class="far fa-thumbs-up"></i>
                                    <span id="comment-${comment.id}__like-value">${comment.liked_by.length}</span>
                                </div>
                                <div class="comment__reply" onclick="replyComment(${comment.id})">
                                    <i class="far fa-comment"></i>
                                    <span class="comment-footer__span">Reply</span>
                                </div>
                            </div>
                            <div id="comment-${comment.id}" class="comment__reply-list"></div>
                            <div class="separate comment-item__separate"></div>
                        </div>`
                    );
                }
            });

            data.forEach((comment) => {
                if (comment.parent_comment_id !== null){
                    $('#comment-' + comment.parent_comment_id).append(
                        `<div class="comment__item">
                            <div class="comment__header">
                                <img src='${comment.commented_by.avatar}' class="comment__avatar" />
                                <div class="comment__user">${comment.commented_by.name}</div>
                                <span class="comment__time">${comment.created_at}</span>
                            </div>
                            <div class="comment__content">${comment.content}</div>
                            <div class="comment__footer">
                                <div id="comment-${comment.id}__like" 
                                    class="comment__like ${comment.liked_by_me === true ? "comment__liked" : ""}" 
                                    onclick="likeComment('${comment.id}')"
                                >
                                    <i class="far fa-thumbs-up"></i>
                                    <span id="comment-${comment.id}__like-value">${comment.liked_by.length}</span>
                                </div>
                                <div class="comment__reply" onclick="replyComment(${comment.id})">
                                    <i class="far fa-comment"></i>
                                    <span class="comment-footer__span">Reply</span>
                                </div>
                            </div>
                            <div class="separate comment-item__separate"></div>
                        </div>`
                    );
                }
            }
            );
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

const addComment = async (post_id) => {
    const content = $('#comment-input').val();

    $.ajax({
        url: 'http://127.0.0.1:5000/comments/create',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            post_id: post_id,
            content: content,
            parent_comment_id: null
        }),
        success: function(data) {
            console.log('Success:', data);
            $('#comment-input').val('');
            loadComments(post_id);
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

const likeComment = async (comment_id) => {
    $.ajax({
        url: `http://127.0.0.1:5000/comments/${comment_id}/like`,
        type: 'POST',
        contentType: 'application/json',
        success: function(data) {
            console.log('Success:', data);
            if (data.liked_by_me === false){
                $('#comment-' + comment_id + '__like').removeClass('comment__liked');
            } else {
                $('#comment-' + comment_id + '__like').addClass('comment__liked');
            }
            $('#comment-' + comment_id + '__like-value').text(data.liked_by.length);
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

const likePost = async (p_id) => {
    const params = {
        post_id: p_id
    };
    try {
        const response = await fetch('http://127.0.0.1:5000/post/like', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        if (!response.ok) {
            throw new Error('Server responded with an error!');
        }
        const data = await response.json();
        if (data === true){
            if ($('#post-' + p_id + '__like').hasClass('post__liked')){
                $('#post-' + p_id + '__like').removeClass('post__liked');
                $('#post-' + p_id + '__like--value').text(parseInt($('#post-' + p_id + '__like--value').text()) - 1);
            } else {
                $('#post-' + p_id + '__like').addClass('post__liked');
                $('#post-' + p_id + '__like--value').text(parseInt($('#post-' + p_id + '__like--value').text()) + 1);
            }
        } else {
            console.log('Error');
        }
    } catch (error) {
        console.error('Error:', error);
    }
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