import os

from Classes.Lab import Lab
from Classes.Lecture import Lecture
from Classes.SchGroup import SchGroup
import pyautogui
from Classes.Tutorial import Tutorial
import fileinput

"""THIS IS THE TERMINAL VERSION OF DATABASE FILLER """

# import msvcrt

groups = []
inp = ''
courseName = ''
courseTerm = ''
instructorName = ''
creditHours = 0
finish = False
change = False
linetoChange = 0


def createTut(tut, group):
    global courseName, inp
    tut.courseName = courseName
    tut.groupNum = group.number
    tut.instName = 'Unknown'
    tut.periodType = 'Tut'
    if checkInp(group, "Tutorial Place: "):
        return True
    tut.place = inp
    clear()
    mainMenu()
    if checkInp(group, "Tutorial type:(1 Or 2) ", 0, 3):
        return True
    tut.type = int(inp)
    clear()
    mainMenu()
    if checkInp(group, "Tutorial Day:(0--->5) ", -1, 6):
        return True
    tut.time.day = int(inp)
    clear()
    mainMenu()
    if checkInp(group, "Tutorial From:(0--->11) ", -1, 12):
        return True
    tut.time.fr = int(inp)
    clear()
    mainMenu()
    if checkInp(group, "Tutorial To:(0--->11) ", -1, 12):
        return True
    tut.time.to = int(inp)
    return False


def createLab(lab, group):
    global courseName, inp
    lab.courseName = courseName
    lab.groupNum = group.number
    lab.instName = 'Unknown'
    lab.periodType = 'Lab'
    if checkInp(group, "Lab Place: "):
        return True
    lab.place = inp
    clear()
    mainMenu()
    if checkInp(group, "Lab Type:(1 Or 2) ", 0, 3):
        return True
    lab.type = int(inp)
    clear()
    mainMenu()
    if checkInp(group, "Lab Day:(0--->5) ", -1, 6):
        return True
    lab.time.day = int(inp)
    clear()
    mainMenu()
    if checkInp(group, "Lab From:(0--->11) ", -1, 12):
        return True
    lab.time.fr = int(inp)
    clear()
    mainMenu()
    if checkInp(group, "Lab To:(0--->11) ", -1, 12):
        return True
    lab.time.to = int(inp)
    return False


def modifyGroup(group, savedGroup=None):
    global inp, change, linetoChange
    print("1.Group Number      2.Group Lecture      3.Group Tutorials      4.Group Labs      (b).Back")
    inp = input("Which property? ")
    if inp == '1':
        print("Group Number: {}".format(group.number), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Group Number:(1--->6) ")
        while isValidModifying(0, 7) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Group Number: {}".format(group.number), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Group Number:(1--->6) ")
        if inp == 'b':
            clear()
            return modifyGroup(group, savedGroup)
        if inp != 'n':
            group.number = int(inp)
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif inp == '2':
        clear()
        lectureMenu(group, savedGroup)
    elif inp == '3':
        clear()
        tutorialsMenu(group, savedGroup)
    elif inp == '4':
        clear()
        labsMenu(group, savedGroup)
    elif inp == 'b':
        clear()
        if savedGroup is not None:
            return viewGroups(savedGroup)
        return
    else:
        clear()
        print("Invalid input ---> (1, 2, 3, 4, b)")
        return modifyGroup(group)


