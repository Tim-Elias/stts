$(document).ready(function() {

    const token = localStorage.getItem('jwt_token');

    // Проверка валидности токена
    if (!token) {
        window.location.href = '/';
    } else {
        $.ajax({
            url: '/admin_protected',  // Защищённый маршрут для проверки токена
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                loadLogs();  // Загрузка списка файлов
            },
            error: function(xhr, status, error) {
                console.error('Ошибка проверки токена:', error);
                window.location.href = '/';
            }
        });
    }



    function loadLogs() {
        $.ajax({
            url: '/logs/data',
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('jwt_token')  // Вставляем токен из локального хранилища
            },
            success: function(data) {
                $('#logs-container').text(data.logs);  // Вставляем логи в контейнер
            },
            error: function(xhr, status, error) {
                $('#logs-container').text('Ошибка загрузки логов.');
                console.error('Ошибка:', error);
            }
        });
    }

    // Загружаем логи при загрузке страницы
    loadLogs();

    // Можно настроить автоматическое обновление логов каждые 30 секунд
    setInterval(loadLogs, 30000);

    $('#backButton').on('click', function() {
        window.location.href = '/account';
    });

});
