from csv import reader
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from os import environ
from os.path import exists, join
from re import compile

from tool.days import parse_date
from tool.document import fix_images, read_markdown
from tool.files import recursive_list
from tool.log import log_exception
from tool.shell import banner
from tool.text import text_join
from tool.user import add_user_login
from unc.models import Course, Project, Lesson, Skill, Student
from unc.projects import add_project, list_assignments


def add_lesson(course, row):
    # CSV Data -- Week, Day, Date, Lesson, Topic, Reading, Projects, Process, Parts
    # print(row)
    project = add_project(course, row)
    date = make_aware(parse_date(row[2]))
    num = row[3] if row[3] != '' else '-1'
    x = Lesson.objects.filter(course=project.course, date=date)
    if len(x)> 1:
        print (x)
    lesson = Lesson.objects.get_or_create(course=project.course, date=date)[0]
    lesson.week = row[0]
    lesson.lesson = num
    lesson.project = project
    lesson.topic = row[4]
    lesson.reading = zybooks_link(course[-3:], row[5])
    lesson.save()
    return lesson


def add_student(first, last, email, domain, course):
    course = Course.lookup(course)
    name = '%s %s' % (first, last)
    s = Student.objects.get_or_create(name=name, email=email, course=course)[0]
    u = add_user_login(first, last, email)
    s.user = u
    s.domain = domain
    s.save()
    return s


def add_teacher():
    course_name = 'bacs200'
    name = 'MarkSeaman'
    email = 'mark.b.seaman@gmail.com'
    domain = r'https://unco-bacs.org'
    c = Course.lookup(course_name)
    u = User.objects.get(username=name)
    s = Student.objects.get_or_create(name=name, email=email, course=c, user=u)[0]
    s.user = u
    s.domain = domain
    s.save()


def create_course(name, title, teacher, description):
    return Course.objects.get_or_create(name=name, title=title, teacher=teacher, description=description)[0]

'''
from unc.bacs import *
drop_students()
'''

def drop_students():
    for f in ['Max Lloyd', 'Michael Koval', 'Deisy Guzman', 'Shalom Ekumbo']:
        try:
            s = Student.lookup(f)
            print(s)
            s.user.delete()
            s.delete()
        except:
            print("No student: "+f)


def fix_domain_protocols():
    for s in Student.objects.all():
        if s.domain != 'No Domain Configured' and not s.domain.startswith('http'):
            s.domain = 'http://' + s.domain
            s.save()
            print(s.domain)


def get_student(request):
    try:
        if not request.user.is_anonymous:
            return Student.objects.get(user=request.user)
    except:
        log_exception('Cannot find student record, %s' % str(request.user))


def import_all_students():
    import_students('bacs350')
    import_students('bacs200')
    print(text_join([list_students(c) for c in unc_courses()]))


def import_students(course):
    def read_students(course):
        data_file = 'Documents/unc/%s/students.csv' % course
        with open(data_file) as f:
            return [row for row in reader(f)]

    def display_student(course, first, last, email):
        print('%s, "%s_%s", %s' % (course, first, last, email))

    table = read_students(course)
    if course == 'bacs200':
        for row in table[2:]:
            # print(row)
            name = row[0].split(' ')
            first, last, email = name[0], ' '.join(name[1:]), row[3]
            display_student(course, first, last, email)
            add_student(first, last, email, 'No Domain Configured', course)
    else:
        for row in table[2:-1]:
            # print(row)
            name = row[0].split(' ')
            first, last, email = name[0], ' '.join(name[1:]), row[3]
            display_student(course, first, last, email)
            add_student(first, last, email, 'No Domain Configured', course)


def import_schedule(course):
    table = read_schedule(course)
    for row in table[2:]:
        add_lesson(course, row)
    return text_join(Lesson.list(course))


def import_test_students():
    course = 'cs350'
    add_student('Tony', 'Stark', 'mark.b.seaman+iron_man@gmail.com', r'https://unco-bacs.org/iron_man', course)
    add_student('Natasha', 'Romanov ', 'mark.b.seaman+black_widow@gmail.com', r'https://unco-bacs.org/black_widow',
                course)
    add_student('Bruce', 'Banner', 'mark.b.seaman+hulk@gmail.com', r'https://unco-bacs.org/hulk', course)
    add_student('Steve', 'Rogers', 'mark.b.seaman+cap@gmail.com', r'https://unco-bacs.org/cap_america', course)
    add_student('Carol', 'Danvers', 'mark.b.seaman+marvel@gmail.com', r'https://unco-bacs.org/cap_marvel', course)
    add_student('Wanda', 'Maximoff', 'mark.b.seaman+witch@gmail.com', r'https://unco-bacs.org/scarlet_witch', course)
    add_student('Sensei', '200', 'mark.b.seaman+200@gmail.com', r'https://unco-bacs.org', 'bacs200')
    add_student('Sensei', '350', 'mark.b.seaman+350@gmail.com', r'https://unco-bacs.org', 'bacs350')


def initialize_data():
    create_course('cs350', 'Software Engineering (under development)', 'Mark Seaman',
                  'This class is for test purposes only')
    create_course('bacs200', 'Web Development Intro (Fall 2019)', 'Mark Seaman',
                  'Web Design and Development for Small Business')
    create_course('bacs350', 'Web Development Intermediate (Fall 2019)', 'Mark Seaman',
                  'Intermediate Web Development with PHP/MySQL')
    # import_schedule('bacs200')
    # import_schedule('bacs350')


