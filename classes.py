from abc import ABC, abstractmethod
import requests
from connector import Connector
import json
import os


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        return Connector(file_name)


class SuperJob(Engine):
    """Методы SJ."""

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword
        self.parameters = None

    def get_request(self):
        """API запрос
        В системе должен быть записан API ключ под названием SUPERJOB_API_KEY !!!
        """
        headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv('SUPERJOB_API_KEY'),
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.parameters = {'keyword': self.keyword, 'count': 1, 'page': 0}
        raw_data = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=self.parameters)
        data = raw_data.content.decode()
        raw_data.close()
        json_sj = json.loads(data)
        return json_sj

    def get_info_vacancy(self, data):
        info = {
            'from': 'SuperJob',
            'name': data['profession'],
            'url': data['link'],
            'description': data.get('client').get('description'),
            'salary': data['currency'],
            'date_published': data['date_published']

        }
        return info

    @property
    def get_vacancies(self):
        vacancies = []
        while len(vacancies) <= 500:
            data = self.get_request()
            objects = data['objects']
            if not objects:
                break
            for vacancy in objects:
                if vacancy.get('currency') is not None and vacancy.get('currency') == 'rub':
                    vacancies.append(self.get_info_vacancy(vacancy))
            self.parameters['page'] += 1

        return vacancies


class HH(Engine):
    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword
        self.parameters = {
            'text': self.keyword,
            'per_page': 100,
            'area': 113,
            'page': 0
       }

    def get_request(self):
        response = requests.get('https://api.hh.ru/vacancies/', params=self.parameters)
        data = response.content.decode()
        response.close()
        json_hh = json.loads(data)
        return json_hh

    def get_info_vacancy(self, data):
        info = {
            'from': 'HeadHunter',
            'name': data.get('name'),
            'url': data.get('alternate_url'),
            'description': data.get('snippet').get('responsibility'),
            'salary': data.get('salary'),
            'date_published': data.get('published_at'),
            'experience': data.get('experience'),
            'page_number': data.get('page')
        }
        return info

    @property
    def get_vacancies(self):
        vacancies = []
        while len(vacancies) <= 500:
            data = self.get_request()
            items = data.get('items')
            if not items:
                break
            for vacancy in items:
                if vacancy.get('salary') is not None and vacancy.get('salary').get('currency') == 'RUR':
                    vacancies.append(self.get_info_vacancy(vacancy))
            self.parameters['page'] += 1
        return vacancies


class Vacancy:
    def __init__(self, data):
        self.name = data['name']
        self.url = data['url']
        self.description = data['description']
        self.salary = data.get('salary')
        self.date_published = data['date_published']

    def __str__(self):
        return f'Название вакансии - {self.name}, З/П сосавляет - {self.salary()}'


