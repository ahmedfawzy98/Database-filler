import os
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_files = os.path.join(base_dir, 'Database_files')
database_path = os.path.join(base_dir, '../SSPScheduler-WebApp/db.sqlite3')

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
# 0,1,2,3,4                               ,5             ,6        ,7,8,9,10,          ,16     ,17            ,18         ,23 ,24     ,25            ,26               ,31 ,32     ,33            ,34 ,       ,39 ,40     ,41            ,42 ,       ,47 ,48
# 1,3,3,1,Dr Mohsen Mandour- Dr said Agamy,Modern Physics,Class 103,1,0,0,1,,,,,Lecture,Unknown,Modern Physics,P41,1,4,6,6,Tut,Unknown,Modern Physics,Class C12,1,5,5,5,Tut,Unknown,Modern Physics,Lab,2,0,4,4,Lab,Unknown,Modern Physics,Lab,2,0,5,5,Lab,CCE

for file in os.listdir(database_files):
    file_path = os.path.join(database_files, file)
    f = open(file_path, 'r')
    for line in f.readlines():
        info = line.split(',')
        if info[5] not in courses:
            courses[info[5]] = course_id
            cursor.execute("insert into scheduler_course (id, name, priority, term, creditHours, department)"
                           "values ({},'{}',{},{},{},'{}')".format(course_id, info[5], 0, info[1], info[2],
                                                                   info[48].strip('\n')))
        if info[4] not in instructors:
            instructors[info[4]] = instructor_id
            cursor.execute("insert into scheduler_instructor (id, name, priority, course_id)"
                           "values ({},'{}',{},{})".format(instructor_id, info[4], 0, courses[info[5]]))

        cursor.execute("insert into scheduler_group (id, groupNum, inst_id, available)"
                       " values ({},{},{},{})".format(info[0], info[3], instructors[info[4]], True))

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


connection.commit()

connection.close()

