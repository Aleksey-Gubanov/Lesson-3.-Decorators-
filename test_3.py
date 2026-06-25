import os
from test_2 import logger  # импортируем декоратор из 2-го задания

# Путь к лог-файлу для этого задания
LOG_PATH = 'task_3.log'

# Удаляем старый лог, если есть (чтобы тесты были чистыми)
if os.path.exists(LOG_PATH):
    os.remove(LOG_PATH)


# ==========================================
# 📦 Классы из СТАРОГО домашнего задания (ООП)
# с примененным декоратором @logger
# ==========================================

class Student:
    """Класс студента."""

    @logger(LOG_PATH)
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    @logger(LOG_PATH)
    def rate_lecture(self, lecturer, course, grade):
        """Выставление оценок лекторам."""
        if isinstance(lecturer, Lecturer) and \
                course in self.courses_in_progress and \
                course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    @logger(LOG_PATH)
    def get_average_grade(self):
        """Подсчет средней оценки за ДЗ."""
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return 0.0
        return sum(all_grades) / len(all_grades)

    @staticmethod
    @logger(LOG_PATH)
    def average_grade_by_course(students_list, course_name):
        """Подсчет средней оценки за ДЗ по всем студентам в рамках курса."""
        if not students_list:
            return 'Список студентов пуст'

        all_grades = []
        for student in students_list:
            if course_name in student.grades:
                all_grades.extend(student.grades[course_name])

        if not all_grades:
            return 'Нет оценок по этому курсу'

        return sum(all_grades) / len(all_grades)

    def __str__(self):
        """Строковое представление студента."""
        avg_grade = self.get_average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) \
            if self.courses_in_progress else 'Нет'
        finished_courses = ', '.join(self.finished_courses) \
            if self.finished_courses else 'Нет'
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade:.1f}\n'
                f'Курсы в процессе изучения: {courses_in_progress}\n'
                f'Завершенные курсы: {finished_courses}')

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()

    def __gt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() > other.get_average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() == other.get_average_grade()


class Mentor:
    """Родительский класс преподавателей."""

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    """Класс лекторов."""

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    @logger(LOG_PATH)
    def get_average_grade(self):
        """Подсчет средней оценки за лекции."""
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return 0.0
        return sum(all_grades) / len(all_grades)

    @staticmethod
    @logger(LOG_PATH)
    def average_grade_by_course(lecturers_list, course_name):
        """Подсчет средней оценки за лекции по всем лекторам в рамках курса."""
        if not lecturers_list:
            return 'Список лекторов пуст'

        all_grades = []
        for lecturer in lecturers_list:
            if course_name in lecturer.grades:
                all_grades.extend(lecturer.grades[course_name])

        if not all_grades:
            return 'Нет оценок по этому курсу'

        return sum(all_grades) / len(all_grades)

    def __str__(self):
        """Строковое представление лектора."""
        avg_grade = self.get_average_grade()
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {avg_grade:.1f}')

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() > other.get_average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() == other.get_average_grade()


class Reviewer(Mentor):
    """Класс экспертов, проверяющих ДЗ."""

    def __init__(self, name, surname):
        super().__init__(name, surname)

    @logger(LOG_PATH)
    def rate_hw(self, student, course, grade):
        """Выставление оценок студентам за ДЗ."""
        if isinstance(student, Student) and \
                course in self.courses_attached and \
                course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        """Строковое представление эксперта."""
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


# ==========================================
# 🧪 Тестовый запуск (демонстрация работы)
# ==========================================
if __name__ == '__main__':
    # ========================================================================
    # СОЗДАНИЕ ОБЪЕКТОВ
    # ========================================================================
    student_1 = Student('Ruoy', 'Eman', 'male')
    student_2 = Student('John', 'Doe', 'male')

    lecturer_1 = Lecturer('Some', 'Buddy')
    lecturer_2 = Lecturer('Ivan', 'Petrov')

    reviewer_1 = Reviewer('Some', 'Buddy')
    reviewer_2 = Reviewer('Anna', 'Smith')

    # ========================================================================
    # НАСТРОЙКА КУРСОВ
    # ========================================================================
    student_1.courses_in_progress += ['Python', 'Git']
    student_1.finished_courses += ['Введение в программирование']
    student_2.courses_in_progress += ['Python', 'Java']

    lecturer_1.courses_attached += ['Python', 'Git']
    lecturer_2.courses_attached += ['Python', 'Java']

    reviewer_1.courses_attached += ['Python', 'Git']
    reviewer_2.courses_attached += ['Python', 'Java']

    # ========================================================================
    # ВЫСТАВЛЕНИЕ ОЦЕНОК (эти вызовы попадут в лог)
    # ========================================================================
    reviewer_1.rate_hw(student_1, 'Python', 10)
    reviewer_1.rate_hw(student_1, 'Python', 9)
    reviewer_1.rate_hw(student_1, 'Git', 8)

    reviewer_2.rate_hw(student_2, 'Python', 7)
    reviewer_2.rate_hw(student_2, 'Python', 8)
    reviewer_2.rate_hw(student_2, 'Java', 9)

    student_1.rate_lecture(lecturer_1, 'Python', 9)
    student_1.rate_lecture(lecturer_1, 'Python', 10)
    student_1.rate_lecture(lecturer_1, 'Git', 9)

    student_2.rate_lecture(lecturer_2, 'Python', 8)
    student_2.rate_lecture(lecturer_2, 'Python', 7)
    student_2.rate_lecture(lecturer_2, 'Java', 10)

    # ========================================================================
    # ВЫВОД РЕЗУЛЬТАТОВ
    # ========================================================================
    print('=' * 60)
    print('ЗАДАНИЕ №3 — ПРИМЕНЕНИЕ ДЕКОРАТОРА К СТАРОМУ ДЗ')
    print('=' * 60)

    print('\n--- Студенты ---')
    print(student_1)
    print()
    print(student_2)

    print('\n--- Лекторы ---')
    print(lecturer_1)
    print()
    print(lecturer_2)

    print('\n--- Сравнение ---')
    print(f'student_1 > student_2: {student_1 > student_2}')
    print(f'lecturer_1 > lecturer_2: {lecturer_1 > lecturer_2}')

    print('\n--- Средние оценки по курсам (статические методы) ---')
    students_list = [student_1, student_2]
    lecturers_list = [lecturer_1, lecturer_2]

    result = Student.average_grade_by_course(students_list, 'Python')
    print(f'Студенты, Python: {result:.2f}')

    result = Lecturer.average_grade_by_course(lecturers_list, 'Python')
    print(f'Лекторы, Python: {result:.2f}')

    print('\n' + '=' * 60)
    print(f'✅ Лог успешно сформирован в файле: {LOG_PATH}')
    print('=' * 60)