import json
import random
from typing import List

from faker import Faker

fake = Faker()

class TaskCore:
    def __init__(self, name, description, task_value, task_effort, task_id=None):
        self.name = name
        self.description = description
        self.task_value = task_value
        self.task_effort = task_effort
        self.task_id = task_id if task_id else fake.uuid4()

def generate_core_tasks(num_tasks: int = 25) -> List[TaskCore]:
    tasks = []
    domains = ['AI/ML/Data Science', 'Product Management', 'App Development and Delivery', 'Project Management', 'Marketing and Sales', 'Customer Success', 'Mobile App Development']
    
    for _ in range(num_tasks):
        # Randomly select a domain for each task
        domain = random.choice(domains)
        
        # Customize the task generation based on the selected domain
        if domain == 'AI/ML/Data Science':
            task_name = fake.sentence(ext_word_list=['Machine Learning', 'Deep Learning', 'Data Mining', 'Neural Networks'])
            task_description = fake.text(max_nb_chars=200, ext_word_list=['Algorithm', 'Model', 'Feature', 'Prediction'])
        elif domain == 'Product Management':
            task_name = fake.sentence(ext_word_list=['Product Launch', 'Market Research', 'Competitor Analysis', 'Customer Feedback'])
            task_description = fake.text(max_nb_chars=200, ext_word_list=['Strategy', 'Roadmap', 'Innovation', 'Market'])
        elif domain == 'App Development and Delivery':
            task_name = fake.sentence(ext_word_list=['App Development', 'User Interface', 'Backend Development', 'Testing'])
            task_description = fake.text(max_nb_chars=200, ext_word_list=['Functionality', 'Performance', 'Security', 'User Experience'])
        elif domain == 'Project Management':
            task_name = fake.sentence(ext_word_list=['Project Planning', 'Resource Allocation', 'Risk Management', 'Project Closure'])
            task_description = fake.text(max_nb_chars=200, ext_word_list=['Timeline', 'Budget', 'Team', 'Objectives'])
        elif domain == 'Marketing and Sales':
            task_name = fake.sentence(ext_word_list=['Marketing Campaign', 'Sales Strategy', 'Customer Relationship', 'Market Analysis'])
            task_description = fake.text(max_nb_chars=200, ext_word_list=['Target Audience', 'Marketing Channels', 'Sales Funnel', 'Customer Retention'])
        elif domain == 'Customer Success':
            task_name = fake.sentence(ext_word_list=['Customer Onboarding', 'Customer Support', 'Customer Feedback', 'Customer Retention'])
            task_description = fake.text(max_nb_chars=200, ext_word_list=['Customer Satisfaction', 'Support Tickets', 'Product Feedback', 'Customer Journey'])
        elif domain == 'Mobile App Development':
            task_name = fake.sentence(ext_word_list=['App Design', 'User Experience', 'Backend Development', 'Testing'])
            task_description = fake.text(max_nb_chars=200, ext_word_list=['Functionality', 'Performance', 'Security', 'User Interface'])
        else:
            task_name = fake.sentence()
            task_description = fake.text(max_nb_chars=200)

        tasks.append(TaskCore(
            name=task_name,
            description=task_description,
            task_value=fake.random_int(min=1, max=1000),
            task_effort=fake.random_int(min=1, max=100)
        ))
    return tasks

def save_tasks_to_json(tasks: List[TaskCore], filename: str = 'data/core_tasks.json'):
    task_data = [task.__dict__ for task in tasks]
    with open(filename, 'w') as f:
        json.dump(task_data, f)

# Example usage
if __name__ == "__main__":
    tasks = generate_core_tasks()
    save_tasks_to_json(tasks)