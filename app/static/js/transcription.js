$(document).ready(function() {
    // Проверка наличия токена в localStorage
    const token = localStorage.getItem('jwt_token');

    // Если токен отсутствует, перенаправляем на страницу входа
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
                loadPrompts(); // Загружаем промпты после проверки токена
                loadAudioFiles(); // Загрузка аудиофайлов после проверки токена
            },
            error: function(xhr, status, error) {
                console.error('Ошибка проверки токена:', error);
                window.location.href = '/';
            }
        });
    }

    // Обработка формы при отправке
    // Обновление кода отправки аудиофайла
    $('#audioForm').on('submit', function(event) {
        event.preventDefault();

        const selectedAudioFile = $('#audioSelect').val();  // Получаем выбранный аудиофайл
        const selectedPrompt = $('#prompt_name').val();      // Получаем выбранный промпт

        if (!selectedAudioFile) {
            alert('Пожалуйста, выберите аудиофайл.');
            return;
        }

        if (!selectedPrompt) {
            alert('Пожалуйста, выберите промпт.');
            return;
        }

        const formData = new FormData();
        downloadAudioFile(selectedAudioFile).then((audioFile) => {
            formData.append('audio', audioFile);  // Добавляем файл в FormData
            formData.append('prompt_name', selectedPrompt);  // Добавляем промпт

            processAudio(formData);  // Отправляем данные на сервер
        }).catch(error => {
            alert('Ошибка при скачивании аудиофайла: ' + error.message);
        });
    });

    // Функция для обработки аудиофайла
    function processAudio(formData) {
        const token = localStorage.getItem('jwt_token');
        $('#loadingIcon').show();  // Показываем иконку загрузки
        $('#submitButton').prop('disabled', true).text('Отправка...');  // Блокируем кнопку

        $.ajax({
            url: '/process_audio',  // Маршрут обработки аудио
            type: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log('Аудиофайл успешно отправлен');

                // Скрываем спиннер и восстанавливаем кнопку
                $('#loadingIcon').hide();  
                $('#submitButton').prop('disabled', false).text('Отправить');

                // Получаем транскрипцию и анализ из ответа
                //const transcription = encodeURIComponent(response.transcription);
                //const analysis = encodeURIComponent(response.analysis);
                const transcription_id = encodeURIComponent(response.transcription_id);
                // Перенаправляем на страницу с параметрами
                window.location.href = `/transcription/view/${transcription_id}`;
                //window.location.href = `/result?transcription=${transcription}&analysis=${analysis}`;
            },
            error: function(xhr) {
                // Скрываем иконку загрузки и восстанавливаем кнопку при ошибке
                $('#loadingIcon').hide();
                $('#submitButton').prop('disabled', false).text('Отправить');
                
                let errorMsg = 'Произошла ошибка при обработке аудио.';
                if (xhr.responseJSON && xhr.responseJSON.msg) {
                    errorMsg = xhr.responseJSON.msg;
                } else if (xhr.responseText) {
                    try {
                        const responseObj = JSON.parse(xhr.responseText);
                        if (responseObj.error) {
                            errorMsg = responseObj.error;
                        }
                    } catch (e) {
                        console.error('Ошибка парсинга ответа:', e);
                    }
                }
                alert(errorMsg);
            }
        });
    }

    // Функция для скачивания аудиофайла в виде байтов
    function downloadAudioFile(fileName) {
        return new Promise((resolve, reject) => {
            const token = localStorage.getItem('jwt_token');
            $.ajax({
                url: '/download_file_bytes',  // Обновляем URL на новый маршрут
                type: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + token
                },
                data: { file_name: fileName },
                xhrFields: {
                    responseType: 'blob'  // Указываем, что ожидаем ответ в виде Blob
                },
                success: function(blob) {
                    // Проверяем, действительно ли получен Blob
                    if (blob instanceof Blob) {
                        // Создаем объект File из Blob
                        const file = new File([blob], fileName, { type: blob.type });
                        resolve(file);  // Возвращаем файл
                    } else {
                        reject(new Error('Получен некорректный ответ от сервера.'));
                    }
                },
                error: function(xhr, status, error) {
                    console.error(`Error downloading file ${fileName}:`, error);
                    reject(new Error('Ошибка при скачивании файла: ' + error));
                }
            });
        });
    }


    // Загрузка всех промптов
    function loadPrompts() {
        const token = localStorage.getItem('jwt_token');
        $.ajax({
            url: '/user_prompts',
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                console.log('Полученные данные:', response);  // Отладка
                const promptSelect = $('#prompt_name');
                promptSelect.empty();
                promptSelect.append('<option value="">-- Выберите промпт --</option>');

                response.prompt_data.forEach(prompt => {
                    promptSelect.append(`<option value="${prompt.prompt_name}">${prompt.prompt_name}</option>`);
                });
            },
            error: function(xhr, status, error) {
                console.error('Ошибка загрузки промптов:', status, error);
            }
        });
    }

    // Загрузка всех аудиофайлов
    function loadAudioFiles() {
        const token = localStorage.getItem('jwt_token');
        $.ajax({
            url: '/user_audio_files',
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                const audioSelect = $('#audioSelect');
                audioSelect.empty();
                audioSelect.append('<option value="">-- Выберите аудиофайл --</option>');

                response.audio_files.forEach(audio => {
                    audioSelect.append(`<option value="${audio[0]}">${audio[0]}</option>`);
                });
            },
            error: function(xhr, status, error) {
                console.error('Ошибка загрузки аудиофайлов:', status, error);
            }
        });
    }
    $('#backButton').on('click', function() {
        window.location.href = '/account';
    });
});
