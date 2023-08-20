from src.api import HHApi
from src.create_db import Saver
from src.db import DBManager
from src.functions import Vacancy
from src.load_file import Loader
import os

# 1740 Яндекс
# 40565 Google Inc.
# 3529 Сбер
# 15478 VK
# 78638 Тинькофф
# 740 Норильский никель
# 3388 Газпромбанк
# 23186 Русагро
# 3776 МТС Диджитал
# 6041 Северсталь
# 4233 X5 Group
# 2180 Ozon
# 115 АйТеко
# 566 OCS Distribution
# 2748 Ростелеком

class Job():
    """Класс взаимодействия с пользователем"""
    SALARY_FROM = 100000  # Константы зарплат для фильтров
    SALARY_TO = 150000  # Константы зарплат для фильтров
    EMPLOYERS = [1235466, 2748, 40565, 3529, 15478, 2180, 78638, 740, 3388, 3388, 23186, 3776, 6041, 4233, 115, 566, 2748, 1740]
    hh_api = HHApi()
    file_name = 'my_name'
    result_all = []
    while True:
        print(f"\n{' ' * 8}ОСНОВНОЕ МЕНЮ\n\
1. найти и вывести список вакансий с ресурсов HH.ru \n\
2. МЕНЮ работы с Базой Данных HH_BASE\n\
3. МЕНЮ работы с файлом xlsx\n\
4. МЕНЮ фильтров \n\
5. выйти")
        choiсe = input("Ваш выбор - ")
        if choiсe == '1':
            result_all = []
            platforms = [HHApi()]
            for item in platforms:
                result = item.search(EMPLOYERS)
                result_all.extend(result)
            vacancy = Vacancy(result_all)
            vacancy.output_vacancies()
        if choiсe == "2":
            while True:
                print(f"\n{' ' * 8} МЕНЮ работы с ТАБЛИЦЕЙ  {file_name}  БАЗЫ ДАННЫХ\n\
1. сохранить вакансии в базу данных\n\
2. показать вакансии из таблицы БАЗЫ ДАННЫХ\n\
3. Получает список всех компаний и количество вакансий у каждой компании.\n\
4. Получает список всех вакансий, в названии которых содержится заданное слова\n\
5. получает среднюю зарплату по вакансиям\n\
6. получает список всех вакансий, у которых зарплата выше средней по всем вакансиям\n\
7. удалить таблицу\n\
8. удалить данные из таблицы\n\
9. задать имя таблицы БАЗЫ ДАННЫХ\n\
0. выход в основное меню\n")
                choiсe_file = input("     Ваш выбор: ")

                if choiсe_file == "1":  #сохранить вакансии в базу данных
                    write = Saver(result_all, file_name)
                    write.createdb()
                if choiсe_file == "2":  #Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
                    write = DBManager(file_name)
                    write.get_all_vacancies()
                if choiсe_file == "3":   #Получает список всех компаний и количество вакансий у каждой компании.
                    write = DBManager(file_name)
                    write.get_companies_and_vacancies_count()
                if choiсe_file == "4":    #Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
                    keyword = input('Введите ключевое слово для поиска: ')
                    write = DBManager(file_name)
                    write.get_vacancies_with_keyword(keyword)
                if choiсe_file == "5":    #получает среднюю зарплату по вакансиям.
                    write = DBManager(file_name)
                    write.get_avg_salary()
                if choiсe_file == "6":    #получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
                    write = DBManager(file_name)
                    write.get_vacancies_with_higher_salary()
                if choiсe_file == "7":    # удалить таблицу
                    write = DBManager(file_name)
                    write.delete_table()
                if choiсe_file == "8":   # удалить данные из таблицы
                    write = DBManager(file_name)
                    write.clear_table()
                if choiсe_file == "9":  # задать имя таблицы
                    file_name = input("Введите имя таблицы :")
                if choiсe_file == "0":   #выход в основное меню
                    break

        if choiсe == "3":
            while True:
                print(f"\n{' ' * 8} МЕНЮ работы с файлом {file_name}.xlsx\n\
1. сохранить вакансии в файл xls\n\
2. удалить вакансию из файла xls по id\n\
3. показать вакансии из файла xls\n\
4. задать имя файла xls\n\
5. удалить файл xls\n\
6. выход в основное меню")
                choiсe_file = input("     Ваш выбор: ")
                if choiсe_file == "1":
                    write = Saver(result_all, file_name)
                    write.write_vacancies_xls()
                    if os.path.isfile(f'./{file_name}.xlsx'):
                        print(f"файл {file_name}.xlsx сохранен!")
                if choiсe_file == "2":
                    if os.path.isfile(f'./{file_name}.xlsx'):
                        id = input("id для удаления ")
                        result = Loader(file_name)
                        Saver(result.get_vacancies_xls()).delete_vacancy_xls(id)
                if choiсe_file == "3":  # показать вакансии из файла xlsx
                    if os.path.isfile(f'./{file_name}.xlsx'):
                        result_all = Loader(file_name)
                        Vacancy(result_all.get_vacancies_xls()).output_vacancies()
                if choiсe_file == "4":
                    file_name = input("Введите имя файла без расширения :")
                if choiсe_file == "5":  # удалить файл xlsx
                    if os.path.isfile(f'./{file_name}.xlsx'):
                        os.remove(f'./{file_name}.xlsx')
                        print(f"файл {file_name}.xlsx удалён ")
                if choiсe_file == "6":
                    break
        if choiсe == "4":
            if result_all != []:
                print(f"\n{' ' * 8} МЕНЮ работы с фильтрами\n\
1. Упорядочить список по зарплате < ОТ >\n\
2. Упорядочить список по зарплате < ДО >\n\
3. Показать список вакансий с зарплатой {SALARY_FROM} - {SALARY_TO} руб.\n\
4. Показать список вакансий с зарплатой 0 - {SALARY_FROM} руб.\n\
5. Удалить из списка вакансии без указания зарплаты\n\
6. выход в основное меню")
                choiсe_filter = input("     Ваш выбор: ")
                if choiсe_filter == "1" or choiсe_filter == "2":
                    dict_choice = {"1": "salary_from", "2": 'salary_to'}
                    vacancy = Vacancy(result_all)
                    result_all = vacancy.sort_list(dict_choice[choiсe_filter])
                    Vacancy(result_all).output_vacancies()
                if choiсe_filter == "3":
                    vacancy = Vacancy(result_all)
                    result_all = vacancy.filter_salary(SALARY_FROM, SALARY_TO)
                    Vacancy(result_all).output_vacancies()
                if choiсe_filter == "4":
                    vacancy = Vacancy(result_all)
                    result_all = vacancy.filter_salary(0, SALARY_FROM)
                    Vacancy(result_all).output_vacancies()
                if choiсe_filter == "5":
                    vacancy = Vacancy(result_all)
                    result_all = vacancy.filter_salary_zero()
                    Vacancy(result_all).output_vacancies()
                if choiсe_filter == "6":
                    pass
            else:
                print('Необходимо сначала получить список вакансий!!')
        if choiсe == '5':
            break