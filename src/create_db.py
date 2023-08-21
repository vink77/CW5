import json
import pandas as pd
import psycopg2
from src.database import password


class Saver:
    """Класс для создания и заполнения таблиц."""

    def __init__(self, vacancies=[], filename='my_name'):
        self.filename_json = f"./{filename}.json"
        self.filename_xls = filename
        self.filename_db = filename
        self.vacancies = vacancies

        self.conn = psycopg2.connect(
            host='localhost',
            database='HH_BASE',
            user='postgres',
            password=password
        )

    def createdb(self) -> None:


        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(f"SELECT EXISTS(SELECT relname from pg_class where relname = '{self.filename_db}' and relkind='r');")
                    rows = cur.fetchall()
                    rows = bool(rows[0][0])
                    if not rows:
                        cur.execute(f"CREATE \
                        TABLE {self.filename_db} (id_vacancies integer,\
                        appointment varchar,\
                        city varchar(38),\
                        company_name varchar(40),\
                        company_url varchar(40),\
                        description varchar,\
                        salary_from integer,\
                        salary_to integer);")

                    cur.execute(f"TRUNCATE TABLE {self.filename_db} RESTART IDENTITY;")
                    for item in self.vacancies:
                        cur.execute(f"INSERT INTO {self.filename_db} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                    [item["id"], item["name"], item["town"],item["firm_name"], item["url"], item["description"], item["salary_from"],item["salary_to"]])
                    print(f'\nДанные сохранены в таблицу  {self.filename_db}\n')
        finally:
            self.conn.close()


















    def write_vacancies_json(self):
        """Метод для добавления вакансий в JSON формате в файл .json"""
        with open(self.filename_json, 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)

    def delete_vacancy_json(self, id):
        """Метод для удаления вакансий из JSON файла .json по id"""
        with open(self.filename_json, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
            new_vacancies = []
            for item in vacancies:
                if str(item['id']) != str(id):
                    new_vacancies.append(item)
        with open(self.filename_json, "w", encoding="utf-8") as file:
            json.dump(new_vacancies, file, ensure_ascii=False, indent=4)

    def write_vacancies_xls(self) -> None:
        """метод для записи в файл-xls"""
        id = []
        name = []
        town = []
        firm_name = []
        url = []
        description = []
        salary_from = []
        salary_to = []

        for item in self.vacancies:
            id.append(item['id'])
            name.append(item['name'])
            town.append(item['town'])
            firm_name.append(item['firm_name'])
            url.append(item['url'])
            description.append(item['description'])
            salary_from.append(item['salary_from'])
            salary_to.append(item['salary_to'])

        df = pd.DataFrame(
            {
                'id': id,
                'name': name,
                'town': town,
                'firm_name': firm_name,
                'url': url,
                'description': description,
                'salary_from': salary_from,
                'salary_to': salary_to
            })
        df.to_excel(f'./{self.filename_xls}.xlsx', index=False)

    def delete_vacancy_xls(self, id):
        """Метод для удаления вакансии из файла my_name.xls по id"""
        new_vacancies = []
        for item in self.vacancies:
            if str(item['id']) != str(id):
                new_vacancies.append(item)
        vacancies = Saver(new_vacancies, self.filename_xls)
        vacancies.write_vacancies_xls()