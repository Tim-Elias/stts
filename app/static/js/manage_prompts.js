$(document).ready(function() {
    console.log('Управление промптами подключилось');
    const token = localStorage.getItem('jwt_token');

    // Если токен отсутствует, перенаправляем на домашнюю страницу
    if (!token) {
        window.location.href = '/';
    } else {
        // Проверка валидности токена на сервере
        $.ajax({
            url: '/protected',  // Защищённый маршрут для проверки токена
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                loadPrompts();
                console.log('Токен валидный, пользователь: ', response.logged_in_as);
            },
            error: function(xhr, status, error) {
                console.error('Ошибка проверки токена:', error);
                // Если токен недействителен, перенаправляем на домашнюю страницу
                window.location.href = '/';
            }
        });
    }

    // Функция для загрузки промптов
    function loadPrompts() {
        $.ajax({
            url: '/get_prompts',
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                const promptList = $('#promptList');
                promptList.empty(); // Очищаем перед обновлением списка

                response.prompt_data.forEach(prompt => {
                    promptList.append(`
                        <tr>
                            <td>${prompt.prompt_name}</td>
                            <td>${prompt.text}</td>
                            <td>
                                <a href="/prompt/${prompt.prompt_id}" class="btn btn-warning">Edit</a>
                                <button class="btn btn-danger" onclick="deletePrompt(${prompt.prompt_id})">Delete</button>
                            </td>
                        </tr>
                    `);
                });
            },
            error: function(xhr, status, error) {
                console.error('Error loading prompts:', status, error);
            }
        });
    }

    // Функция для удаления промпта
    window.deletePrompt = function(prompt_id) {
        if (confirm('Are you sure you want to delete this prompt?')) {
            $.ajax({
                url: `/prompt/${prompt_id}/delete`,
                type: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + token
                },
                success: function() {
                    loadPrompts();  // Перезагрузить список после удаления
                },
                error: function(xhr, status, error) {
                    console.error('Error deleting prompt:', status, error);
                }
            });
        }
    };
});
