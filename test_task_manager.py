import unittest
from unittest.mock import patch, mock_open
from task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        with patch.object(TaskManager, 'load_tasks'), patch.object(TaskManager, 'save_tasks'):
            self.tm = TaskManager()

    @patch("builtins.open", new_callable=mock_open)
    def test_add_task(self, mock_file):
        with patch("builtins.print") as mock_print:
            self.tm.add_task("Test Task")
            mock_print.assert_called_with("Tarea añadida: Test Task")
        self.assertEqual(len(self.tm._tasks), 1)
        self.assertEqual(self.tm._tasks[0].description, "Test Task")

    @patch("builtins.open", new_callable=mock_open)
    def test_delete_task(self, mock_file):
        self.tm.add_task("Task to delete")
        task_id = self.tm._tasks[0].id
        with patch("builtins.print") as mock_print:
            self.tm.delete_task(task_id)
            mock_print.assert_called_with(f"Tarea eliminada: #{task_id}")
        self.assertEqual(len(self.tm._tasks), 0)

    @patch("builtins.open", new_callable=mock_open)
    def test_delete_nonexistent_task(self, mock_file):
        with patch("builtins.print") as mock_print:
            self.tm.delete_task(999)
            mock_print.assert_called_with("Tarea no encontrada: #999")

    @patch("builtins.open", new_callable=mock_open)
    def test_list_tasks(self, mock_file):
        self.tm.add_task("Task 1")
        self.tm.add_task("Task 2")
        with patch("builtins.print") as mock_print:
            self.tm.list_tasks()
            self.assertTrue(mock_print.call_count >= 2)

    @patch("builtins.open", new_callable=mock_open)
    def test_complete_task(self, mock_file):
        self.tm.add_task("Task to complete")
        task_id = self.tm._tasks[0].id
        with patch("builtins.print") as mock_print:
            self.tm.complete_task(task_id)
            mock_print.assert_called_with(f"Tarea completada: [✓] #{task_id}: Task to complete")
        self.assertTrue(self.tm._tasks[0].completed)


if __name__ == "__main__":
    unittest.main()
