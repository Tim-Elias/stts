import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from app.logger import logger


class S3Manager:
    def __init__(self, app):
        logger.info("Инициализация S3 клиента.")
        self.s3 = boto3.client(
            's3',
            endpoint_url=app.config['endpoint_url'],
            region_name=app.config['region_name'],
            aws_access_key_id=app.config['aws_access_key_id'],
            aws_secret_access_key=app.config['aws_secret_access_key'],
            config=Config(s3={'addressing_style': 'path'})
        )

    def upload_file(self, file_name, bucket_name, object_name=None):
        if object_name is None:
            object_name = file_name
        logger.info(f"Загрузка файла '{file_name}' в bucket '{bucket_name}' с именем '{object_name}'.")
        try:
            self.s3.upload_file(file_name, bucket_name, object_name)
            logger.info(f"Файл '{file_name}' успешно загружен в {bucket_name}/{object_name}.")
        except ClientError as e:
            logger.error(f"Ошибка при загрузке файла '{file_name}': {e}")

    def download_file(self, bucket_name, object_name, file_name=None):
        if file_name is None:
            file_name = object_name
        logger.info(f"Скачивание файла '{object_name}' из bucket '{bucket_name}' в '{file_name}'.")
        try:
            self.s3.download_file(bucket_name, object_name, file_name)
            logger.info(f"Файл '{object_name}' успешно скачан в '{file_name}'.")
        except ClientError as e:
            logger.error(f"Ошибка при скачивании файла '{object_name}': {e}")

    def list_files(self, bucket_name, prefix=""):
        logger.info(f"Получение списка файлов из bucket '{bucket_name}' с префиксом '{prefix}'.")
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            files = [obj['Key'] for obj in response.get('Contents', [])]
            logger.info(f"Найдено {len(files)} файлов.")
            return files
        except ClientError as e:
            logger.error(f"Ошибка при получении списка файлов из bucket '{bucket_name}': {e}")
            return []

    def delete_file(self, bucket_name, object_name):
        logger.info(f"Удаление файла '{object_name}' из bucket '{bucket_name}'.")
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=object_name)
            logger.info(f"Файл '{object_name}' успешно удален из bucket '{bucket_name}'.")
        except ClientError as e:
            logger.error(f"Ошибка при удалении файла '{object_name}': {e}")

    def generate_presigned_url(self, bucket_name, object_name, expiration=3600):
        logger.info(f"Генерация временного URL для файла '{object_name}' в bucket '{bucket_name}', срок действия {expiration} секунд.")
        try:
            response = self.s3.generate_presigned_url('get_object',
                                                      Params={'Bucket': bucket_name, 'Key': object_name},
                                                      ExpiresIn=expiration)
            logger.info(f"URL успешно сгенерирован для файла '{object_name}'.")
            return response
        except ClientError as e:
            logger.error(f"Ошибка при генерации URL для файла '{object_name}': {e}")
            return None

    def file_exists(self, bucket_name, object_name):
        logger.info(f"Проверка существования файла '{object_name}' в bucket '{bucket_name}'.")
        try:
            self.s3.head_object(Bucket=bucket_name, Key=object_name)
            logger.info(f"Файл '{object_name}' существует в bucket '{bucket_name}'.")
            return True
        except ClientError as e:
            logger.warning(f"Файл '{object_name}' не найден в bucket '{bucket_name}': {e}")
            return False

    def get_file_metadata(self, bucket_name, object_name):
        logger.info(f"Получение метаданных для файла '{object_name}' из bucket '{bucket_name}'.")
        try:
            response = self.s3.head_object(Bucket=bucket_name, Key=object_name)
            logger.info(f"Метаданные для файла '{object_name}' получены.")
            return {
                'ContentType': response['ContentType'],
                'ContentLength': response['ContentLength'],
                'LastModified': response['LastModified'],
            }
        except ClientError as e:
            logger.error(f"Ошибка при получении метаданных для файла '{object_name}': {e}")
            return None

    def get_file(self, bucket_name, object_name):
        logger.info(f"Получение файла '{object_name}' из bucket '{bucket_name}'.")
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=object_name)
            file_content = response['Body'].read()  # Чтение содержимого файла в байты
            logger.info(f"Файл '{object_name}' успешно получен.")
            return file_content
        except ClientError as e:
            logger.error(f"Ошибка при получении файла '{object_name}': {e}")
            return None