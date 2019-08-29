class Course:
    def __init__(self):
        self.priority = 0
        self.name = ''
        self.instructors = []
        self.term = 0

    def add_instructor(self, instructor):
        self.instructors.append(instructor)
