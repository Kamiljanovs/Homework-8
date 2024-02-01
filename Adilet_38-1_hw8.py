import sqlite3

def create_table_countries(connection):
    with connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS countries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        ''')

def insert_countries_data(connection, data):
    with connection:
        connection.executemany('INSERT INTO countries (title) VALUES (?)', data)

def create_table_cities(connection):
    with connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                area REAL DEFAULT 0,
                country_id INTEGER,
                FOREIGN KEY (country_id) REFERENCES countries(id)
            )
        ''')

def insert_cities_data(connection, data):
    with connection:
        connection.executemany('INSERT INTO cities (title, country_id) VALUES (?, ?)', data)

def create_table_students(connection):
    with connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                city_id INTEGER,
                FOREIGN KEY (city_id) REFERENCES cities(id)
            )
        ''')

def insert_students_data(connection, data):
    with connection:
        connection.executemany('INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)', data)

def main():
    with sqlite3.connect('new.db') as connection:
        create_table_countries(connection)
        insert_countries_data(connection, [('Кыргызстан',), ('Германия',), ('Италия',)])

        create_table_cities(connection)
        insert_cities_data(connection, [('Бишкек', 1), ('Берлин', 2), ('Мюнхен', 2), ('Ош', 1), ('Рим', 3), ('Милан', 3), ('Париж', 0)])

        create_table_students(connection)
        insert_students_data(connection, [('Адилет', 'Камилжанов', 1), ('Бексултан', 'Жолонов', 2), ('Мирлан', 'Бурканов', 3),
                                          ('Актилек', 'Абдилалиев', 4), ('Жанат', 'Алымбеков', 5), ('Мирзат', 'Мусаев', 6),
                                          ('Тологон', 'Иманбеков', 7), ('Бийбол', 'Раимбаев', 1), ('Атай', 'Акыбаев', 2),
                                          ('Байсал', 'Калыков', 3), ('Нурадил', 'Насиров', 4), ('Баястан', 'Ыскаков', 5),
                                          ('Нур-Мухаммед', 'Жанболотов', 6), ('Азамат', 'Эргешов', 7), ('Бекзат', 'Касенов', 1)])

    while True:
        print("Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")

        with sqlite3.connect('new.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT id, title FROM cities')
            cities = cursor.fetchall()
            for city in cities:
                print(f"{city[0]}. {city[1]}")

        selected_city_id = int(input("Введите id города (0 для выхода): "))
        if selected_city_id == 0:
            break

        with sqlite3.connect('new.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT students.first_name, students.last_name, countries.title, cities.title, cities.area
                FROM students
                JOIN cities ON students.city_id = cities.id
                JOIN countries ON cities.country_id = countries.id
                WHERE cities.id = ?
            ''', (selected_city_id,))
            students_info = cursor.fetchall()

            if students_info:
                print(f"\nУченики в городе {students_info[0][3]}, {students_info[0][2]}:")
                for student in students_info:
                    print(f"Имя: {student[0]}, Фамилия: {student[1]}, Площадь города: {student[4]}")
            else:
                print("Нет информации о учениках в выбранном городе.")

if __name__ == "__main__":
    main()
