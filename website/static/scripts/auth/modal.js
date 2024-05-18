const closeModalAuth = () => {
    const modalAuth = document.getElementById('modal-auth');
    modalAuth.classList.remove('modal-auth--show');
}

const openModalAuth = () => {
    const modalAuth = document.getElementById('modal-auth');
    modalAuth.classList.add('modal-auth--show');
}

const closeBoxUser = () => {
    const boxUser = document.getElementById('box-user');
    boxUser.classList.remove('box-user--show');
}

const openBoxUser = () => {
    const boxUser = document.getElementById('box-user');
    if (boxUser.classList.contains('box-user--show')) {
        boxUser.classList.remove('box-user--show');
    } else {
        boxUser.classList.add('box-user--show');
    }
}

const toggleModalAuth = (tag) => {
    switch (tag) {
        case 'login':
            document.getElementById('modal-auth__login-title').classList.add('modal-auth__title--active');
            document.getElementById('modal-auth__signup-title').classList.remove('modal-auth__title--active');
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';
            document.getElementById('fullname').value = '';
            document.getElementById('email').focus();
            document.getElementById('modal-auth-btn').setAttribute('onclick', 'login()');
            document.getElementById('modal-auth-btn').innerText = 'Login';
            document.getElementById('modal-auth__fullname').classList.add('modal-auth__fullname--hide');
            break;
        case 'signup':
            document.getElementById('modal-auth__login-title').classList.remove('modal-auth__title--active');
            document.getElementById('modal-auth__signup-title').classList.add('modal-auth__title--active');
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';
            document.getElementById('fullname').value = '';
            document.getElementById('email').focus();
            document.getElementById('modal-auth-btn').setAttribute('onclick', 'signup()');
            document.getElementById('modal-auth-btn').innerText = 'Sign Up';
            document.getElementById('modal-auth__fullname').classList.remove('modal-auth__fullname--hide');
            break;
        default:
            break;
    }
}

const login = () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if (email && password) {
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/auth/login',
            data: {
                email: email,
                password: password
            },
            success: (response) => {
                if (response.status === '404')
                    alert('User not found');
                else {
                    console.log(response);
                    localStorage.setItem('avatar', response.avatar);
                    localStorage.setItem('fullname', response.fullname);
                    localStorage.setItem('email', response.email);
                    checkLogin();
                    closeModalAuth();
                    document.getElementById('email').value = '';
                    document.getElementById('password').value = '';
                    document.getElementById('fullname').value = '';
                    location.reload();
                }
            }
        });
    } else {
        alert('Please fill in all fields');
    }
}

const signup = () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const fullname = document.getElementById('fullname').value;
    if (email && password) {
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/auth/signup',
            data: {
                email: email,
                password: password,
                fullname: fullname
            },
            success: (response) => {
                if (response.status === '409')
                    alert('User already exists');
                else {
                    console.log(response);
                    localStorage.setItem('fullname', response.fullname);
                    localStorage.setItem('email', response.email);
                    localStorage.setItem('avatar', response.avatar);
                    checkLogin();
                    closeModalAuth();
                    document.getElementById('email').value = '';
                    document.getElementById('password').value = '';
                    document.getElementById('fullname').value = '';
                    location.reload();
                }
            }
        });
    }
}

const checkLogin = () => {
    console.log('Checking login');
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5000/account/info',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        success: (response) => {
            if (response.status === '200') {
                console.log(response);
                if (response.profile.fullname !== '') {
                    $('#box-user__name').text(response.profile.fullname);
                    $('#user-welcome__username').text(response.profile.fullname);
                } else {
                    $('#box-user__name').text('User');
                    $('#user-welcome__username').text('User');
                }
                $('#box-user__email').text(response.profile.email);
                $('#box-user__avatar').attr('src', response.profile.avatar);

                $('#box-user__item-logout').css('display', 'flex');
                $('#box-user__item-login').css('display', 'none');

                $('#box-user__header--link').attr('href', '/account');
                $('#box-user__header--link').removeAttr('onclick');
                return true;
            } else {
                console.log('Not logged in');
                $('#box-user__name').text("Guest");
                $('#user-welcome__username').text("Guest");
                $('#box-user__email').text("");
                $('#box-user__avatar').attr('src', "/static/images/user.png");
                $('#box-user__item-logout').css('display', 'none');
                $('#box-user__item-login').css('display', 'flex');
                $('#box-user__header--link').attr('href', '#');
                $('#box-user__header--link').attr('onclick', 'openModalAuth()');
                return false;
            }
        }
    });
}

const logout = () => {
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/auth/logout',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        success: (response) => {
            console.log(response);
            checkLogin();
        }
    });
}