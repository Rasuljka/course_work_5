from classes.dbmanager import DBManager

db = DBManager()

print("Привет! Я менеджер базы данных DBManager\nВведите номер задачи, которую хотите выполнить:\n")

while True:
    user_input = input("1 - получить список компаний и количество вакансий\n"
                       "2 - получить все вакансии\n"
                       "3 - получить среднюю зарплату\n"
                       "4 - получить список всех вакансий с зарплатой выше средней\n"
                       "5 - искать вакансии по ключевому слову\n")

    if user_input == "1":
        for i in db.get_companies_and_vacancies_count():
            print(i)

    elif user_input == "2":
        for i in db.get_all_vacancies():
            print(i)

    elif user_input == "3":
        for i in db.get_avg_salary():
            print(i)

    elif user_input == "4":
        for i in db.get_vacancies_with_higher_salary():
            print(i)

    elif user_input == "5":
        user_input = input("Введите ключевое слово: ")
        for i in db.get_vacancies_with_keyword(user_input):
            print(i)

    else:
        print("Вы ввели некорректный номер задачи. Попробуйте еще раз.")

    user_input_1 = input("Хотите ли вы продолжить работу с менеджером базы? (y/n): ")
    if user_input_1 == "y":
        continue
    elif user_input_1 == "n":
        print("До свидания!")
        break
