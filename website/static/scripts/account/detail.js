$('#profile-fullname').on('input',function(e){
    if (e.target.value.length > 0){
        $('#profile-fullname').removeClass('is-invalid');
        $('#profile-fullname').addClass('is-valid');
    } else {
        $('#profile-fullname').removeClass('is-valid');
        $('#profile-fullname').addClass('is-invalid');
    }
    if (e.target.value !== $('#profile-fullname-original').val()){
        $('#profile-fullname').addClass('is-changed');
    } else {
        $('#profile-fullname').removeClass('is-changed');
    }
    checkBtnUpdate();
});

$('#profile-bio').on('input',function(e){
    if (e.target.value.length > 0){
        $('#profile-bio').removeClass('is-invalid');
        $('#profile-bio').addClass('is-valid');
    } else {
        $('#profile-bio').removeClass('is-valid');
        $('#profile-bio').addClass('is-invalid');
    }
    if (e.target.value !== $('#profile-bio-original').val()){
        $('#profile-bio').addClass('is-changed');
    } else {
        $('#profile-bio').removeClass('is-changed');
    }
    checkBtnUpdate();
});

const checkBtnUpdate = () => {
    if ($('#profile-fullname').hasClass('is-valid') && $('#profile-bio').hasClass('is-valid') 
        && ($('#profile-fullname').hasClass('is-changed') || $('#profile-bio').hasClass('is-changed')) ){
        $('#profile-btn-update').prop('disabled', false);
    } else {
        $('#profile-btn-update').prop('disabled', true);
    }
}

const updateProfile = () => {
    const fullname = $('#profile-fullname').val();
    const bio = $('#profile-bio').val();
    const data = {fullname: fullname, bio: bio};
    $.ajax({
        url: '/account/update',
        type: 'POST',
        data: data,
        success: function(response){
            if (response.status === '200'){
                $('#profile-fullname-original').val(fullname);
                $('#profile-bio-original').val(bio);
                $('#profile-fullname').removeClass('is-changed');
                $('#profile-bio').removeClass('is-changed');
                $('#profile-btn-update').prop('disabled', true);
                $('#profile-alert').html('<div class="alert alert-success" role="alert">Profile updated successfully</div>');
            } else {
                $('#profile-alert').html('<div class="alert alert-danger" role="alert">Error updating profile</div>');
            }
        }
    });
}

const updateAvatar = () => {
    const avatar = $('#profile-avatar').prop('files')[0];
    const data = new FormData();
    data.append('avatar', avatar);
    $.ajax({
        url: '/account/update-avatar',
        type: 'POST',
        data: data,
        contentType: false,
        processData: false,
        success: function(response){
            if (response.status === '200'){
                $('#profile-avatar-img').attr('src', response.profile.avatar);
                $('#profile-alert').html('<div class="alert alert-success" role="alert">Avatar updated successfully</div>');
            } else {
                $('#profile-alert').html('<div class="alert alert-danger" role="alert">Error updating avatar</div>');
            }
        }
    });
}