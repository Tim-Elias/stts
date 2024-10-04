$(document).ready(function() {
    

    // Обработчик для формы входа
    $('#loginForm').on('submit', function(event) {
        event.preventDefault();

        let user_id = $('#user_id').val();
        let password = $('#password').val();

        $.ajax({
            url: '/auth',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_id: user_id, password: password }),
            success: function(response) {
                localStorage.setItem('jwt_token', response.access_token);  // Сохраняем токен в localStorage
                $('#loginAlert').html('<div class="alert alert-success">Login successful!</div>');
                window.location.href = '/account';  
            },
            error: function(xhr) {
                let errorMsg = 'An error occurred.';
                if (xhr.responseJSON && xhr.responseJSON.msg) {
                    errorMsg = xhr.responseJSON.msg;
                }
                $('#loginAlert').html(`<div class="alert alert-danger">${errorMsg}</div>`);
            }
            
        });
    });
    
    // Обработчик для кнопки "Войти через Google"
    $('#googleLogin').on('click', function() {
        // Редиректим пользователя на страницу авторизации Google
        window.location.href = '/auth/google';
    });

    // Обработчик для кнопки "Register"
    $('#registerButton').on('click', function() {
        // Редиректим пользователя на страницу регистрации
        window.location.href = '/register';
    });

    // Обработчик для формы регистрации
    $('#registerForm').on('submit', function(event) {
        event.preventDefault();

        let username = $('#username').val();
        let user_id = $('#user_id').val();
        let password = $('#password').val();

        $.ajax({
            url: '/register',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username: username, user_id: user_id, password: password }),
            success: function(response) {
                $('#registerAlert').html('<div class="alert alert-success">Registration successful! Redirecting...</div>');
                localStorage.setItem('jwt_token', response.access_token);  // Сохраняем токен в localStorage
                window.location.href = '/account'; 
            },
            error: function() {
                $('#registerAlert').html('<div class="alert alert-danger">Error during registration.</div>');
            }
        });
    });

});

