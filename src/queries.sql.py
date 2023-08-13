#
DROP TABLE my_name

#Удалить все данные из таблицы со сбросом идентификатор в исходное состояние
TRUNCATE TABLE my_name RESTART IDENTITY;

#вывести все данные из таблицы
SELECT * FROM my_name

#вывести все вакансии  из таблицы отсортированные по городам
SELECT * FROM my_name
GROUP BY city

#вывести все вакансии  из москвы
SELECT * FROM my_name
WHERE city = 'Москва'


#количество вакансий в каждом из городов, отсортированный по кол-ву вакансий по убыванию
SELECT city, COUNT(city) as count_city
FROM my_name
GROUP BY city
ORDER BY COUNT(city) DESC;

#количество вакансий  по работодателям, отсортированный по кол-ву вакансий по убыванию
SELECT company_name, COUNT(company_name) as count_company
FROM my_name
GROUP BY company_name
ORDER BY COUNT(company_name) DESC;

#создание таблицы my_name
CREATE TABLE my_name (id_vacancies integer,
                        appointment varchar,
                        city varchar(38),
                        company_name varchar(40),
                        description varchar,
                        salary_from integer,
                        salary_to integer)