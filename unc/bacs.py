from csv import reader
from re import compile

from tool.document import fix_images, read_markdown

from unc.models import Course, Project, Lesson
from tool.shell import banner, text_join
from django.utils.timezone import make_aware
from datetime import datetime
from tool.days import parse_date, date_str


def add_project(course, row):
    date = make_aware(parse_date(row[2]))
    # date = make_aware(datetime.strptime(row[2], "%d-%b"))
    date = date_str(date)
    page = '%s/project_%s.html' % (course, row[0])
    instructions = '/unc/%s/project/%s' % (course, row[0])
    title = 'Project %s' % row[0]
    # print(date, page, instructions)
    return create_project(course, row[0], title, page, date, instructions)


def add_lesson(course, row):
    # CSV Data -- Week, Day, Date, Lesson, Topic, Reading, Projects, Process, Parts
    # print(row)
    project = add_project(course, row)
    date = make_aware(parse_date(row[2]))
    # date = make_aware(datetime.strptime(row[2], "%d-%b"))
    num = row[3] if row[3] != '' else '-1'
    # print('%s - lesson %s - %s' % (date.strftime('%b %d'), num, row[4]))
    # print('date: %s' % date)
    lesson = Lesson.objects.get_or_create(course=project.course, lesson=num, date=date)[0]
    lesson.week = row[0]
    lesson.project = project
    lesson.topic = row[4]
    lesson.reading = zybooks_link(course[-3:], row[5])
    lesson.save()
    return lesson


def build_projects(course):

    def create_project_record(course, project_num, page, features):
        p = Project.lookup(course, project_num)
        p.page = page
        p.save()
        for f in features:
            p.add_requirement(f)

    create_project_record(course, '01', 'bacs200/index.html', ['head', 'body', 'h1', 'p'])
    create_project_record(course, '02', 'bacs200/profile.html', ['head', 'title', 'body', 'h1', 'p'])
    create_project_record(course, '03', 'bacs200/projects/index.html', ['head', 'body', 'h1', 'p'])
    print_projects('bacs200')
    # print(Requirement.list())


def create_course(name, title, teacher, description):
    return Course.objects.get_or_create(name=name, title=title, teacher=teacher, description=description)[0]


def create_project(course, num, title, page, due, instructions):
    course = Course.objects.get(name=course)
    due = make_aware(datetime.strptime(due, "%Y-%m-%d"))
    project = Project.objects.get_or_create(course=course, num=num)[0]
    project.title = title
    project.page = page
    project.due = due
    project.instructions = instructions
    project.save()
    return project


def import_schedule(course):
    table = read_schedule(course)
    for row in table[2:]:
        add_lesson(course, row)


def init_data_test():
    initialize_data()
    print(print_data())


def initialize_data():
    create_course('bacs200', 'Web Development Intro (Fall 2019)', 'Mark Seaman',
                  'Web Design and Development for Small Business')
    create_course('bacs350', 'Web Development Intermediate (Fall 2019)', 'Mark Seaman',
                  'Intermediate Web Development with PHP/MySQL')
    import_schedule('bacs200')
    import_schedule('bacs350')


def print_projects(course):
    results = []
    for p in Project.objects.filter(course__name=course).order_by('due'):
        results.append('Project %s' % p)
        results.append('    '+'\n    '.join([r.label for r in p.requirements]))
    return results


def print_data():
    courses = [banner('Courses')] + Course.list()
    bacs200 = [banner('BACS 200'), 'PROJECTS:'] + print_projects('bacs200') + ['', 'LESSONS:'] + Lesson.list('bacs200')
    bacs350 = [banner('BACS 350'), 'PROJECTS:'] + Project.list('bacs350') + ['', 'LESSONS:'] + Lesson.list('bacs350')
    return text_join(courses + bacs200 + bacs350)


def read_schedule(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    with open(data_file) as f:
        return [row[:-2] for row in reader(f)]


def schedule_data(course):
    title = Course.objects.get(name=course).title
    return [title, 'Class Schedule'], Lesson.query(course)


def slides_markdown(course, lesson):
    doc = 'Documents/unc/%s/lesson/%s' % (course, lesson)
    text = fix_images(read_markdown(doc), '/static/images/unc/%s' % course)
    bear = '\n\n---\n\n<img src="/static/images/unc/bacs200/Bear.200.png">\n\n---\n\n'
    return bear + text + bear


def weekly_lessons(course):
    weeks = []
    for w in range(15):
        week = w + 1
        weeks.append(Lesson.objects.filter(course__name=course, week=week).order_by('date'))
    return weeks


def zybooks_link(course, reading):
    # print(reading)
    match_pattern = r'^(\d+).(\d+) (.*)$'
    url = 'https://learn.zybooks.com/zybook/UNCOBACS%sSeamanFall2019' % course
    replace_pattern = r'<a href="%s/chapter/\1/section/\2">\1.\2 - \3</a>' % url
    link = compile(match_pattern).sub(replace_pattern, reading)
    # print(link)
    return link


