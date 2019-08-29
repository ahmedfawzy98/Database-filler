import os
import re

import xlrd

from Classes.Lab import Lab
from Classes.Lecture import Lecture
from Classes.SchGroup import SchGroup
from Classes.Tutorial import Tutorial
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tables_path = os.path.join(base_dir, 'tables_excel')
database_files = os.path.join(base_dir, 'Database_files')
file_path = ''
sheet = None
groups = []
unknown = {}
course_name = ''
group_number = ''
term_number = ''
day = ''
fr = ''
to = ''


def set_group_number(cell_text):
    global group_number
    if '1' in cell_text:
        group_number = 1
    elif '2' in cell_text:
        group_number = 2
    elif '3' in cell_text:
        group_number = 3
    elif '4' in cell_text:
        group_number = 4
    elif '5' in cell_text:
        group_number = 5
    elif '6' in cell_text:
        group_number = 6
    return


def set_term_number(cell_text):
    global term_number
    if cell_text.startswith('10'):
        term_number = 10
    elif cell_text.startswith('1'):
        term_number = 1
    elif cell_text.startswith('2'):
        term_number = 2
    elif cell_text.startswith('3'):
        term_number = 3
    elif cell_text.startswith('4'):
        term_number = 4
    elif cell_text.startswith('5'):
        term_number = 5
    elif cell_text.startswith('6'):
        term_number = 6
    elif cell_text.startswith('7'):
        term_number = 7
    elif cell_text.startswith('8'):
        term_number = 8
    elif cell_text.startswith('9'):
        term_number = 9
    elif cell_text.startswith('Hu'):
        term_number = 11
    else:
        return -1


def set_day(cell_text):
    global day
    if cell_text.startswith("Sa"):
        day = 0
    elif cell_text.startswith("Su"):
        day = 1
    elif cell_text.startswith("Mo"):
        day = 2
    elif cell_text.startswith("Tu"):
        day = 3
    elif cell_text.startswith("Wed"):
        day = 4
    elif cell_text.startswith("Th"):
        day = 5
    return


def set_from_to(cell_text):
    global fr, to
    if cell_text.startswith("1-") or cell_text.startswith("1 -"):
        fr = 0
        to = 1
        return True
    elif cell_text.startswith("3-") or cell_text.startswith("3 -"):
        fr = 2
        to = 3
        return True
    elif cell_text.startswith("5-")or cell_text.startswith("5 -"):
        fr = 4
        to = 5
        return True
    elif cell_text.startswith("7-")or cell_text.startswith("7 -"):
        fr = 6
        to = 7
        return True
    elif cell_text.startswith("9-")or cell_text.startswith("9 -"):
        fr = 8
        to = 9
        return True
    elif cell_text.startswith("11-")or cell_text.startswith("11 -"):
        fr = 10
        to = 11
        return True
    return False


def set_group(group_courses):
    global course_name
    if course_name not in group_courses:
        group_courses[course_name] = SchGroup(True)
        group_courses[course_name].number = group_number
        group_courses[course_name].courseTerm = term_number
    group = group_courses[course_name]
    group.lecture.courseName = course_name
    for i in range(len(group.tutorials)):
        group.tutorials[i].courseName = course_name
    for i in range(len(group.labs)):
        group.labs[i].courseName = course_name
    return group_courses[course_name]


def check_cell_case(left_up, left_down, right_up, right_down, row=None):
    if left_up != '' and left_down == '' and right_up == '' and right_down == '' and row != sheet.nrows:
        return 1
    elif left_up != '' and left_down != '' and right_up == '' and right_down == '':
        return 2
    elif left_up != '' and left_down != '' and right_up != '' and right_down != '':
        return 3
    elif left_up == '' and left_down == '' and right_up != '' and right_down != '':
        return 4
    elif left_up == '' and left_down == '' and right_up == '' and right_down != '':
        return 5
    elif left_up == '' and left_down != '' and right_up == '' and right_down == '':
        return 6
    else:
        return -1


