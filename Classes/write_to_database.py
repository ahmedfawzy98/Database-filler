import os
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_files = os.path.join(base_dir, 'Database_files')
database_path = os.path.join(base_dir, '../SSPScheduler-WebApp/db.sqlite3')

# 0,1,2,3,4                               ,5             ,6        ,7,8,9,10,          ,16     ,17            ,18         ,23 ,24     ,25            ,26               ,31 ,32     ,33            ,34 ,       ,39 ,40     ,41            ,42 ,       ,47 ,48
# 1,3,3,1,Dr Mohsen Mandour- Dr said Agamy,Modern Physics,Class 103,1,0,0,1,,,,,Lecture,Unknown,Modern Physics,P41,1,4,6,6,Tut,Unknown,Modern Physics,Class C12,1,5,5,5,Tut,Unknown,Modern Physics,Lab,2,0,4,4,Lab,Unknown,Modern Physics,Lab,2,0,5,5,Lab,CCE


def fill_database():
    course_id = 1
    instructor_id = 1
    lecture_id = 1
    exLecture_id = 1
    tut_id = 1
    lab_id = 1
    time_id = 1

    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute('delete from scheduler_course;')
    cursor.execute('delete from scheduler_instructor;')
    cursor.execute('delete from scheduler_time;')
    cursor.execute('delete from scheduler_lecture;')
    cursor.execute('delete from scheduler_tutorial;')
    cursor.execute('delete from scheduler_lab;')
    cursor.execute('delete from scheduler_group;')
    cursor.execute('delete from scheduler_exlecture;')

    courses = {}
    instructors = {}

    term_number = None

    for file in os.listdir(database_files):
        file_path = os.path.join(database_files, file)
        f = open(file_path, 'r')
        for line in f.readlines():
            info = line.split(',')

            if info[4].lower() == 'unknown':
                continue

            if term_number != info[1]:
                term_number = info[1]
                courses.clear()
                instructors.clear()

            if info[5] not in courses:
                courses[info[5]] = course_id
                cursor.execute("insert into scheduler_course (id, name, priority, term, creditHours, department)"
                               "values ({},'{}',{},{},{},'{}')".format(course_id, info[5], 0, info[1], info[2],
                                                                       info[48].strip('\n')))

            info[4] = fix_inst_name(info[4])
            inst_identifier = info[4] + ' ' + info[5]
            result = match_insts_names(inst_identifier, info[5], instructors)
            inst_identifier = result[0]
            if result[-1] == 'update':
                inst_id = instructors[result[1]]
                cursor.execute("update scheduler_instructor set name='{}' where id={}".format(info[4], inst_id))
                instructors[inst_identifier] = instructors.pop(result[1])

            if inst_identifier not in instructors:
                instructors[inst_identifier] = instructor_id
                cursor.execute("insert into scheduler_instructor (id, name, priority, course_id)"
                               "values ({},'{}',{},{})".format(instructor_id, info[4], 0, courses[info[5]]))

            cursor.execute("insert into scheduler_group (id, groupNum, inst_id, available)"
                           " values ({},{},{}, True)".format(info[0], info[3], instructors[inst_identifier]))

            cursor.execute("insert into scheduler_lecture (id, place, type, PeriodType, group_id)"
                           "values ({},'{}',{},'{}',{})".format(lecture_id, info[6], info[7], info[15], info[0]))
            cursor.execute("insert into scheduler_time (id, time_day, time_from, time_to, lecture_id)"
                           "values ({},{},{},{},{})".format(time_id, info[8], info[9], info[10], lecture_id))
            time_id += 1

            if info[12] != '':
                cursor.execute("insert into scheduler_exlecture (id, Place, lecture_id)"
                               "values ({},'{}',{})".format(exLecture_id, info[11], lecture_id))
                cursor.execute("insert into scheduler_time (id, time_day, time_from, time_to, exlecture_id)"
                               "values ({},{},{},{},{})".format(time_id, info[8], info[9], info[10], exLecture_id))
                time_id += 1
                exLecture_id += 1

            if info[16] != '':
                cursor.execute("insert into scheduler_tutorial (id, place, type, PeriodType, group_id)"
                               "values ({},'{}',{},'{}',{})".format(tut_id, info[18], info[19], info[23], info[0]))
                cursor.execute("insert into scheduler_time (id, time_day, time_from, time_to, tut_id)"
                               "values ({},{},{},{},{})".format(time_id, info[20], info[21], info[22], tut_id))
                tut_id += 1
                time_id += 1

            if info[24] != '':
                cursor.execute("insert into scheduler_tutorial (id, place, type, PeriodType, group_id)"
                               "values ({},'{}',{},'{}',{})".format(tut_id, info[26], info[27], info[31], info[0]))
                cursor.execute("insert into scheduler_time (id, time_day, time_from, time_to, tut_id)"
                               "values ({},{},{},{},{})".format(time_id, info[28], info[29], info[30], tut_id))
                tut_id += 1
                time_id += 1

            if info[32] != '':
                cursor.execute("insert into scheduler_lab (id, place, type, PeriodType, group_id)"
                               "values ({},'{}',{},'{}',{})".format(lab_id, info[34], info[35], info[39], info[0]))
                cursor.execute("insert into scheduler_time (id, time_day, time_from, time_to, lab_id)"
                               "values ({},{},{},{},{})".format(time_id, info[36], info[37], info[38], lab_id))
                lab_id += 1
                time_id += 1

            if info[40] != '':
                cursor.execute("insert into scheduler_lab (id, place, type, PeriodType, group_id)"
                               "values ({},'{}',{},'{}',{})".format(lab_id, info[42], info[43], info[47], info[0]))
                cursor.execute("insert into scheduler_time (id, time_day, time_from, time_to, lab_id)"
                               "values ({},{},{},{},{})".format(time_id, info[44], info[45], info[46], lab_id))
                lab_id += 1
                time_id += 1

            course_id += 1
            instructor_id += 1
            lecture_id += 1
        term_number = None

    connection.commit()

    connection.close()


def fix_inst_name(inst_name):
    inst_name = inst_name.replace('ich', 'esh')
    inst_name = inst_name.replace('ch', 'sh')
    if inst_name[-1].isdigit() and inst_name[-2].lower() == 'g':
        inst_name = inst_name[:-2]
        inst_name = inst_name.strip().rstrip('-')
    inst_name = inst_name.replace('-', '/')
    inst_name = inst_name.strip()
    return inst_name


def match_insts_names(inst_identifier, course_name, instructors):
    insts_identifiers = list(instructors.keys())
    insts_identifiers.sort()
    counter = 0
    name1_words = inst_identifier.split(' ')
    for identifier in insts_identifiers:
        if course_name in identifier:
            name2_words = identifier.split(' ')
            for word in name1_words:
                for word2 in name2_words:
                    if word == word2:
                        counter += 1
            if counter >= len(course_name.split(' ')) + 2:
                if len(identifier) > len(inst_identifier):
                    return [identifier, 'yes']
                else:
                    return [inst_identifier, identifier, 'update']
            counter = 0
    return [inst_identifier, 'no']


if __name__ == '__main__':
    fill_database()
