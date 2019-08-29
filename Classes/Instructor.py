class Instructor:
    def __init__(self):
        self.priority = 0
        self.name = ''
        self.courseName = ''
        self.groups = []

    def add_group(self, group):
        self.groups.append(group)