def create_lab(group, lab_type, right=False):
    global course_name, group_number, day, fr, to
    # lab = Lab()
    # lab.courseName = course_name
    # lab.groupNum = group_number
    # lab.instName = 'Unknown'
    # lab.periodType = 'Lab'
    # lab.place = 'Lab'
    # lab.type = lab_type
    # lab.time.day = day
    # lab.time.fr = fr
    # lab.time.to = fr
    # if right:
    #     lab.time.fr = to
    #     lab.time.to = to
    # group.add_lab(lab)
    # if lab_type == 2:
    #     lab = Lab()
    #     lab.courseName = course_name
    #     lab.groupNum = group_number
    #     lab.instName = 'Unknown'
    #     lab.periodType = 'Lab'
    #     lab.place = 'Lab'
    #     lab.type = lab_type
    #     lab.time.day = day
    #     lab.time.fr = to
    #     lab.time.to = to
    #     group.add_lab(lab)
    for i in range(lab_type):
        lab = Lab()
        lab.courseName = course_name
        lab.groupNum = group_number
        lab.instName = 'Unknown'
        lab.periodType = 'Lab'
        lab.place = 'Lab'
        lab.type = lab_type
        lab.time.day = day
        lab.time.fr = fr
        lab.time.to = fr
        if right or i == 1:
            lab.time.fr = to
            lab.time.to = to
        group.add_lab(lab)


def create_tutorial(group, place, tut_type, right=False):
    global course_name, group_number, day, fr, to
    # tut = Tutorial()
    # tut.courseName = course_name
    # tut.groupNum = group_number
    # tut.instName = 'Unknown'
    # tut.periodType = 'Tut'
    # tut.place = place
    # tut.type = tut_type
    # tut.time.day = day
    # tut.time.fr = fr
    # tut.time.to = fr
    # if right:
    #     tut.time.fr = to
    #     tut.time.to = to
    # group.add_tut(tut)
    # if tut_type == 2:
    #     tut = Tutorial()
    #     tut.courseName = course_name
    #     tut.groupNum = group_number
    #     tut.instName = 'Unknown'
    #     tut.periodType = 'Tut'
    #     tut.place = place
    #     tut.type = tut_type
    #     tut.time.day = day
    #     tut.time.fr = to
    #     tut.time.to = to
    #     group.add_tut(tut)
    for i in range(tut_type):
        tut = Tutorial()
        tut.courseName = course_name
        tut.groupNum = group_number
        tut.instName = 'Unknown'
        tut.periodType = 'Tut'
        tut.place = place
        tut.type = tut_type
        tut.time.day = day
        tut.time.fr = fr
        tut.time.to = fr
        if right or i == 1:
            tut.time.fr = to
            tut.time.to = to
        group.add_tut(tut)


def check_lecture_case(row, col, saved_names, cell_case=1, single_row=False):
    global course_name
    # previous = sheet.cell_value(row - 2, col)
    # if cell_case == 2 and not single_row:
    #     next_cell = sheet.cell_value(row + 1, col)
    # elif cell_case == 2 and single_row:
    #     next_cell = sheet.cell_value(row, col)
    # elif cell_case != 2 and single_row:
    #     next_cell = sheet.cell_value(row, col)
    # else:
    #     next_cell = sheet.cell_value(row + 2, col)
    # if 'lec' in str(previous).lower():
    #     crs_name = set_course_name(previous.split('-')[0], saved_names)
    #     if crs_name.startswith(course_name):
    #         return 1  # completion of lecture
    # if 'lec' in str(next_cell).lower():
    #     crs_name = set_course_name(next_cell.split('-')[0], saved_names)
    #     if crs_name.startswith(course_name):
    #         return 2  # start of lecture
    # return 3  # extension of lecture
    # return -1
    previous = sheet.cell_value(row - 2, col)
    next_cell = sheet.cell_value(row + 2, col)
    if 'lec' in str(previous).lower():
        crs_name = set_course_name(previous.split('-')[0], saved_names)
        if crs_name.startswith(course_name):
            return 1
    if cell_case == 2 or single_row:
        next_cell = sheet.cell_value(row + 1, col)
    if 'lec' in str(next_cell).lower():
        crs_name = set_course_name(next_cell.split('-')[0], saved_names)
        if crs_name.startswith(course_name):
            return 2
    if cell_case == 1 and single_row:
        return 4
    return 3


