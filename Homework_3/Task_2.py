import requests
from pprint import pprint


class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.header = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token}'
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        param = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=self.header, params=param)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path)['href']
        print(href)
        with open(filename, 'rb') as file:
            response = requests.put(href, file)
        response.raise_for_status()
        if response.status_code == 201:
            print('Success!')


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    ya = YaUploader('token')
    ya.upload_file_to_disk('Netology/file.txt', 'file.txt')
