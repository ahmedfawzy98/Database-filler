from Classes.Lecture import Lecture


class SchGroup:
    def __init__(self, lecture=False):
        self.lecture = None
        if lecture:
            self.lecture = Lecture()
        self.tutorials = []
        self.labs = []
        self.number = None
        self.courseTerm = None
        self.lecExPlace = ''
        self.lecExDay = ''
        self.lecExFrom = ''
        self.lecExTo = ''
        self.creditHours = None
        self.tut_wait = False
        self.lab_wait = False
        self.lab_case = None
        self.tut_case = None

    def setLecture(self, lecture):
        self.lecture = lecture
        # self.daysTaken.add(lecture.time.day)

    def add_lab(self, lab):
        self.labs.append(lab)
        # self.daysTaken.add(lab.time.day)

    def add_tut(self, tut):
        self.tutorials.append(tut)
        # self.daysTaken.add(tut.time.day)