def check_place(cell_text):
    cell_text_content = cell_text.split('-')
    if 'place' in cell_text_content[-1].lower():
        if ':' in cell_text_content[-1]:
            place = cell_text_content[-1].split(':')[-1]
        else:
            place = cell_text_content[-1][cell_text_content[-1].lower().find('place') + 5:]
    else:
        cell_text_content = cell_text.split(':')
        if cell_text_content[0] != cell_text:
            place = cell_text_content[-1]
        elif 'tut' in cell_text.lower() and 'place' not in cell_text.lower():
            place = cell_text[cell_text.lower().find('tut') + 3:]
        else:
            if 'place' not in cell_text.lower():
                place = 'Unknown'
            else:
                place = cell_text[cell_text.lower().find('place') + 5:]
    if place.isdigit():
        place = 'Class ' + place
    place = place.replace('-', '')
    place = re.sub(' +', ' ', place)
    if place == '':
        return 'Unknown'
    return place.strip()


def fix_tutorials(tutorials):
    odd = None
    for tut in tutorials:
        if tut.type == 1:
            if tut.time.fr % 2 != 0:
                odd = True
            else:
                odd = False
            break
    for tut in tutorials:
        if tut.type == 2:
            if odd and tut.time.fr % 2 != 0:
                tutorials.remove(tut)
                break
            elif not odd and tut.time.fr % 2 == 0:
                tutorials.remove(tut)
                break


def add_lecture_extension(group, place):
    group.lecExPlace = place
    group.lecExDay = day
    group.lecExFrom = fr
    group.lecExTo = to


def add_lecture(group, row, col, case=False, place=None):
    global course_name, group_number, day, fr, to
    main_lecture = sheet.cell_value(row, col)
    lecture = group.lecture
    lecture.instName = main_lecture[main_lecture.find('Dr'):]
    if len(lecture.instName) == 1:
        lecture.instName = 'Unknown'
    else:
        lecture.instName = lecture.instName.replace('.', ' ')
        lecture.instName = lecture.instName.replace('Dr', 'Dr ')
        lecture.instName = lecture.instName.replace('Prof', '')
        lecture.instName = lecture.instName.replace('prof', '')
        lecture.instName = lecture.instName.replace('\n', ' ')
        lecture.instName = lecture.instName.replace(')', ' ')
        lecture.instName = lecture.instName.replace('(', ' ')
        lecture.instName = re.sub(' +', ' ', lecture.instName)
        lecture.instName = lecture.instName.strip()
    if place is not None:
        lecture.place = place
    else:
        lecture.place = check_place(sheet.cell_value(row + 1, col))
    lecture.courseName = course_name
    lecture.groupNum = group_number
    lecture.type = 1
    lecture.periodType = 'Lecture'
    lecture.time.day = day
    if case:
        lecture.time.fr = fr
        lecture.time.to = to
    else:
        lecture.time.fr = to
        set_from_to(sheet.cell_value(row, 1))
        lecture.time.to = to


