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

#получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT * FROM my_name
WHERE ABS(salary_to - salary_from)>(SELECT FLOOR(AVG(ABS(salary_to - salary_from))) AS avg_salary
FROM my_name WHERE (salary_to - salary_from)<>0)

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

#проверяет существует ли таблица
SELECT EXISTS (
   SELECT FROM pg_catalog.pg_class c
   JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
   WHERE  n.nspname = 'schema_name'
   AND    c.relname = 'table_name'
   AND    c.relkind = 'r'    -- only tables
   );

SELECT EXISTS(SELECT relname FROM pg_class where relname = my_name and relkind='r');

# Получает среднюю зарплату по вакансиям
SELECT ROUND (((SELECT AVG(salary_from) FROM my_name WHERE salary_from <> 0) +
(SELECT AVG(salary_to) FROM my_name WHERE salary_to <> 0))/2)

#Получает список вакансий с ЗП больше средней по всем вакансиям в таблице
SELECT * FROM my_name
WHERE salary_to > (SELECT ROUND (((SELECT AVG(salary_from) FROM my_name WHERE salary_from <> 0) +
(SELECT AVG(salary_to) FROM my_name WHERE salary_to <> 0))/2))
OR  salary_from > (SELECT ROUND (((SELECT AVG(salary_from) FROM my_name WHERE salary_from <> 0) +
(SELECT AVG(salary_to) FROM my_name WHERE salary_to <> 0))/2));