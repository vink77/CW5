import psycopg2

class DBManager():
    def __init__(self, filename='my_name'):
        self.filename_db = filename
        self.conn = psycopg2.connect(
            host='localhost',
            database='HH_BASE',
            user='postgres',
            password='9877'
        )

    def get_companies_and_vacancies_count(self):
        '''Получает список всех компаний и количество  вакансий у  каждой компании.'''
        try:
            with self.conn:
                with self.conn.cursor() as cur:

                    cur.execute(f"SELECT company_name, COUNT(company_name) as count_company\
                                FROM {self.filename_db}\
                                GROUP BY company_name\
                                ORDER BY COUNT(company_name) DESC;")
                    rows = cur.fetchall()
                    for row in rows:
                        print(f'В компании "{row[0]}" {"."*(30-len(row[0]))} {row[1]} вакансий')
                    return rows
        finally:
            self.conn.close()


    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.'''
        pass

    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям.'''
        pass
    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
        pass
    def get_vacancies_with_keyword(self):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.'''
        pass