class Student:
    all_students = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student.all_students.append(self)

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname} \
                 \nСредняя оценка за домашние задания: {self.average_grade()} \
                 \nКурсы в порцессе изучения: {", ".join(self.courses_in_progress)} \
                 \nЗвершенные курсы: {", ".join(self.finished_courses) if self.finished_courses else "Пока нету"}'

    def __lt__(self, other):
        return self.average_grade() < other.average_grade()

    def average_grade(self):
        if self.grades:
            all_grades = [i for j in self.grades.values() for i in j]
            return sum(all_grades) / len(all_grades)
        else:
            return 0

    def rate_teacher(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in self.courses_in_progress
                and course in lecturer.courses_attached):
            if course in lecturer.grades_from_students:
                lecturer.grades_from_students[course] += [grade]
            else:
                lecturer.grades_from_students[course] = [grade]
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        print('Only reviewers can grade students')


class Lecturer(Mentor):
    all_lecturers = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_from_students = {}
        Lecturer.all_lecturers.append(self)

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname} \
         \nСредняя оценка за лекции: {self.average_grade_from_students()}'

    def __lt__(self, other):
        return self.average_grade_from_students() < other.average_grade_from_students()

    def average_grade_from_students(self):
        if self.grades_from_students:
            all_grades = [i for j in self.grades_from_students.values() for i in j]
            return sum(all_grades) / len(all_grades)
        else:
            return 0


class Reviewer(Mentor):
    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def average_students_grade(all_students, searched_course):
    all_grades = []
    for student in all_students:
        if searched_course in student.grades:
            all_grades += student.grades[searched_course]
    if not all_grades:
        return 'Такой курс еще не оценивали'
    return sum(all_grades) / len(all_grades)


def average_lecturers_grade(all_lecturers, searched_course):
    all_grades = []
    for lecturer in all_lecturers:
        if searched_course in lecturer.grades_from_students:
            all_grades += lecturer.grades_from_students[searched_course]
    if not all_grades:
        return 'Такой курс еще не оценивали'
    return sum(all_grades) / len(all_grades)


best_student = Student('Best', 'Student', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['Java']
best_student.finished_courses += ['Kotlin']

cool_reviewer = Reviewer('Cool', 'Reviewer')
cool_reviewer.courses_attached += ['Python']
cool_reviewer.courses_attached += ['Java']

cool_lecturer = Lecturer('Cool', 'Lecturer')
cool_lecturer.courses_attached += ['Python']
cool_lecturer.courses_attached += ['Java']

cool_reviewer.rate_hw(best_student, 'Python', 8)
cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Java', 7)
cool_reviewer.rate_hw(best_student, 'Java', 5)

cool_lecturer.rate_hw(best_student, 'Python', 10)  # Checking that only reviewers can grade students

bad_student = Student('Bad', 'Student', 'your_gender')

bad_student.courses_in_progress += ['Python']
bad_student.courses_in_progress += ['Java']

cool_reviewer.rate_hw(bad_student, 'Python', 3)
cool_reviewer.rate_hw(bad_student, 'Python', 2)
cool_reviewer.rate_hw(bad_student, 'Java', 1)
cool_reviewer.rate_hw(bad_student, 'Java', 2)

bad_lecturer = Lecturer('Bad', 'lecturer')

print('-----------------------------')
print(best_student.grades)

best_student.rate_teacher(cool_lecturer, 'Python', 7)
best_student.rate_teacher(cool_lecturer, 'Python', 8)
best_student.rate_teacher(cool_lecturer, 'Java', 10)
best_student.rate_teacher(cool_lecturer, 'Java', 5)

print('-----------------------------')
print(cool_lecturer.grades_from_students)

print('-----------------------------')
print(cool_reviewer)
print('-----------------------------')
print(cool_lecturer)
print('-----------------------------')
print(best_student)
print('-----------------------------')

print(bad_lecturer < cool_lecturer)
print('-----------------------------')

print(bad_student < best_student)
print('-----------------------------')

print(average_students_grade(Student.all_students, 'Python'))
print(average_lecturers_grade(Lecturer.all_lecturers, 'Python'))