def write_file():
    global file_path
    empty = ",,,,,,,"
    f = open(file_path, 'w')
    for group in groups:
        f.write('{},{},{},'.format(group.courseTerm, group.creditHours, group.number))
        f.write('{},{},{},{},{},{},{},{},{},{},{},{},'.format(group.lecture.instName, group.lecture.courseName,
                                                              group.lecture.place, group.lecture.type,
                                                              group.lecture.time.day, group.lecture.time.fr,
                                                              group.lecture.time.to, group.lecExPlace, group.lecExDay,
                                                              group.lecExFrom, group.lecExTo,
                                                              group.lecture.periodType))
        if len(group.tutorials) == 0:
            f.write(empty + ",")
            f.write(empty + ",")
        elif len(group.tutorials) == 1:
            f.write(
                '{},{},{},{},{},{},{},{},'.format(group.tutorials[0].instName, group.tutorials[0].courseName,
                                                  group.tutorials[0].place, group.tutorials[0].type,
                                                  group.tutorials[0].time.day, group.tutorials[0].time.fr,
                                                  group.tutorials[0].time.to, group.tutorials[0].periodType))
            f.write(empty + ",")
        else:
            for j in range(2):
                f.write('{},{},{},{},{},{},{},{},'.format(group.tutorials[j].instName,
                                                          group.tutorials[j].courseName,
                                                          group.tutorials[j].place, group.tutorials[0].type,
                                                          group.tutorials[j].time.day,
                                                          group.tutorials[j].time.fr,
                                                          group.tutorials[j].time.to,
                                                          group.tutorials[j].periodType))
        if len(group.labs) == 0:
            f.write(empty + ",")
            f.write(empty + "\n")
        elif len(group.labs) == 1:
            f.write(
                '{},{},{},{},{},{},{},{},'.format(group.labs[0].instName, group.labs[0].courseName,
                                                  group.labs[0].place, group.labs[0].type,
                                                  group.labs[0].time.day, group.labs[0].time.fr,
                                                  group.labs[0].time.to, group.labs[0].periodType))
            f.write(empty + "\n")
        else:
            for j in range(2):
                if j == 0:
                    end = ","
                else:
                    end = "\n"
                f.write('{},{},{},{},{},{},{},{}{}'.format(group.labs[j].instName,
                                                           group.labs[j].courseName,
                                                           group.labs[j].place, group.labs[0].type,
                                                           group.labs[j].time.day,
                                                           group.labs[j].time.fr,
                                                           group.labs[j].time.to,
                                                           group.labs[j].periodType, end))
    f.close()


