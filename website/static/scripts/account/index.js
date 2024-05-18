const updateBackground = () => {
    const background = $('#profile-background').prop('files')[0];
    const data = new FormData();
    data.append('background', background);
    $.ajax({
        url: '/account/update-background',
        type: 'POST',
        data: data,
        contentType: false,
        processData: false,
        success: function(response){
            if (response.status === '200'){
                $('#profile-background-img').attr('src', response.profile.background);
                $('#profile-alert').html('<div class="alert alert-success" role="alert">Background updated successfully</div>');
            } else {
                $('#profile-alert').html('<div class="alert alert-danger" role="alert">Error updating background</div>');
            }
        }
    });
}

const post_detail = async (p_id) => {
    window.location.href = '/post/' + p_id;
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
        if (data === true){
            if ($('#post-' + p_id + '__like').hasClass('post__liked')){
                $('#post-' + p_id + '__like').removeClass('post__liked');
                $('#post-' + p_id + '__like--value').text(parseInt($('#post-' + p_id + '__like--value').text()) - 1);
            } else {
                $('#post-' + p_id + '__like').addClass('post__liked');
                $('#post-' + p_id + '__like--value').text(parseInt($('#post-' + p_id + '__like--value').text()) + 1);
            }
        } else {
            openModalAuth();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}