import json, pandas

class Loader:
    """Класс для сохранения информации о вакансиях в JSON и XLS -файл."""
    FILE_NAME = "my_name"

    def __init__(self, filename=FILE_NAME):
        self.filename_json = f"./{filename}.json"
        self.filename_xls = filename

    def get_vacancies_json(self):
        """Метод для получения вакансий из файла my_name.json"""
        with open(self.filename_json, 'r', encoding='utf-8') as file:
            result_all = json.load(file)
            return result_all

    def get_vacancies_xls(self):
        """Метод для получения вакансий из файла my_name.xlsx"""
        excel_data_df = pandas.read_excel(f'./{self.filename_xls}.xlsx')
        result_all = excel_data_df.to_json(orient='records', force_ascii=False)
        result_all = json.loads(result_all)
        return result_all