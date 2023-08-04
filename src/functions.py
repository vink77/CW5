class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, vacancies):
        self.vacancies = vacancies

    def output_vacancies(self):
        """ метод вывода списка вакансий в консоль"""
        # подготовка поля /description/ к читабельному виду
        for item in self.vacancies:
            s1 = f"Описание: {item['description']}".split(' ')
            s3 = []
            num = 150
            l = num
            for i in s1:
                s3.append(i)
                if len(''.join(s3)) > l:
                    l += num
                    s3.append('\n')
            salary_from_text = '' if int(item['salary_from']) == 0 else f"от: {item['salary_from']}"
            salary_to_text = '' if int(item['salary_to']) == 0 else f"до: {item['salary_to']}"
            if int(item['salary_from']) == 0 and int(item['salary_to']) == 0:
                salary_from_text = 'не указана'
            print(f"\nid: {item['id']}\n"
                  f"Должность: {item['name']}\n"
                  f"Город :{item['town']}\n"
                  f"Фирма: {item['firm_name']}\n"
                  f"URL: {item['url']}\n"
                  f"Зарплата {salary_from_text} {salary_to_text}")
            print(' '.join(s3))
        print(f"\nНайдено {len(self.vacancies)} вакансий")

    def sort_list(self, sort_pool):
        """ сортировка списка "vacancies" по <от> или <до>"""
        sorting = sorted(self.vacancies, key=lambda x: x[sort_pool], reverse=True)
        return sorting

    def filter_salary(self, salary_from, salary_to):
        """ фильтрация спискаа "vacancies" по зарплате <от> и/или <до>"""
        result_all = []
        for item in self.vacancies:
            if int(item['salary_from']) >= salary_from and int(item['salary_to']) <= salary_to and int(
                    item['salary_from']) <= salary_to:
                result_all.append(item)
        return result_all

    def filter_salary_zero(self):
        """ фильтрация спискаа "vacancies" по зарплате <от> и/или <до>"""
        result_all = []
        for item in self.vacancies:
            if int(item['salary_from']) != 0 or int(item['salary_to']) != 0:
                result_all.append(item)
        return result_all