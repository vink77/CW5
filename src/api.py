from abc import ABC, abstractmethod
import requests


class API(ABC):

    def __init__(self, url, num_vacancies=100):
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
                   '</ul>', '<highlighttext>', '</highlighttext>', '·']
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

    def get_vacancies(self, EMPLOYERS, page = 1):

        """метод поиска вакансий с платформы HH"""
        params = {
            'employer_id': EMPLOYERS,
            'page': page,
            'per_page': self.num_vacancies}
        response = requests.get(self.url, params).json()
        return response

    def search(self, EMPLOYERS, page = 1):
        result = []
        salary_from = salary_to = 0
        for page in range(5): #количество вакансий
            response = self.get_vacancies(EMPLOYERS,page)
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


