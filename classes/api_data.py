import requests


class HHParser:
    def get_request(self):
        params = {
            "per_page": 10,
            "sort_by": "by_vacancies_open"
        }
        response = requests.get(f"https://api.hh.ru/employers", params=params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            print("Произошла ошибка при выполнении запроса.")

    def get_employers(self):
        data = self.get_request()
        employers = []
        for employer in data:
            employers.append({'id': employer['id'], 'name': employer['name']})
        return employers

    def get_vacancies(self, id_company):
        params = {
            "per_page": 10,
            "employer_id": id_company
        }
        response = requests.get(f"https://api.hh.ru/vacancies", params=params)
        if response.status_code == 200:
            return response.json()['items']

    def get_all_vacancies(self):
        employers = self.get_employers()
        vacancies = []
        for employer in employers:
            vacancies.extend(self.get_vacancies(employer['id']))
        return vacancies

    def filter_vacancies(self):
        vacancies = self.get_all_vacancies()
        filter_data = []
        for vacancy in vacancies:
            if not vacancy['salary']:
                salary_from = 0
                salary_to = 0
            else:
                salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0
            filter_data.append({
                'id': vacancy['id'],
                'name': vacancy['name'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'published_at': vacancy['published_at'],
                'url': vacancy['alternate_url'],
                'area': vacancy['area']['name'],
                'employer': vacancy['employer']['id']
            })
        return filter_data
