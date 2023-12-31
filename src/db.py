import psycopg2
from src.database import password
class DBManager():
    def __init__(self, filename='my_name'):
        self.filename_db = filename
        self.conn = psycopg2.connect(host='localhost',
            database='HH_BASE',
            user='postgres',
            password=password)

    def get_companies_and_vacancies_count(self):
        '''Получает список всех компаний и количество  вакансий у  каждой компании.'''
        command=  f"SELECT company_name, COUNT(company_name) as count_company FROM {self.filename_db} GROUP BY company_name ORDER BY COUNT(company_name) DESC;"
        DBManager.get_command(self, command)

    def get_all_vacancies(self):
        '''Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.'''
        command=  f"SELECT * FROM {self.filename_db};"
        DBManager.get_command(self, command)

    def get_avg_salary(self):
        '''Получает среднюю зарплату по вакансиям.'''
        command = f"SELECT ROUND (((SELECT AVG(salary_from) FROM {self.filename_db} WHERE salary_from <> 0) +\
                   (SELECT AVG(salary_to) FROM {self.filename_db} WHERE salary_to <> 0))/2) ;"
        print("Средняя зарплата по вакансиям")
        DBManager.get_command(self, command)

    def get_vacancies_with_higher_salary(self):
        '''Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
        command = f"SELECT * FROM {self.filename_db} \
                    WHERE salary_to > (SELECT ROUND (((SELECT AVG(salary_from) FROM {self.filename_db} WHERE salary_from <> 0) +\
                   (SELECT AVG(salary_to) FROM {self.filename_db} WHERE salary_to <> 0))/2))\
                    OR  salary_from > (SELECT ROUND (((SELECT AVG(salary_from) FROM {self.filename_db} WHERE salary_from <> 0) +\
                   (SELECT AVG(salary_to) FROM {self.filename_db} WHERE salary_to <> 0))/2));"
        DBManager.get_command(self, command)

    def get_vacancies_with_keyword(self, keyword):
        '''Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.'''
        command = f"SELECT * FROM {self.filename_db} WHERE LOWER(appointment) LIKE '%{keyword}%';"
        DBManager.get_command(self, command)

    def delete_table(self):
        """Метод для удаления таблицы из БД"""
        command = f"DROP TABLE {self.filename_db};"
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(command)
            print(f"Таблица {self.filename_db} удалена")
        except ValueError:
            print("Error")
        finally:
            self.conn.close()
    def clear_table(self):
        """Метод для удаления данных из таблицы"""
        command = f"TRUNCATE TABLE {self.filename_db} RESTART IDENTITY;"
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(command)
        finally:
            self.conn.close()


    def get_command(self, command):
        '''Выводит в консоль результат полученной в метод SQL-комманды.'''
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        f"SELECT EXISTS(SELECT relname from pg_class where relname = '{self.filename_db}' and relkind='r');")
                    rows = cur.fetchall()
                    rows = bool(rows[0][0])
                    if rows:
                        cur.execute(command)
                        rows = cur.fetchall()
                        for row in rows:
                            print(str(row))
                        print(f'\nКоличество результатов - {len((rows))}\n')
                    else:
                        print(f'Таблица {self.filename_db} еще не создана')
                    return rows
        finally:
            self.conn.close()