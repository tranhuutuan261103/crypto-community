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
                            <div class="comment-item__inner">
                                <img src='${comment.commented_by.avatar}' class="comment__avatar" />
                                <div>
                                    <div class="comment__header">
                                        <div class="comment__user">${comment.commented_by.name}</div>
                                        <span class="comment__time">${comment.created_at}</span>
                                    </div>
                                    <div class="comment__content">${comment.content}</div>
                                </div>
                            </div>
                            <div class="comment__footer">
                                <div id="comment-${comment.id}__like" 
                                    class="comment__like ${comment.liked_by_me === true ? "comment__liked" : ""}" 
                                    onclick="likeComment('${comment.id}')"
                                >
                                    <i class="far fa-thumbs-up"></i>
                                    <span id="comment-${comment.id}__like-value">${comment.liked_by.length}</span>
                                </div>
                                <div class="comment__reply" onclick="replyComment('${comment.id}', '${comment.id}')">
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
                            <div class="comment-item__inner">
                                <img src='${comment.commented_by.avatar}' class="comment__avatar" />
                                <div style="position: relative;">
                                    <div class="comment__header">
                                        <div class="comment__user">${comment.commented_by.name}</div>
                                        <span class="comment__time">${comment.created_at}</span>
                                    </div>
                                    ${comment.replying_to !== null ? `<span class="comment__reply-to">Replying to ${comment.replying_to.name}</span>` : ""}
                                    <div class="comment__content">${comment.content}</div>
                                </div>
                            </div>
                            <div class="comment__footer">
                                <div id="comment-${comment.id}__like" 
                                    class="comment__like ${comment.liked_by_me === true ? "comment__liked" : ""}" 
                                    onclick="likeComment('${comment.id}')"
                                >
                                    <i class="far fa-thumbs-up"></i>
                                    <span id="comment-${comment.id}__like-value">${comment.liked_by.length}</span>
                                </div>
                                <div class="comment__reply" onclick="replyComment('${comment.id}', '${comment.parent_comment_id}')">
                                    <i class="far fa-comment"></i>
                                    <span class="comment-footer__span">Reply</span>
                                </div>
                            </div>
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
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
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
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        success: function(data) {
            if (data.code === 401){
                openModalAuth();
                return;
            }
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
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify(params)
        });
        if (!response.ok) {
            throw new Error('Server responded with an error!');
        }
        const data = await response.json();
        if (data.code === 401){
            openModalAuth();
            return;
        }
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

const closeModal = () => {
    $('#modal-comment').css('display', 'none');
    $('#modal-comment-reply-user').text('');
    $('#modal-comment-reply-user-2').text('');
    $('#modal-comment-reply-avatar').attr('src', '');
    $('#modal-comment-reply-avatar').attr('alt', '');
    $('#modal-comment-reply-content').text('');
    $('#modal-comment-reply-time').text('');
}

const replyComment = (comment_id, parent_comment_id) => {
    $.ajax({
        url: `http://127.0.0.1:5000/comments/${comment_id}`,
        type: 'GET',
        contentType: 'application/json',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        success: function(data) {
            $('#modal-comment-reply-user').text(data.commented_by.name);
            $('#modal-comment-reply-user-2').text(data.commented_by.name);
            $('#modal-comment-reply-avatar').attr('src', data.commented_by.avatar);
            $('#modal-comment-reply-avatar').attr('alt', data.commented_by.name);
            $('#modal-comment-reply-content').text(data.content);
            $('#modal-comment-reply-time').text(data.created_at);
            $('#modal-comment-reply-btn').attr('onclick', `submitReplyComment('${comment_id}', '${parent_comment_id}')`);
            $('#modal-comment').css('display', 'flex');
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
    $('#modal-comment').css('display', 'flex');
}

const submitReplyComment = async (comment_id, parent_comment_id_param) => {
    const content = $('#modal-comment-reply-input').val();

    $.ajax({
        url: `http://127.0.0.1:5000/comments/${comment_id}/reply`,
        type: 'POST',
        contentType: 'application/json',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        data: JSON.stringify({
            post_id: $('#post-id').val(),
            content: content,
            parent_comment_id: parent_comment_id_param
        }),
        success: function(data) {
            if (data.code === 401){
                openModalAuth();
                return;
            }
            console.log('Success:', data);
            $('#modal-comment-reply-input').val('');
            closeModal();
            loadComments($('#post-id').val());
        },
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
            $('#trending-token-list').empty();
            data.forEach((token) => {
                $('#trending-token-list').append(
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