def list_course_content():
    data = [banner('Course Content Data')]
    data += Course.list()
    for c in unc_courses():
        data.append(banner(c))
        data.append('\nPROJECTS:\n')
        data += Project.list(c)
        data.append('\nLESSONS:\n')
        data += Lesson.list(c)
        data.append('\nSTUDENTS:')
        data.append(list_students(c))
        data.append('\nASSIGNMENTS:')
        data.append(list_assignments(c))
    return text_join(data)


def list_students(course):
    return ("\nStudents %s:\n" % course) + text_join([str(s) for s in Course.students(course)])


def read_schedule(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    with open(data_file) as f:
        return [row[:-2] for row in reader(f)]


def update_topics():

    def set_lesson_topic(course, lesson_id, name, zybooks=None):
        x = Lesson.lookup(course, lesson_id)
        x.topic = name
        if zybooks:
            x.reading = zybooks_link(course[-3:], zybooks)
        x.save()

    course = 'bacs200'
    set_lesson_topic(course, '11', 'Forming URLs')
    set_lesson_topic(course, '12', 'Development Workflow')
    set_lesson_topic(course, '13', 'Test and Debug')
    set_lesson_topic(course, '14', 'Using Stylesheets')
    set_lesson_topic(course, '15', 'Text & Color')
    set_lesson_topic(course, '16', 'Spacing & Borders')
    set_lesson_topic(course, '17', 'Page Layout')
    set_lesson_topic(course, '18', 'Page Structure')
    set_lesson_topic(course, '19', 'Menus', '4.5 Font & Text Properties')
    set_lesson_topic(course, '20', 'Bootstrap', '4.6 Box Model')
    set_lesson_topic(course, '21', 'Tab View', '3.1 HTML Containers')
    set_lesson_topic(course, '22', 'Accordion', '3.2 Forms')
    set_lesson_topic(course, '23', 'Version Control', '3.3 Common Widgets')
    set_lesson_topic(course, '24', 'W3Schools', '3.4 HTML5 Widgets')
    set_lesson_topic(course, '25', 'W3Schools Tutorials', '3.5 Audio & Video')

    course = 'bacs350'
    set_lesson_topic(course, '11', 'Document Viewer')
    set_lesson_topic(course, '12', 'Document Manager')
    set_lesson_topic(course, '13', 'Directory Listing')
    set_lesson_topic(course, '14', 'Document Select')
    set_lesson_topic(course, '15', 'SQL Tables')
    set_lesson_topic(course, '16', 'Database Connect')
    set_lesson_topic(course, '17', 'List Rows ')
    set_lesson_topic(course, '18', 'CRUD Operations')
    set_lesson_topic(course, '19', 'Add Records')
    set_lesson_topic(course, '20', 'Update Records')
    set_lesson_topic(course, '21', 'Data Form Views', '14.1 Relational Databases')
    set_lesson_topic(course, '22', 'Edit View', '14.2 SQL')
    set_lesson_topic(course, '23', 'Forms App', '14.3 Tables')
    set_lesson_topic(course, '24', 'Logging', '14.4 Insert Records')
    set_lesson_topic(course, '25', 'MVC Pattern', '14.5 Selecting Records')
    set_lesson_topic(course, '26', 'Single Page App', '14.6 SQL Functions')


def schedule_data(course):
    title = Course.objects.get(name=course).title
    return [title, 'Class Schedule'], Lesson.query(course)


def slides_markdown(course, lesson):
    doc = 'Documents/unc/%s/lesson/%s' % (course, lesson)
    text = fix_images(read_markdown(doc), '/static/images/unc/%s' % course)
    bear = '\n\n---\n\n<img src="/static/images/unc/bacs200/Bear.200.png">\n\n---\n\n'
    return bear + text + bear


def student_data(course):
    return Course.students(course)


def student_projects(course):
    skills = [s.images.split(',')[0] for s in Skill.query(course)[5:]]
    projects = Project.query(course)[5:8]
    return [(s, projects, skills) for s in Course.students(course)]


def show_course_files(course):
    return banner(course) + text_join(recursive_list('Documents/unc/%s' % course))


def show_sample_files():
    def list_files(path):
        if exists(path):
            return banner(path) + text_join(recursive_list(path))
        else:
            return '%s path does not exist' % path

    paths = [
        join(environ['HOME'], 'UNC', 'old-code', 'public_html'),
        join(environ['HOME'], 'UNC', 'UNC-BACS200-2019-Fall', 'public_html'),
        join(environ['HOME'], 'UNC', 'UNC-BACS350-2019-Fall', 'public_html'),
    ]

    return text_join([list_files(path) for path in paths])


def unc_courses():
    return Course.all()

# def delete_students():
#     c = create_course('cs350', 'Software Engineering (under development)', 'Mark Seaman',
#                   'This class is for test purposes only')
#     print(c)
#     Student.objects.filter(course=c).delete()


def weekly_agenda(course, week):
    project = Project.lookup(course, week)
    lessons = Lesson.objects.filter(course__name=course, week=week).order_by('date')
    return dict(week=week, lessons=lessons, project=project)


def weekly_lessons(course):
    return [weekly_agenda(course, week + 1) for week in range(8)]


def zybooks_link(course, reading):
    match_pattern = r'^(\d+).(\d+) (.*)$'
    url = 'https://learn.zybooks.com/zybook/UNCOBACS%sSeamanFall2019' % course
    replace_pattern = r'<a href="%s/chapter/\1/section/\2">\1.\2 - \3</a>' % url
    link = compile(match_pattern).sub(replace_pattern, reading)
    return link
