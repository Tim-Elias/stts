$(document).ready(function() {
    const token = localStorage.getItem('jwt_token');

    // Проверка валидности токена
    if (!token) {
        window.location.href = '/';
    } else {
        $.ajax({
            url: '/protected',  // Защищённый маршрут для проверки токена
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                loadFiles();  // Загрузка списка файлов
            },
            error: function(xhr, status, error) {
                console.error('Ошибка проверки токена:', error);
                window.location.href = '/';
            }
        });
    }

    // Функция загрузки файлов
    // Функция загрузки файлов
    $('#uploadForm').on('submit', function(event) {
        event.preventDefault();

        let formData = new FormData(this);
        const fileInput = $('#fileInput')[0]; // input с id="fileInput"
        
        // Проверяем, что файл выбран
        if (fileInput.files.length === 0) {
            alert('Пожалуйста, выберите файл для загрузки.');
            return;
        }

        // Получаем оригинальное имя и расширение файла
        const originalFileName = fileInput.files[0].name; // Оригинальное имя файла
        const fileExtension = originalFileName.split('.').pop(); // Расширение файла

        // Устанавливаем имя файла без расширения в поле формы
        const fileNameWithoutExtension = originalFileName.split('.').slice(0, -1).join('.'); // Имя без расширения
        $('#fileNameInput').val(fileNameWithoutExtension); // input с id="fileNameInput"

        $.ajax({
            url: '/upload_audio',
            type: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            data: formData,
            processData: false,
            contentType: false,
            success: function() {
                alert('Файл успешно загружен');
                loadFiles();  // Обновление списка файлов
                // Очищаем форму после успешной загрузки
                $('#uploadForm')[0].reset(); // Сбрасываем форму
            },
            error: function(xhr, status, error) {
                console.error('Ошибка загрузки файла:', error);
            }
        });
    });

    // Функция загрузки списка файлов
    function loadFiles(page = 1) {
        $.ajax({
            url: `/get_files?page=${page}`,
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            success: function(response) {
                let fileList = $('#fileList');
                fileList.empty();

                response.files.forEach(file => {
                    fileList.append(`
                        <tr>
                            <td>${file.name}</td>
                            <td>
                                <button class="btn btn-info" onclick="downloadFile('${file.name}')">Download</button>
                                <button class="btn btn-danger" onclick="deleteFile('${file.name}')">Delete</button>
                            </td>
                        </tr>
                    `);
                });

                // Пагинация
                let pagination = $('#pagination');
                pagination.empty();
                for (let i = 1; i <= response.total_pages; i++) {
                    pagination.append(`<li class="page-item"><a class="page-link" href="#" onclick="loadFiles(${i})">${i}</a></li>`);
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка загрузки списка файлов:', error);
            }
        });
    }

    // Функция удаления файла
    window.deleteFile = function(fileName) {
        if (!confirm(`Are you sure you want to delete the file '${fileName}'?`)) return;

        $.ajax({
            url: '/delete_file',
            type: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({ 'file_name': fileName }),
            success: function() {
                alert(`File '${fileName}' deleted successfully`);
                loadFiles();  // Обновление списка файлов после удаления
            },
            error: function(xhr, status, error) {
                console.error(`Ошибка удаления файла ${fileName}:`, error);
            }
        });
    }

    // Обработчик для кнопки "Назад"
    $('#backButton').on('click', function() {
        window.location.href = '/account';  // Перенаправляем на главную страницу аккаунта
    });

    window.downloadFile = function(fileName) {
        $.ajax({
            url: '/download_file',
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            data: { file_name: fileName },
            success: function(response) {
                if (response.url) {
                    // Перенаправление на временный URL для скачивания
                    window.location.href = response.url;
                } else {
                    alert('Error generating download URL');
                }
            },
            error: function(xhr, status, error) {
                console.error(`Error downloading file ${fileName}:`, error);
            }
        });
    }
});
