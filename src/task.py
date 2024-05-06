class Task:
    def __init__(self, description, value, effort, ratio=None):
        self.description = description
        self.value = value
        self.effort = effort
        self.ratio = ratio # This line is new

    def calculate_ratio(self):
        if self.effort == 0:
            self.ratio = 0 # Or any other appropriate value for division by zero
        else:
            self.ratio = self.value / self.effort