def extract_table():
    global group_number, term_number, course_name, day, fr, to, sheet
    col = 2
    start_row = 0
    group_courses = {}  # courses in the same group (vertically) in the table
    while not sheet.cell_value(start_row, col).startswith('G'):
        start_row += 1
        if start_row == 5:
            col += 1
            start_row = 0
    while col < sheet.ncols:
        row = start_row + 2
        set_group_number(sheet.cell_value(start_row, col))
        set_term_number(sheet.cell_value(1, col))
        while row < sheet.nrows:
            single_row = False
            last_row = True
            left_up = sheet.cell_value(row, col)
            right_up = sheet.cell_value(row, col + 1)
            left_down = None
            right_down = None
            if row != sheet.nrows - 1:
                last_row = False
                left_down = sheet.cell_value(row + 1, col)
                right_down = sheet.cell_value(row + 1, col + 1)
            left_up = str(left_up);left_down = str(left_down); right_up = str(right_up); right_up = str(right_up)
            set_day(sheet.cell_value(row, 0))
            case = check_cell_case(left_up, left_down, right_up, right_down)
            if case == -1:
                row += 1
                continue
            set_from_to(sheet.cell_value(row, 1))
            if str(sheet.cell_value(row + 1, 1)) != '':
                single_row = True
            if case == 4:
                course_name = right_up.split('-')[0]
            elif case == 5:
                course_name = right_down.split('-')[0]
            elif case == 6:
                course_name = left_down.split('-')[0]
            else:
                course_name = left_up.split('-')[0]
                # if course_name == left_up:
                #     course_name = left_up[:left_up.lower().find('lec')]
            course_name = set_course_name(course_name, group_courses)
            group = set_group(group_courses)
            if case == 1:
                if 'lab' in left_up.lower():
                    create_lab(group, 2)
                elif 'tut' in left_up.lower():
                    place = check_place(left_up)
                    create_tutorial(group, place, 2)
                elif 'lec' in left_up.lower():
                    lecture_case = check_lecture_case(row, col, group_courses, 1, single_row)
                    # if not single_row:
                    if lecture_case == 1:
                        group.lecture.time.to = fr
                    elif lecture_case == 2:
                        # if single_row:
                        #     row += 1
                        # else:
                        row += 2
                        add_lecture(group, row, col)
                    elif lecture_case == 3:
                        place = check_place(left_up)
                        # course_name = set_course_name(left_up.split('-')[0], group_courses)
                        # group = set_group(group_courses)
                        add_lecture_extension(group, place)
                    elif lecture_case == 4:
                        place = check_place(left_up)
                        add_lecture(group, row, col, True, place)
                    # else:
                    #     if lecture_case == 1:
                    #         group.lecture.time.to = fr
                    #     elif lecture_case == 2:
                    #         # if single_row:
                    #         #     row += 1
                    #         # else:
                    #         row += 2
                    #         add_lecture(group, row, col)
                    #     elif lecture_case == 3:
                    #         place = check_place(left_up)
                    #         # course_name = set_course_name(left_up.split('-')[0], group_courses)
                    #         # group = set_group(group_courses)
                    #         add_lecture_extension(group, place)
            elif case == 2:
                if 'lec' not in left_up.lower() and 'lec' not in left_down.lower():
                    if 'tut' in left_up.lower():
                        if 'place' in left_down.lower() and 'tut' not in left_down.lower() \
                                and 'lab' not in left_down.lower():
                            place = check_place(left_down)
                            create_tutorial(group, place, 1)
                            row += 2
                            continue
                        else:
                            place = check_place(left_up)
                            create_tutorial(group, place, 2)
                    elif 'lab' in left_up.lower():
                        if 'place' in left_down.lower() and 'tut' not in left_down.lower() \
                                and 'lab' not in left_down.lower():
                            create_lab(group, 1)
                            row += 2
                            continue
                        else:
                            create_lab(group, 2)
                    course_name = left_down.split('-')[0]
                    course_name = set_course_name(course_name, group_courses)
                    group = set_group(group_courses)
                    if 'tut' in left_down.lower():
                        place = check_place(left_down)
                        create_tutorial(group, place, 2)
                    elif 'lab' in left_down.lower():
                        create_lab(group, 2)
                elif 'lec' in left_up.lower() and 'lec' not in left_down.lower():
                    if left_down.startswith('Place'):
                        add_lecture(group, row, col, True)
                    elif check_lecture_case(row, col, group_courses, 1, single_row) == 1:
                        group.lecture.time.to = fr
                    elif check_lecture_case(row, col, group_courses, 1, single_row) == 3:
                        place = check_place(left_up)
                        # course_name = set_course_name(left_up.split('-')[0], group_courses)
                        # group = set_group(group_courses)
                        add_lecture_extension(group, place)
                    if 'tut' in left_down.lower():
                        place = check_place(left_down)
                        create_tutorial(group, place, 2)
                        if len(group.tutorials) > 2:
                            fix_tutorials(group.tutorials)
                    elif 'lab' in left_down.lower():
                        create_lab(group, 2)
                elif 'lec' not in left_up.lower() and 'lec' in left_down.lower():
                    if not single_row:
                        if 'tut' in left_up.lower():
                            place = check_place(left_up)
                            create_tutorial(group, place, 2)
                        elif 'lab' in left_up.lower():
                            create_lab(group, 2)
                        lecture_case = check_lecture_case(row + 1, col, group_courses, 2)
                        if lecture_case == 2:
                            # if single_row:
                            #     row += 1
                            # else:
                            row += 2
                            add_lecture(group, row, col)
                        elif lecture_case == 3:
                            place = check_place(left_down)
                            # course_name = set_course_name(left_down.split('-')[0], group_courses)
                            # group = set_group(group_courses)
                            add_lecture_extension(group, place)
                    else:
                        if 'tut' in left_up.lower():
                            place = check_place(left_up)
                            create_tutorial(group, place, 2)
                        elif 'lab' in left_up.lower():
                            create_lab(group, 2)
                elif 'lec' in left_up.lower() and 'lec' in left_down.lower():
                    if not single_row:
                        lecture_case = check_lecture_case(row, col, group_courses)
                        if lecture_case == 1:
                            group.lecture.time.to = fr
                        elif lecture_case == 3:
                            place = check_place(left_up)
                            # course_name = set_course_name(left_up.split('-')[0], group_courses)
                            # group = set_group(group_courses)
                            add_lecture_extension(group, place)
                        course_name = set_course_name(left_down.split('-')[0], group_courses)
                        group = set_group(group_courses)
                        lecture_case = check_lecture_case(row + 1, col, group_courses, 2)
                        if lecture_case == 2:
                            # if single_row:
                            #     row += 1
                            # else:
                            row += 2
                            add_lecture(group, row, col)
                        elif lecture_case == 3:
                            place = check_place(left_down)
                            add_lecture_extension(group, place)
                    else:
                        lecture_case = check_lecture_case(row, col, group_courses, 1, single_row)
                        if lecture_case == 1:
                            group.lecture.time.to = fr
                        elif lecture_case == 2:
                            row += 1
                            add_lecture(group, row, col)
                        elif lecture_case == 3:
                            place = check_place(left_up)
                            # course_name = set_course_name(left_up.split('-')[0], group_courses)
                            # group = set_group(group_courses)
                            add_lecture_extension(group, place)
                        # course_name = set_course_name(left_down.split('-')[0], group_courses)
                        # group = set_group(group_courses)
                        # lecture_case = check_lecture_case(row + 1, col, group_courses, 2, single_row)
                        # if lecture_case == 2:
                        #     if single_row:
                        #         row += 1
                        #     else:
                        #         row += 2
                        #     add_lecture(group, row, col)
                        # elif lecture_case == 3:
                        #     place = check_place(left_down)
                        #     add_lecture_extension(group, place)
            elif case == 3:
                if 'tut' in left_up.lower():
                    place = check_place(left_down)
                    create_tutorial(group, place, 1)
                elif 'lab' in left_up.lower():
                    create_lab(group, 1)
                course_name = right_up.split('-')[0]
                course_name = set_course_name(course_name, group_courses)
                group = set_group(group_courses)
                if 'tut' in right_up.lower():
                    place = check_place(right_down)
                    create_tutorial(group, place, 1, True)
                elif 'lab' in right_up.lower():
                    create_lab(group, 1, True)
            elif case == 4:
                if 'tut' in right_up.lower():
                    place = check_place(right_down)
                    create_tutorial(group, place, 1, True)
                elif 'lab' in right_up.lower():
                    create_lab(group, 1, True)
            elif case == 5:
                if 'tut' in right_down.lower():
                    place = check_place(right_down)
                    create_tutorial(group, place, 1, True)
                elif 'lab' in right_down.lower():
                    create_lab(group, 1, True)
            elif case == 6:
                if sheet.cell_value(row + 1, 1) == '':
                    if 'tut' in left_down.lower():
                        place = check_place(left_down)
                        create_tutorial(group, place, 1, True)
                    elif 'lab' in left_down.lower():
                        create_lab(group, 1, True)
                    else:
                        if group.lecture.groupNum != '':
                            place = check_place(left_down)
                            add_lecture_extension(group, place)

            if not last_row and sheet.cell_value(row + 1, 1) != '':
                row += 1
            else:
                row += 1
                if row != sheet.nrows:
                    set_day(sheet.cell_value(row, 0))
                row += 1
        col += 1
        if set_term_number(sheet.cell_value(1, col)) == -1:
            col += 1
        for group in group_courses.values():
            groups.append(group)
        group_courses.clear()
        write_file()
    groups.clear()


