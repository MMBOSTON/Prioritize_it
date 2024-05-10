class Task:
    def __init__(self, description, value, effort, ratio=None, id=None, name=None):
        self.description = description
        self.value = value
        self.effort = effort
        self.id = id
        self.name = name
        self.calculate_ratio()  # Call calculate_ratio here

    def __str__(self):
        return f"Task(name={self.name}, description={self.description}, value={self.value}, effort={self.effort}, ratio={self.ratio}, id={self.id})"

    def calculate_ratio(self):
        if self.effort == 0:
            self.ratio = 0  # Or any other appropriate value for division by zero
        else:
            self.ratio = self.value / self.effort

    def generate_report(self):
        # replace with your actual logic for generating a report
        print(f"Generating report for task: {self.name}")