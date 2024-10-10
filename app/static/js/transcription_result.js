$(document).ready(function() {
    const token = localStorage.getItem('jwt_token');
    let offset = 0;
    const limit = 10;

    if (!token) {
        window.location.href = '/';
    } else {
        $.ajax({
            url: '/protected',
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                loadTranscriptions();
            },
            error: function(xhr, status, error) {
                console.error('Ошибка проверки токена:', error);
                window.location.href = '/';
            }
        });
    }

    function loadTranscriptions() {
        $.ajax({
            url: `/transcriptions?offset=${offset}&limit=${limit}`,
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                $('#loadingIndicator').hide();
                $('#transcriptionsTable tbody').empty();

                if (response.length === 0) {
                    $('#transcriptionsTable tbody').append('<tr><td colspan="3">Нет транскрипций.</td></tr>');
                }

                response.forEach(function(transcription) {
                    const row = `<tr class="clickable-row" data-transcription-id="${transcription.transcription_id}">
                                    <td>${transcription.transcription_id}</td>
                                    <td>${transcription.text}</td>
                                    <td>${transcription.analysis}</td>
                                </tr>`;
                    $('#transcriptionsTable tbody').append(row);
                });

                // Обработчик для клика по строкам
                $('.clickable-row').on('click', function() {
                    const transcriptionId = $(this).data('transcription-id');
                    window.location.href = `/transcription/view/${transcriptionId}`; // Переход на страницу с деталями транскрипции
                });
            },
            error: function(xhr, status, error) {
                $('#loadingIndicator').hide();
                console.error('Ошибка при загрузке транскрипций:', error);
            }
        });
    }

});