def check_two_ways(name1, name2):
    if name1 in name2 or name2 in name1:
        return True
    return False


def modify_course_name(name):
    if 'IV' in name:
        name = name.replace('IV', ' 4')
    elif 'III' in name:
        name = name.replace('III', '3')
    elif 'II' in name:
        name = name.replace('II', '2')
    elif 'I' in name:
        name = name.replace('I', '1')
    if name.endswith('lV'):
        name = name.strip('lV')
        name = name + '4'
    elif name.endswith('lll'):
        name = name.strip('lll')
        name = name + '3'
    elif name.endswith('ll'):
        name = name.strip('ll')
        name = name + '2'
    elif name.endswith('l'):
        name = name.strip('l')
        name = name + '1'
    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.strip('I')
    name = name.strip('Lec')
    name = name.strip('lec')
    name = name.strip('Tut')
    name = name.strip('tut')
    name = name.strip('Lab')
    name = name.strip('lab')
    name = name.strip()
    name = re.sub(' +', ' ', name)
    if name[-2] != ' ' and name[-1].isdigit():
        name = name[:-1] + ' ' + name[-1]
    return name


def choose_name(name1, name2):
    if len(name1) > len(name2):
        return name1
    elif len(name1) < len(name2):
        return name2
    else:
        if re.search(r'\d', name1) is not None and re.search(r'\d', name2) is None:
            return name1
        elif re.search(r'\d', name1) is None and re.search(r'\d', name2) is not None:
            return name2
        else:
            return name1


