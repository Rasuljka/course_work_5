import psycopg2

from utils.config import config


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='postgres1', **config())
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cur.execute("""
            SELECT employers.name, COUNT(vacancies.id) AS vacancies_count
            FROM employers
            LEFT JOIN vacancies ON vacancies.employer = employers.id
            GROUP BY employers.name
            ORDER BY vacancies_count DESC;
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        self.cur.execute("""
            SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
            FROM vacancies
            LEFT JOIN employers ON vacancies.employer = employers.id;
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям."""
        self.cur.execute("""
            SELECT AVG(vacancies.salary_from) AS avg_salary
            FROM vacancies;
        """)
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.cur.execute("""
            SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
            FROM vacancies
            LEFT JOIN employers ON vacancies.employer = employers.id
            WHERE vacancies.salary_from > 100000;
        """)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, у которых в названии есть указанное слово."""
        self.cur.execute("""SELECT vacancies.name, vacancies.area, vacancies.salary_from, vacancies.salary_to, 
        vacancies.published_at, vacancies.url, employers.name FROM vacancies LEFT JOIN employers ON 
        vacancies.employer = employers.id WHERE LOWER(vacancies.name) LIKE LOWER('%{}%'); """.format(keyword))
        return self.cur.fetchall()
