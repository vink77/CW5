from abc import ABC, abstractmethod
import requests


class API(ABC):
    def __init__(self, url, num_vacancies=30):
        self.url = url
        self.num_vacancies = num_vacancies

    @abstractmethod
    def search(self, request_job):
        """абстрактный метод поиска вакансий с платформ"""
        pass

    @staticmethod
    def string_convert(string: str):
        """
        Метод для удаления ненужных символов из строки
        :param string: строка для конвертации
        :return: строка без лишних символов
        """
        symbols = ['  ', '   ', '\n', '</p>', '<p>', '</li>', '<li>', '<b>', '</b>', '<ul>', '<li>', '</li>', '<br />',
                   '</ul>', '<highlighttext>', '·']
        try:
            for symb in symbols:
                string = string.replace(symb, " ")
        except AttributeError:
            return 'не указано'
        return string


class HHApi(API):
    """класс получения данных с платформы HH.ru"""
    result = []

    def __init__(self, url='https://api.hh.ru/vacancies'):
        self.url = url
        super().__init__(url)

    def search(self, request_job, city):
        """метод поиска вакансий с платформы HH"""
        town_hh = [1, 2, 47, 4]
        params = {
            'text': request_job,
            'area': town_hh[city - 1],
            'employer_id': [1740, 2180, 78638],
            'pages': 0,
            'per_page': self.num_vacancies}
        response = requests.get(self.url, params).json()

        # if response.status_code == 200:
        result = []
        salary_from = salary_to = 0
        for item in response['items']:
            salary = item.get('salary', {})
            if salary == None:
                salary_from = 0
                salary_to = 0
            elif item['salary']['from'] == None:
                salary_from = 0
            elif item['salary']['to'] == None:
                salary_to = 0
            else:
                salary_from = salary.get('from')
                salary_to = salary.get('to')
            result.append({
                "id": item["id"],
                "name": item['name'],
                "town": item['area']['name'],
                "firm_name": item['employer']['name'],
                "url": item['alternate_url'],
                "description": API.string_convert(item['snippet']['requirement']),
                "salary_to": salary_to,
                "salary_from": salary_from}
            )
        return result


class SJApi(API):
    """класс получения данных с платформы SuperJob.ru"""

    def __init__(self, url='https://api.superjob.ru/2.0/vacancies'):
        self.url = url
        super().__init__(url)

    def search(self, request_job, city):
        """метод поиска вакансий с платформы SJ"""

        # api_key: str = os.getenv('Sjob_API_KEY')
        dict_town_sj = {1: "Москва", 2: "Санкт-Петербург", 3: "Кемерово", 4: "Новосибирск"}
        # town_sj = dict_town_sj[city]

        headers = {
            'X-Api-App-Id':
                'v3.r.137478329.0484df93bd0dbe1d4ec473961f0e68359d16d3f6.0ab6ee7c38c6375a5deb84c35464cc67b7b4c44b'
        }

        params = {
            "keywords": [request_job],
            "count": self.num_vacancies,
            "town": dict_town_sj[city]
        }

        response = requests.get(self.url, headers=headers, params=params).json()
        print(response)

        result = []
        for item in response['objects']:
            result.append({
                "id": item['id'],
                "name": item['profession'],
                "town": item['town']['title'],
                "firm_name": item['firm_name'],
                "url": item['link'],
                "description": API.string_convert(item['vacancyRichText']),
                "salary_to": item['payment_to'],
                "salary_from": item['payment_from']}
            )
        return result