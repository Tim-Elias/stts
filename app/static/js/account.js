$(document).ready(function() {
    // Проверка наличия токена в localStorage
    const token = localStorage.getItem('jwt_token');

    // Если токен отсутствует, перенаправляем на страницу home
    if (!token) {
        window.location.href = '/';
    } else {
        // Проверка валидности токена с сервером
        $.ajax({
            url: '/protected',  // Защищенный маршрут для проверки токена
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                console.log('Токен валидный, пользователь: ', response.logged_in_as);

                // Запрос имени пользователя
                $.ajax({
                    url: '/get_username',  // Маршрут для получения имени пользователя
                    type: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + token
                    },
                    success: function(username) {
                        // Вставляем имя пользователя в HTML
                        $('#username').text(username);
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка получения имени пользователя:', error);
                    }
                });
            },
            error: function(xhr, status, error) {
                console.error('Ошибка проверки токена:', error);
                window.location.href = '/';
            }
        });
    }
    


    // Обработчик выхода из аккаунта
    $('#logoutButton').on('click', function() {
        localStorage.removeItem('jwt_token');  // Удаляем токен из localStorage
        window.location.href = '/';  // Перенаправляем на страницу входа
    });

    // Обработчик кнопки "Управление промптами"
    $('#managePrompts').on('click', function() {
        console.log('Переход к управлению промптами');
        window.location.href = '/manage_prompts';
        // Здесь может быть логика перенаправления или отображения интерфейса управления промптами
    });

    // Обработчик кнопки "Загрузить аудиозаписи"
    $('#uploadAudio').on('click', function() {
        console.log('Переход к загрузке аудиозаписей');
        window.location.href = '/manage_audio';
        // Логика для загрузки аудиофайлов
    });

    // Обработчик кнопки "Транскрибация аудио и анализ"
    $('#transcribeAnalyze').on('click', function() {
        console.log('Переход к транскрибации и анализу');
        window.location.href = '/transcription';  // Перенаправляем на страницу входа
        // Логика транскрибации и анализа аудиозаписей
    });

    // Обработчик кнопки "Результаты"
    $('#viewResults').on('click', function() {
        console.log('Переход к результатам');
        window.location.href = '/transcription_result';
        // Логика для отображения результатов
    });

    // Обработчик кнопки "История действий"
    $('#viewHistory').on('click', function() {
        console.log('Переход к истории действий');
        // Логика для отображения истории действий пользователя
    });

    // Обработчик кнопки "Административная панель"
    $('#adminPanel').on('click', function() {
        console.log('Переход к административной панели');
        // Логика для доступа к административной панели
    });

});