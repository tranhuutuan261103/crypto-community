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

const previewThumbnail = (input) => {
    console.log("Preview Thumbnail");
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
            $('#thumbnail-preview').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

const createPost = async () => {
    const content = $('#content').val();
    //const thumbnail = $('#thumbnail')[0].files[0];
    const params = {
        content: content,
        //thumbnail: thumbnail
    };
    try {
        const response = await fetch('http://127.0.0.1:5000/post/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({post: params})
        });
        if (!response.ok) {
            throw new Error('Server responded with an error!');
        }
        const data = await response.json();
        if (data === true){
            window.location.href = '/';
        } else {
            console.log('Error');
        }
    }
    catch (error) {
        console.error('Error:', error);
    }
}