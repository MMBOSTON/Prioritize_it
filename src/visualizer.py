import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self):
        sns.set()

    def plot_pareto(self, tasks):
        tasks.sort(key=lambda x: x.ratio, reverse=True)
        values = [task.value for task in tasks]
        labels = [task.description for task in tasks]
        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_xlabel('Tasks')
        ax.set_ylabel('Value/Effort Ratio')
        ax.set_title('Pareto Chart')
        return fig

    def plot_burndown(self, tasks):
        tasks.sort(key=lambda x: x.ratio, reverse=True)
        cumulative_value = [sum(task.value for task in tasks[:i+1]) for i in range(len(tasks))]
        labels = range(1, len(tasks) + 1)
        fig, ax = plt.subplots()
        ax.plot(labels, cumulative_value)
        ax.set_xlabel('Tasks Completed')
        ax.set_ylabel('Total Value Delivered')
        ax.set_title('Value Burndown Chart')
        return fig