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
        command=  f"SELECT company_name, COUNT(company_name) as count_company FROM {self.filename_db} GROUP BY company_name ORDER BY COUNT(company_name) DESC;"
        DBManager.get_command(self, command)

    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.'''
        command=  f"SELECT * FROM {self.filename_db};"
        DBManager.get_command(self, command)

    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям.'''
        command = f"SELECT * FROM {self.filename_db};"
        DBManager.get_command(self, command)
    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
        command = f"SELECT * FROM {self.filename_db};"
        DBManager.get_command(self, command)
    def get_vacancies_with_keyword(self, keyword):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.'''
        command = f"SELECT * FROM {self.filename_db} WHERE appointment LIKE '%{keyword}%';"
        DBManager.get_command(self, command)


    def get_command(self, command):
        '''Выводит в консоль результат полученной в метод SQL-комманды.'''
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(command)
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
                    return rows
        finally:
            self.conn.close()