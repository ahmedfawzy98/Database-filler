from Classes.Time import Time


class Period:
    def __init__(self):
        self.instName = ''
        self.courseName = ''
        self.place = ''
        self.type = ''
        self.time = Time()
        self.length = ''
        self.groupNum = ''
        self.periodType = ''

    def printMe(self):
        info = '(' + str(self.groupNum) + ')' + str(self.courseName) + '-' + str(self.periodType)
        print(info, end='')
        for i in range(38-len(info)):
            print(end=' ')

    def setTime(self, time):
        self.time = time
        if self.time.day == '':
            self.time.day = 0
        if self.time.fr == '':
            self.time.fr = 0
        if self.time.to == '':
            self.time.to = 0
        self.length = self.time.to - self.time.fr + 1
