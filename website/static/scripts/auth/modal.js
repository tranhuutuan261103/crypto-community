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
                    localStorage.setItem('token', response.token);
                    localStorage.setItem('user_name', response.user_name);
                    localStorage.setItem('email', response.email);
                    checkLogin();
                    closeModalAuth();
                    document.getElementById('email').value = '';
                    document.getElementById('password').value = '';
                    document.getElementById('fullname').value = '';
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
    if (email && password) {
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/auth/signup',
            data: {
                email: email,
                password: password
            },
            success: (response) => {
                if (response.status === '409')
                    alert('User already exists');
                else {
                    console.log(response);
                    localStorage.setItem('token', response.token);
                    localStorage.setItem('user_name', response.user_name);
                    localStorage.setItem('email', response.email);
                    checkLogin();
                    closeModalAuth();
                    document.getElementById('email').value = '';
                    document.getElementById('password').value = '';
                    document.getElementById('fullname').value = '';
                }
            }
        });
    }
}

const checkLogin = () => {
    if (localStorage.getItem('token')) {
        $('#user-welcome__username').text(localStorage.getItem('user_name'));
        if (localStorage.getItem('user_name') === '') {
            $('#box-user__name').text("No name");
            $('#user-welcome__username').text("No name");
        } else {
            $('#box-user__name').text(localStorage.getItem('user_name'));
            $('#user-welcome__username').text(localStorage.getItem('user_name'));
        }
        $('#box-user__email').text(localStorage.getItem('email'));

        $('#box-user__item-logout').css('display', 'flex');
        $('#box-user__item-login').css('display', 'none');
    } else {
        $('#user-welcome__username').text('Guest');
        $('#box-user__name').text('Guest');
        $('#box-user__email').text('Guest');

        $('#box-user__item-logout').css('display', 'none');
        $('#box-user__item-login').css('display', 'flex');
    }
}

const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_name');
    localStorage.removeItem('email');
    checkLogin();
}