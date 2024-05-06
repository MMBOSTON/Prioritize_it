class Task:
    def __init__(self, description, value, effort):
        self.description = description
        self.value = value
        self.effort = effort
        self.ratio = self.calculate_ratio()

    def calculate_ratio(self):
        if self.effort == 0:
            return 0
        return self.value / self.effort