def check(group, leftBound, rightBound):
    global inp, courseName, courseTerm, instructorName, creditHours
    if inp == "1a":
        print("Course Name: {}".format(courseName), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Course's Name: ")
        if inp == 'b':
            return True
        if inp != 'n':
            courseName = inp
            group.lecture.courseName = inp
        print("Credit Hours: {}".format(creditHours), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Credit Hours:(1--->4) ")
        while isValidModifying(0, 5) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Credit Hours: {}".format(creditHours), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Credit Hours:(1--->4) ")
        if inp == 'b' or inp == 'n':
            return True
        creditHours = int(inp)
        group.creditHours = int(inp)
        return True
    elif inp == "2a":
        print("Course Term: {}".format(courseTerm), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Course's Term: ")
        while isValidModifying(0, 11) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Course Term: {}".format(courseTerm), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Course's Term: ")
        if inp == 'b' or inp == 'n':
            return True
        courseTerm = int(inp)
        group.courseTerm = int(inp)
        return True
    elif inp == "3a":
        print("Instructor Name: {}".format(instructorName), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Instructor's Name: ")
        if inp == 'b' or inp == 'n':
            return True
        instructorName = inp
        group.lecture.instName = inp
        return True
    elif inp == "5m":
        if len(groups) == 0:
            return 3
        clear()
        viewGroups()
        return True
    elif inp == "4m":
        clear()
        modifyGroup(group)
        return True
    elif inp == "finish":
        return False
    else:
        return isValidFilling(leftBound, rightBound)


def viewGroups(j=0):
    global inp
    for i in range(len(groups)):
        print("{}.Course Name: {} , instructor Name: {} , group Number: {}".
              format(i + 1, groups[i].lecture.courseName, groups[i].lecture.instName, groups[i].number))
    if j != 0:
        print("Which Group? {}".format(j))
        lastGroupsMenu(j)
    else:
        inp = input("Which Group? ")
        while isValidModifying(0, len(groups) + 1, False) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            inp = input("Which Group? ")
        if inp == 'b':
            return
        i = int(inp)
        lastGroupsMenu(i)


def checkInp(group, inputString, leftBound=None, rightBound=None):
    global finish, inp
    inp = input(inputString)
    ch = check(group, leftBound, rightBound)
    while ch != 2:
        if not ch:
            finish = True
            break
        else:
            clear()
            if ch == 3:
                print("No saved groups yet")
            mainMenu()
            if ch == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif ch == 'i':
                print("Invalid input ---> Input must be number")
            elif ch == 'is':
                print("Invalid input ---> Enter yes Or no")
            inp = input(inputString)
            ch = check(group, leftBound, rightBound)
    if finish:
        return True
    return False


def mainMenu():
    global change
    print('(1a) Modify Course Name and Credit Hours', end='     ')
    print('(2a) Modify Course Term', end='     ')
    print('(3a) Modify Instructor Name', end='     ')
    print("(4m) Modify Group Info", end='     ')
    print("(5m) Modify last groups", end='     ')
    print('(finish) Finish')
    print("Information of group number {}:\n".format(len(groups) + 1))
    if change:
        change = False
        writeFile()


def lastGroupsMenu(i):
    global inp, change, linetoChange
    print("1. Modify Course Name      2. Modify Course Term      "
          "3. Modify Instructor Name      4. Modify Other Group Info      (b)Back")
    inp = input("Which one? ")
    if inp == '1':
        print("Course Name: {}".format(groups[i - 1].lecture.courseName), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Course's Name: ")
        if inp == 'b':
            clear()
            return viewGroups(i)
        if inp != 'n':
            groups[i - 1].lecture.courseName = inp
            change = True
            linetoChange = i
        print("Credit Hours: {}".format(groups[i - 1].creditHours), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Credit Hours:(1--->4) ")
        while isValidModifying(0, 5) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Credit Hours: {}".format(groups[i - 1].creditHours), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Credit Hours:(1--->4) ")
        if inp == 'b':
            clear()
            return viewGroups(i)
        if inp != 'n':
            groups[i - 1].creditHours = int(inp)
            change = True
            linetoChange = i
    elif inp == '2':
        print("Course Term: {}".format(groups[i - 1].courseTerm), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Course's Term: ")
        while isValidModifying(0, 11) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Course Term: {}".format(groups[i - 1].courseTerm), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Course's Term: ")
        if inp == 'b':
            clear()
            return viewGroups(i)
        if inp != 'n':
            groups[i - 1].courseTerm = int(inp)
            change = True
            linetoChange = i
    elif inp == '3':
        print("Instructor Name: {}".format(groups[i - 1].lecture.instName), end='   ---->   ')
        inp = input("(n->No change & b->Back) New Instructor's Name: ")
        if inp == 'b':
            clear()
            return viewGroups(i)
        if inp != 'n':
            groups[i - 1].lecture.instName = inp
            change = True
            linetoChange = i
    elif inp == '4':
        clear()
        return modifyGroup(groups[i - 1], i)
    elif inp == 'b':
        clear()
        return viewGroups()
    else:
        clear()
        print("Invalid input ---> (1, 2, 3, 4, 5, b)")
        return lastGroupsMenu(i)


def tutorialsMenu(group, savedGroup=None):
    global inp, change, linetoChange
    if len(group.tutorials) == 0:
        print("No tutorials in this group")
        return modifyGroup(group, savedGroup)
    else:
        print("(b)Back")
        for i in range(len(group.tutorials)):
            print("1.({})Tutorial Place: {}".format(i + 1, group.tutorials[i].place), end="      ")
            print("2.({})Tutorial Type: {}".format(i + 1, group.tutorials[i].type), end="      ")
            print("3.({})Tutorial Day: {}".format(i + 1, group.tutorials[i].time.day), end="      ")
            print("4.({})Tutorial From: {}".format(i + 1, group.tutorials[i].time.fr), end="      ")
            print("5.({})Tutorial To: {}".format(i + 1, group.tutorials[i].time.to))
        i = 0
        if len(group.tutorials) == 2:
            inp = input("Which Tutorial? (1 Or 2) ")
            while isValidModifying(0, 3, False) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                inp = input("Which Tutorial? (1 Or 2) ")
            if inp == 'b':
                clear()
                return modifyGroup(group, savedGroup)
            i = int(inp)
        inp = input("Which property? ")
        if inp == '1':
            inp = input("(n->No change & b->Back) New Tutorial's Place: ")
            if inp == 'b':
                clear()
                return tutorialsMenu(group, savedGroup)
            if inp != 'n':
                group.tutorials[i - 1].place = inp
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == '2':
            inp = input("(n->No change & b->Back) New Tutorial's Type:(1 Or 2) ")
            while isValidModifying(0, 3) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                print("Tutorial Type: {}".format(group.tutorials[i - 1].type), end='   ---->   ')
                inp = input("(n->No change & b->Back) New Tutorial's Type:(1 Or 2) ")
            if inp == 'b':
                clear()
                return tutorialsMenu(group, savedGroup)
            if inp != 'n':
                group.tutorials[i - 1].type = int(inp)
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == '3':
            inp = input("(n->No change & b->Back) New Tutorial's Day:(0--->5) ")
            while isValidModifying(-1, 6) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                print("Tutorial Day: {}".format(group.tutorials[i - 1].time.day), end='   ---->   ')
                inp = input("(n->No change & b->Back) New Tutorial's Day:(0--->5) ")
            if inp == 'b':
                clear()
                return tutorialsMenu(group, savedGroup)
            if inp != 'n':
                group.tutorials[i - 1].time.day = int(inp)
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == '4':
            inp = input("(n->No change & b->Back) New Tutorial's From:(0--->11) ")
            while isValidModifying(-1, 12) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                print("Tutorial From: {}".format(group.tutorials[i - 1].time.fr), end='   ---->   ')
                inp = input("(n->No change & b->Back) New Tutorial's From:(0--->11) ")
            if inp == 'b':
                clear()
                return tutorialsMenu(group, savedGroup)
            if inp != 'n':
                group.tutorials[i - 1].time.fr = int(inp)
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == '5':
            inp = input("(n->No change & b->Back) New Tutorial's To:(0--->11) ")
            while isValidModifying(-1, 12) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                print("Tutorial To: {}".format(group.tutorials[i - 1].time.to), end='   ---->   ')
                inp = input("(n->No change & b->Back) New Tutorial's To:(0--->11) ")
            if inp == 'b':
                clear()
                return tutorialsMenu(group, savedGroup)
            if inp != 'n':
                group.tutorials[i - 1].time.to = int(inp)
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == 'b':
            clear()
            return modifyGroup(group, savedGroup)
        else:
            print("Invalid input ---> (1, 2, 3, 4, 5, b)")
            return tutorialsMenu(group, savedGroup)


def labsMenu(group, savedGroup=None):
    global inp, change, linetoChange
    if len(group.labs) == 0:
        print("No labs in this group")
        return modifyGroup(group, savedGroup)
    else:
        print("(b)Back")
        for i in range(len(group.labs)):
            print("1.({})Lab Place: {}".format(i + 1, group.labs[i].place), end="      ")
            print("2.({})Lab Type: {}".format(i + 1, group.labs[i].type), end="      ")
            print("3.({})Lab Day: {}".format(i + 1, group.labs[i].time.day), end="      ")
            print("4.({})Lab From: {}".format(i + 1, group.labs[i].time.fr), end="      ")
            print("5.({})Lab To: {}".format(i + 1, group.labs[i].time.to))
        i = 1
        if len(group.labs) == 2:
            inp = input("Which Lab? (1 Or 2) ")
            while isValidModifying(0, 3, False) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                inp = input("Which Lab? (1 Or 2) ")
            if inp == 'b':
                clear()
                return modifyGroup(group, savedGroup)
            i = int(inp)
        inp = input("Which property? ")
        if inp == '1':
            inp = input("(n->No change & b->Back) New Lab's Place: ")
            if inp == 'b':
                clear()
                return labsMenu(group, savedGroup)
            if inp != 'n':
                group.labs[i - 1].place = inp
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == '2':
            inp = input("(n->No change & b->Back) New Lab's Type:(1 Or 2) ")
            while isValidModifying(0, 3) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                print("Lab Type: {}".format(group.labs[i - 1].type), end='   ---->   ')
                inp = input("(n->No change & b->Back) New Lab's Type:(1 Or 2) ")
            if inp == 'b':
                clear()
                return labsMenu(group, savedGroup)
            if inp != 'n':
                group.labs[i - 1].type = int(inp)
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == '3':
            inp = input("(n->No change & b->Back) New Lab's Day:(0--->5) ")
            while isValidModifying(-1, 6) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                print("Lab Day: {}".format(group.labs[i - 1].time.day), end='   ---->   ')
                inp = input("(n->No change & b->Back) New Lab's Day:(0--->5) ")
            if inp == 'b':
                clear()
                return labsMenu(group, savedGroup)
            if inp != 'n':
                group.labs[i - 1].time.day = int(inp)
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == '4':
            inp = input("(n->No change & b->Back) New Lab's From:(0--->11) ")
            while isValidModifying(-1, 12) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                print("Lab From: {}".format(group.labs[i - 1].time.fr), end='   ---->   ')
                inp = input("(n->No change & b->Back) New Lab's From:(0--->11) ")
            if inp == 'b':
                clear()
                return labsMenu(group, savedGroup)
            if inp != 'n':
                group.labs[i - 1].time.fr = int(inp)
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == '5':
            inp = input("(n->No change & b->Back) New Lab's To:(0--->11) ")
            while isValidModifying(-1, 12) != 'v':
                if inp == 'b':
                    print("Invalid number ---> Input must satisfy boundaries")
                elif inp == 'i':
                    print("Invalid input")
                print("Lab To: {}".format(group.labs[i - 1].time.to), end='   ---->   ')
                inp = input("(n->No change & b->Back) New Lab's To:(0--->11) ")
            if inp == 'b':
                clear()
                return labsMenu(group, savedGroup)
            if inp != 'n':
                group.labs[i - 1].time.to = int(inp)
                if savedGroup is not None:
                    change = True
                    linetoChange = savedGroup
        elif inp == 'b':
            clear()
            return modifyGroup(group, savedGroup)
        else:
            print("Invalid input ---> (1, 2, 3, 4, 5, b)")
            return labsMenu(group, savedGroup)


def isValidFilling(leftBound, rightBound):
    global inp
    if leftBound is None and rightBound is None:  # no validation
        return 2
    while True:
        if type(leftBound) == int and type(rightBound) == int:
            if inp.isdigit():
                if leftBound < int(inp) < rightBound:
                    return 2  # valid number
                else:
                    return 'b'  # invalid number
            else:
                return 'i'  # invalid input
        else:
            if inp == leftBound or inp == rightBound:
                return 2  # valid string
            return 'is'  # invalid input


def isValidModifying(leftBound, rightBound, n=True):
    global inp
    if inp.isdigit():
        if leftBound < int(inp) < rightBound:
            return 'v'  # valid number
        else:
            inp = 'b'  # invalid number
    else:
        if inp == 'b':
            return 'v'  # valid character
        elif inp == 'n':
            if n:
                return 'v'  # n character is valid
            inp = 'i'  # n character is not valid
        else:
            inp = 'i'  # invalid input


def lectureMenu(group, savedGroup=None):
    global inp, change, linetoChange
    warningString = "Invalid input ---> (1, 2, 3, 4, 5, b)"
    print("(b)Back")
    print("1.Lecture Place: {}".format(group.lecture.place), end="      ")
    print("2.Lecture Type: {}".format(group.lecture.type), end="      ")
    print("3.Lecture Day: {}".format(group.lecture.time.day), end="      ")
    print("4.Lecture From: {}".format(group.lecture.time.fr), end="      ")
    print("5.Lecture To: {}".format(group.lecture.time.to))
    if group.lecExDay != '':
        warningString = "Invalid input ---> (1, 2, 3, 4, 5, 6, 7, 8, 9, b)"
        print("6.Lecture Extension Place: {}".format(group.lecExPlace), end='      ')
        print("7.Lecture Extension Day: {}".format(group.lecExDay), end='      ')
        print("8.Lecture Extension From: {}".format(group.lecExFrom), end='      ')
        print("9.Lecture Extension To: {}".format(group.lecExTo))
    inp = input("Which property? ")
    if inp == '1':
        inp = input("(n->No change & b->Back) New Lecture's Place: ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecture.place = inp
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif inp == '2':
        inp = input("(n->No change & b->Back) New Lecture's Type:(1 Or 2) ")
        while isValidModifying(0, 3) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Lecture Type: {}".format(group.lecture.type), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Lecture's Type:(1 Or 2) ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecture.type = int(inp)
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif inp == '3':
        inp = input("(n->No change & b->Back) New Lecture's Day:(0--->5) ")
        while isValidModifying(-1, 6) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Lecture Day: {}".format(group.lecture.time.day), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Lecture's Day:(0--->5) ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecture.time.day = int(inp)
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif inp == '4':
        inp = input("(n->No change & b->Back) New Lecture's From:(0--->11) ")
        while isValidModifying(-1, 12) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Lecture From: {}".format(group.lecture.time.fr), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Lecture's From:(0--->11) ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecture.time.fr = int(inp)
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif inp == '5':
        inp = input("(n->No change & b->Back) New Lecture's To:(0--->11) ")
        while isValidModifying(-1, 12) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Lecture To: {}".format(group.lecture.time.to), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Lecture's To:(0--->11) ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecture.time.to = int(inp)
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif inp == 'b':
        clear()
        return modifyGroup(group, savedGroup)
    elif group.lecExDay != '' and inp == '6':
        inp = input("(n->No change & b->Back) New Lecture's Extension Place: ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecExPlace = inp
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif group.lecExDay != '' and inp == '7':
        inp = input("(n->No change & b->Back) New Lecture's Extension Day:(0--->5) ")
        while isValidModifying(-1, 6) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Lecture Day: {}".format(group.lecExDay), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Lecture's Extension Day:(0--->5) ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecExDay = int(inp)
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif group.lecExDay != '' and inp == '8':
        inp = input("(n->No change & b->Back) New Lecture's Extension From:(0--->11) ")
        while isValidModifying(-1, 12) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Lecture From: {}".format(group.lecExFrom), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Lecture's Extension From:(0--->11) ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecExFrom = int(inp)
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    elif group.lecExDay != '' and inp == '9':
        inp = input("(n->No change & b->Back) New Lecture's Extension To:(0--->11) ")
        while isValidModifying(-1, 12) != 'v':
            if inp == 'b':
                print("Invalid number ---> Input must satisfy boundaries")
            elif inp == 'i':
                print("Invalid input")
            print("Lecture To: {}".format(group.lecExTo), end='   ---->   ')
            inp = input("(n->No change & b->Back) New Lecture's Extension To:(0--->11) ")
        if inp == 'b':
            clear()
            return lectureMenu(group, savedGroup)
        if inp != 'n':
            group.lecExTo = int(inp)
            if savedGroup is not None:
                change = True
                linetoChange = savedGroup
    else:
        clear()
        print(warningString)
        return lectureMenu(group, savedGroup)


def clear():
    pyautogui.hotkey('ctrl', 'shift', ';')


def filling():
    global courseName, courseTerm, instructorName, inp, finish, creditHours
    first = True
    while True:
        group = SchGroup()
        lecture = Lecture()
        group.lecture = lecture
        if first:
            mainMenu()
            if checkInp(group, "Course Term:(1--->10) ", 0, 11):
                break
            courseTerm = int(inp)
            clear()
            mainMenu()
            if checkInp(group, "Course Name: "):
                break
            courseName = inp
            clear()
            mainMenu()
            if checkInp(group, "Credit Hours:(1--->4) ", 0, 5):
                break
            creditHours = int(inp)
            clear()
            mainMenu()
            if checkInp(group, "Instructor Name: "):
                break
            instructorName = inp
            first = False
        clear()
        mainMenu()
        if checkInp(group, "Group Number:(1--->6) ", 0, 7):
            break
        group.number = int(inp)
        group.courseTerm = courseTerm
        group.creditHours = creditHours
        lecture.groupNum = group.number
        lecture.periodType = 'Lecture'
        lecture.courseName = courseName
        lecture.instName = instructorName
        clear()
        mainMenu()
        if checkInp(group, "Lec place: "):
            break
        lecture.place = inp
        clear()
        mainMenu()
        if checkInp(group, "Lec Type:(1 Or 2) ", 0, 3):
            break
        lecture.type = int(inp)
        clear()
        mainMenu()
        if checkInp(group, "Lec Day:(0--->5) ", -1, 6):
            break
        lecture.time.day = int(inp)
        clear()
        mainMenu()
        if checkInp(group, "Lec From:(0--->11) ", -1, 12):
            break
        lecture.time.fr = int(inp)
        clear()
        mainMenu()
        if checkInp(group, "Lec To:(0--->11) ", -1, 12):
            break
        lecture.time.to = int(inp)
        clear()
        mainMenu()
        if checkInp(group, "Have Lecture Extension? (yes Or no) ", 'yes', 'no'):
            break
        if inp == "yes":
            clear()
            mainMenu()
            if checkInp(group, "Lec Extension place: "):
                break
            group.lecExPlace = inp
            clear()
            mainMenu()
            if checkInp(group, "Lec Extension Day:(0--->5) ", -1, 6):
                break
            group.lecExDay = int(inp)
            clear()
            mainMenu()
            if checkInp(group, "Lec Extension From:(0--->11) ", -1, 12):
                break
            group.lecExFrom = int(inp)
            clear()
            mainMenu()
            if checkInp(group, "Lec Extension From:(0--->11) ", -1, 12):
                break
            group.lecExTo = int(inp)
        clear()
        mainMenu()
        if checkInp(group, "Have Tutorial? (yes Or no) ", 'yes', 'no'):
            break
        if inp == "yes":
            clear()
            mainMenu()
            tut = Tutorial()
            if createTut(tut, group):
                break
            group.add_tut(tut)
            clear()
            mainMenu()
            if checkInp(group, "Another Tutorial? (yes Or no) ", 'yes', 'no'):
                break
            if inp == "yes":
                clear()
                mainMenu()
                tut = Tutorial()
                if createTut(tut, group):
                    break
                group.add_tut(tut)

        clear()
        mainMenu()
        if checkInp(group, "Have Lab? (yes Or no) ", 'yes', 'no'):
            break
        if inp == "yes":
            clear()
            mainMenu()
            lab = Lab()
            if createLab(lab, group):
                break
            group.add_lab(lab)
            clear()
            mainMenu()
            if checkInp(group, "Another Lab? (yes Or no) ", 'yes', 'no'):
                break
            if inp == 'yes':
                clear()
                mainMenu()
                lab = Lab()
                if createLab(lab, group):
                    break
                group.add_lab(lab)
        groups.append(group)
        writeFile(group)


def writeFile(group=None):
    global linetoChange
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fpath = os.path.join(BASE_DIR, 'Database.csv')
    empty = ",,,,,,,"
    if group is not None:
        f = open(fpath, 'a')
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
    else:
        lines = open(fpath, 'r').readlines()
        # f.write("Term_NUM,Credit_Hours,NUM,LEC_INST_NAME,LEC_CRS_NAME,LEC_PLACE,LEC_TYPE,LEC_DAY,LEC_FROM,LEC_TO,"
        #         "Lec_Ex_Day,Lec_Ex_From,Lec_Ex_To,LEC_PER_TYPE,TUT1_INST_NAME,"
        #         "TUT1_CRS_NAME,TUT1_PLACE,TUT1_TYPE,TUT1_DAY,TUT1_FROM,TUT1_TO,TUT1_PER_TYPE,TUT2_INST_NAME,"
        #         "TUT2_CRS_NAME,TUT2_PLACE,TUT2_TYPE,TUT2_DAY,TUT2_FROM,TUT2_TO,TUT2_PER_TYPE,LAB1_INST_NAME,"
        #         "LAB1_CRS_NAME,LAB1_PLACE,LAB1_TYPE,LAB1_DAY,LAB1_FROM,LAB1_TO,LAB1_PER_TYPE,LAB2_INST_NAME,"
        #         "LAB2_CRS_NAME,LAB2_PLACE,LAB2_TYPE,LAB2_DAY,LAB2_FROM,LAB2_TO,LAB2_PER_TYPE\n")
        # for i in range(len(groups)):

        text = '{},{},{},'.format(groups[linetoChange - 1].courseTerm, groups[linetoChange - 1].creditHours,
                                  groups[linetoChange - 1].number)
        text += '{},{},{},{},{},{},{},{},{},{},{},{},'.format(groups[linetoChange - 1].lecture.instName,
                                                              groups[linetoChange - 1].lecture.courseName,
                                                              groups[linetoChange - 1].lecture.place,
                                                              groups[linetoChange - 1].lecture.type,
                                                              groups[linetoChange - 1].lecture.time.day,
                                                              groups[linetoChange - 1].lecture.time.fr,
                                                              groups[linetoChange - 1].lecture.time.to,
                                                              groups[linetoChange - 1].lecExPlace,
                                                              groups[linetoChange - 1].lecExDay,
                                                              groups[linetoChange - 1].lecExFrom,
                                                              groups[linetoChange - 1].lecExTo,
                                                              groups[linetoChange - 1].lecture.periodType)
        if len(groups[linetoChange - 1].tutorials) == 0:
            text += empty + ","
            text += empty + ","
        elif len(groups[linetoChange - 1].tutorials) == 1:
            text += '{},{},{},{},{},{},{},{},'.format(groups[linetoChange - 1].tutorials[0].instName,
                                                      groups[linetoChange - 1].tutorials[0].courseName,
                                                      groups[linetoChange - 1].tutorials[0].place,
                                                      groups[linetoChange - 1].tutorials[0].type,
                                                      groups[linetoChange - 1].tutorials[0].time.day,
                                                      groups[linetoChange - 1].tutorials[0].time.fr,
                                                      groups[linetoChange - 1].tutorials[0].time.to,
                                                      groups[linetoChange - 1].tutorials[0].periodType)
            text += empty + ","
        else:
            for j in range(2):
                text += '{},{},{},{},{},{},{},{},'.format(groups[linetoChange - 1].tutorials[j].instName,
                                                          groups[linetoChange - 1].tutorials[j].courseName,
                                                          groups[linetoChange - 1].tutorials[j].place,
                                                          groups[linetoChange - 1].tutorials[0].type,
                                                          groups[linetoChange - 1].tutorials[j].time.day,
                                                          groups[linetoChange - 1].tutorials[j].time.fr,
                                                          groups[linetoChange - 1].tutorials[j].time.to,
                                                          groups[linetoChange - 1].tutorials[j].periodType)
        if len(groups[linetoChange - 1].labs) == 0:
            text += empty + ","
            text += empty + "\n"
        elif len(groups[linetoChange - 1].labs) == 1:
            text += '{},{},{},{},{},{},{},{},'.format(groups[linetoChange - 1].labs[0].instName,
                                                      groups[linetoChange - 1].labs[0].courseName,
                                                      groups[linetoChange - 1].labs[0].place,
                                                      groups[linetoChange - 1].labs[0].type,
                                                      groups[linetoChange - 1].labs[0].time.day,
                                                      groups[linetoChange - 1].labs[0].time.fr,
                                                      groups[linetoChange - 1].labs[0].time.to,
                                                      groups[linetoChange - 1].labs[0].periodType)
            text += empty + "\n"
        else:
            for j in range(2):
                if j == 0:
                    end = ","
                else:
                    end = "\n"
                text += '{},{},{},{},{},{},{},{}{}'.format(groups[linetoChange - 1].labs[j].instName,
                                                           groups[linetoChange - 1].labs[j].courseName,
                                                           groups[linetoChange - 1].labs[j].place,
                                                           groups[linetoChange - 1].labs[0].type,
                                                           groups[linetoChange - 1].labs[j].time.day,
                                                           groups[linetoChange - 1].labs[j].time.fr,
                                                           groups[linetoChange - 1].labs[j].time.to,
                                                           groups[linetoChange - 1].labs[j].periodType, end)
        lines[linetoChange + len(lines) - len(groups) - 1] = text
        f = open(fpath, 'w')
        f.writelines(lines)
    f.close()


if __name__ == '__main__':
    print("بسم الله الرحمن الرحيم")
    print("Welcome to Database Filler Application. Let's start the journey\n")
    filling()
    print("Information saved to the file successfully")
    print("Congratulations")
