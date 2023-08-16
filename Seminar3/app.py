# Задание №1
# Создать базу данных для хранения информации о студентах университета.
# База данных должна содержать две таблицы: "Студенты" и "Факультеты".
# В таблице "Студенты" должны быть следующие поля: id, имя, фамилия,
# возраст, пол, группа и id факультета.
# В таблице "Факультеты" должны быть следующие поля: id и название
# факультета.
# Необходимо создать связь между таблицами "Студенты" и "Факультеты".
# Написать функцию-обработчик, которая будет выводить список всех
# студентов с указанием их факультета.

from flask import Flask, render_template
from models import db, Student, Faculty, Book, Author

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("add-student")
def add_student():
    for i in range(1, 21):
        student = Student(name=f'Имя{i}', last_name=f'Фамилия{i}', age=17 + i, gender='Женский' if i % 2 else 'Мужской',
                          group=i // 5, faculty_id=i // 4)
        db.session.add(student)
    db.session.commit()
    print('Student is added to DB!')


@app.cli.command("add-faculty")
def add_faculty():
    for i in range(1, 6):
        faculty = Faculty(faculty_name=f'Факуьтет{i}')
        db.session.add(faculty)
    db.session.commit()
    print('Faculty is added to DB!')


@app.cli.command("add-book")
def add_book():
    for i in range(1, 21):
        book = Book(name=f'Книга{i}', year=f'{1800 + i}', amount=100 + i, author_id=i // 4 + 1)
        db.session.add(book)
    db.session.commit()
    print('Book is added to DB!')


@app.cli.command("add-author")
def add_author():
    for i in range(1, 6):
        author = Author(name=f'Автор{i}', last_name=f'Книгов{i}')
        db.session.add(author)
    db.session.commit()
    print('Author is added to DB!')


@app.route('/university/')
def get_students():
    students = Student.query.all()
    faculties = Faculty.query.all()
    context = {'students': students, 'faculties': faculties}
    return render_template('university.html', **context)


@app.route('/library/')
def get_books():
    books = Book.query.all()
    authors = Author.query.all()
    context = {'books': books, 'authors': authors}
    return render_template('library.html', **context)
