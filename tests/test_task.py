import unittest
import logging
from src.task import Task
from src.prioritize_it import PrioritizeIt

# Set up logging
logging.basicConfig(filename='tests/test.log', level=logging.INFO)

class TestTask(unittest.TestCase):
    def setUp(self):
        self.prioritize = PrioritizeIt()
        self.task = Task('Test task', 10, 5)
        logging.info(f"Set up task with description: {self.task.description}, value: {self.task.value}, effort: {self.task.effort}")

    def test_task_description(self):
        self.assertEqual(self.task.description, 'Test task')
        logging.info("test_task_description passed")

    def test_task_value(self):
        self.assertEqual(self.task.value, 10)
        logging.info("test_task_value passed")

    def test_task_effort(self):
        self.assertEqual(self.task.effort, 5)
        logging.info("test_task_effort passed")

    def test_calculate_ratio(self):
        self.assertEqual(self.task.ratio, 2)
        logging.info("test_calculate_ratio passed")

    def test_add_task(self):
        self.prioritize.add_task(self.task.description, self.task.value, self.task.effort)
        tasks = self.prioritize.view_tasks()
        self.assertEqual(len(tasks), 1)
        logging.info("test_add_task passed")

    def test_remove_task(self):
        self.prioritize.add_task(self.task.description, self.task.value, self.task.effort)
        self.prioritize.remove_task(self.task.description)
        tasks = self.prioritize.view_tasks()
        self.assertEqual(len(tasks), 0)
        logging.info("test_remove_task passed")

    def test_view_tasks(self):
        self.prioritize.add_task(self.task.description, self.task.value, self.task.effort)
        tasks = self.prioritize.view_tasks()
        self.assertEqual(len(tasks), 1)
        logging.info("test_view_tasks passed")

    def test_generate_report(self):
        self.prioritize.add_task(self.task.description, self.task.value, self.task.effort)
        report = self.prioritize.generate_report()
        self.assertIn("Total tasks: 1", report)
        logging.info("test_generate_report passed")

    def test_visualize_tasks(self):
        self.prioritize.add_task(self.task.description, self.task.value, self.task.effort)
        pareto_chart, burndown_chart = self.prioritize.visualize_tasks(self.prioritize.view_tasks())
        self.assertIsNotNone(pareto_chart)
        self.assertIsNotNone(burndown_chart)
        logging.info("test_visualize_tasks passed")

    def tearDown(self):
        logging.info(f"Tear down task with description: {self.task.description}, value: {self.task.value}, effort: {self.task.effort}")


if __name__ == '__main__':
    unittest.main()