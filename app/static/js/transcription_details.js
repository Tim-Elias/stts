$(document).ready(function() {
    const token = localStorage.getItem('jwt_token');
    const transcriptionId = window.location.pathname.split('/').pop(); // Получаем transcription_id из URL

    // Проверка наличия токена в localStorage
    if (!token) {
        window.location.href = '/'; // Перенаправление на главную страницу
    }

    // Загружаем данные транскрипции
    loadTranscriptionDetails(transcriptionId);

    function loadTranscriptionDetails(transcriptionId) {
        $('#loadingIndicator').show();
        $.ajax({
            url: `/api/transcription/${transcriptionId}`,
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                // Заполняем данные на странице
                $('#audioId').text(response.transcription_id); // Выводим transcription_id
                $('#transcriptionText').text(response.text);
                $('#transcriptionAnalysis').text(response.analysis);
                $('#transcriptionPrompt').text(response.prompt);
                $('#transcriptionTokens').text(response.tokens);
                $('#loadingIndicator').hide();
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при загрузке транскрипции:', error);
                alert('Не удалось загрузить транскрипцию.');
                $('#loadingIndicator').hide();
            }
        });
    }

    // Обработчик для кнопки "Назад"
    $('#backButton').on('click', function() {
        window.location.href = '/transcription_result'; // Перенаправляем на страницу со списком транскрипций
    });
});