def remove_digits(name):
    return re.sub(r' \d', '', name)


def check_common_words(name1, name2=None):
    name1_words = name1.split(' ')
    if name2 is not None:
        name2_words = name2.split(' ')
    else:
        name2_words = unknown.keys()
    counter = 0
    for word in name1_words:
        for word2 in name2_words:
            if word.lower() in word2.lower():
                counter += 1
                break
    if counter == 1:
        return 1
    else:
        return counter >= 2


# def fix_conflict(group_1, group_2):
#     group_1.tutorials = group_2.tutorials
#     group_1.labs = group_2.labs


# def check_after_whole_group(saved_groups):
#     for i in range(len(saved_groups)):
#         group_1 = saved_groups[i]
#         for j in range(i, len(saved_groups)):
#             group_2 = saved_groups[j]
#             if check_common_words(group_1.lecture.courseName, group_2.lecture.courseName) == 1:
#                 if group_1.lecture.time.day is not None and group_1.lecture.time.fr is not None and \
#                    group_1.lecture.time.to is not None:
#                     if group_2.lecture.time.day is None and group_2.lecture.time.fr is None and \
#                             group_2.lecture.time.to is None:
#                         fix_conflict(group_1, group_2)


def set_course_name(input_name, saved_names):
    if len(saved_names) != 0:
        input_name = modify_course_name(input_name)
        for name in saved_names:
            # case 1: remove all white spaces only
            if check_common_words(input_name, name):
                chosen = choose_name(input_name, name)
                saved_names[chosen] = saved_names.pop(name)
                return chosen
            elif name in input_name:
                chosen = choose_name(input_name, name)
                saved_names[chosen] = saved_names.pop(name)
                return chosen
            name_copy = remove_digits(name)
            # remove digits from saved  name
            if check_common_words(input_name, name_copy):
                chosen = choose_name(input_name, name)
                saved_names[chosen] = saved_names.pop(name)
                return chosen
            elif name_copy in input_name and name_copy != remove_digits(input_name):
                chosen = choose_name(input_name, name)
                saved_names[chosen] = saved_names.pop(name)
                return chosen
        # remove digits from input name
        name = check_if_unknown(input_name)
        if name is not None:
            chosen = choose_name(input_name, name)
            saved_names[chosen] = saved_names.pop(name)
            return chosen
        for name in saved_names:
            input_copy = remove_digits(input_name)
            if input_copy.lower() in name.lower():
                if check_common_words(input_name, name):
                    chosen = choose_name(input_name, name)
                    saved_names[chosen] = saved_names.pop(name)
                    return chosen
                else:
                    n = check_if_unknown(input_name)
                    if n is not None:
                        chosen = choose_name(input_name, n)
                        saved_names[chosen] = saved_names.pop(n)
                        return chosen
                    else:
                        unknown[input_name] = input_copy
                        continue

                # elif check_mapped_names(input_name, name, mapped_names):
            elif name in input_copy:
                chosen = choose_name(input_name, name)
                saved_names[chosen] = saved_names.pop(name)
                return chosen
        return modify_course_name(input_name)
    else:
        return modify_course_name(input_name)


def check_if_unknown(input_name):
    name_words = input_name.split(' ')
    for word in name_words:
        for name in unknown.keys():
            counter = 0
            for word2 in name.split(' '):
                if word in word2:
                    counter += 1
                    break
            if counter >= 2:
                unknown.pop(name)
                return name
    return None


def parse_all_tables():
    global file_path, sheet
    for file in os.listdir(tables_path):
        if file.endswith('.xlsx'):
            wb = xlrd.open_workbook(os.path.join(tables_path, file))
            sheet = wb.sheet_by_index(0)
            file = file.replace('.xlsx', '.csv')
            file_path = os.path.join(database_files, file)
            extract_table()


if __name__ == '__main__':
    parse_all_tables()
    print("Information saved in the file successfully")
    print("Parsing Done")
