from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.review import *
from unc.skills import *
from insight.models import *


def quick_test():
    # init_unc_data()
    print(print_projects())
    export_projects('bacs350')
    export_projects('bacs200')


def assign_reviews():
    show_groups('bacs200')
    show_groups('bacs350')
    assign_reviews_round4()
    # grade_reviews('bacs200/index.html')
    # grade_reviews('bacs350/index.php')


def setup_insights():
    Insight.import_data('insights.csv')
    Insight.export_data('insights2.csv')

    Insight.print_insights()


def fix_reviews():
    for r in Review.objects.filter(page='bacs350/superhero.php'):
        print(r.reviewer.name, r.page)
        r.page = 'bacs350/superhero/index.php'
        r.save()


def fix_lessons():
    def change_date(course, lesson, date, week):
        x = Lesson.lookup(course, lesson)
        x.date = date
        x.week = week
        x.save()

    date = '2019-12-02'
    change_date('bacs350', 38, date, 14)
    change_date('bacs200', 36, date, 14)


def init_unc_data():
    # x = import_schedule('bacs200')
    # x = import_schedule('bacs350')
    update_lessons()
    update_projects()
    update_skills()
    # fix_lessons()
    x = list_course_content()
    print(x)


def show_course_content():
    x = list_course_content()
    print(x)


