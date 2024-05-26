import psycopg2
from config import config
from classes.api_data import HHParser


def create_database(db_name):
    """Создает базу данных"""
    conn = psycopg2.connect(dbname='test', **config())
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()


def create_tables(db_name):
    """Создает таблицы в базе данных"""
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE employers'
                        '('
                        'id int PRIMARY KEY,'
                        'name varchar(255) UNIQUE NOT NULL)')
            cur.execute('CREATE TABLE vacancies'
                        '('
                        'id int PRIMARY KEY,'
                        'name varchar(255) NOT NULL,'
                        'area varchar(255),'
                        'salary_from int,'
                        'salary_to int,'
                        'published_at timestamp,'
                        'url varchar(255),' 
                        'employer int REFERENCES employers (id) NOT NULL)')
    conn.close()


def insert_data_into_tables(db_name):
    """Заполняет таблицы данными"""
    hh = HHParser()
    employers = hh.get_employers()
    vacancies = hh.filter_vacancies()
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("""
                                INSERT INTO employers VALUES (%s, %s)
                                ON CONFLICT (id) DO NOTHING;
                            """, (employer['id'], employer['name']))
            for vacancy in vacancies:
                cur.execute("""
                                INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (id) DO NOTHING;
                                """, (vacancy['id'], vacancy['name'], vacancy['area'],
                                      vacancy['salary_from'], vacancy['salary_to'],
                                      vacancy['published_at'], vacancy['url'], vacancy['employer']))
    conn.close()


db_name = 'postgres1'
create_database(db_name)
create_tables(db_name)
insert_data_into_tables(db_name)
