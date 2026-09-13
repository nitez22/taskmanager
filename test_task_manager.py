import unittest
from unittest.mock import patch, mock_open

from task_manager import Task, TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        with patch.object(TaskManager, "load_tasks"), patch.object(
            TaskManager, "save_tasks"
        ):
            self.tm = TaskManager()

    @patch("builtins.open", new_callable=mock_open)
    def test_add_task(self, mock_file):
        with patch("builtins.print") as mock_print:
            self.tm.add_task("Test Task")
            mock_print.assert_called_with("Tarea añadida: Test Task")

        self.assertEqual(len(self.tm._tasks), 1)
        self.assertEqual(self.tm._tasks[0].description, "Test Task")
        self.assertEqual(self.tm._next_id, 2)

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
        self.tm._tasks = [
            Task(1, "Task 1"),
            Task(2, "Task 2"),
        ]

        with patch("builtins.print") as mock_print:
            self.tm.list_tasks()

        self.assertEqual(mock_print.call_count, 2)
        self.assertIs(mock_print.call_args_list[0].args[0], self.tm._tasks[0])
        self.assertIs(mock_print.call_args_list[1].args[0], self.tm._tasks[1])

    @patch("builtins.open", new_callable=mock_open)
    def test_list_tasks_empty(self, mock_file):
        with patch("builtins.print") as mock_print:
            self.tm.list_tasks()
            mock_print.assert_called_once_with("No hay tareas pendientes")

    @patch("builtins.open", new_callable=mock_open)
    def test_complete_task(self, mock_file):
        self.tm.add_task("Task to complete")
        task_id = self.tm._tasks[0].id

        with patch("builtins.print") as mock_print:
            self.tm.complete_task(task_id)
            mock_print.assert_called_with(
                f"Tarea completada: [✓] #{task_id}: Task to complete"
            )

        self.assertTrue(self.tm._tasks[0].completed)

    @patch("builtins.open", new_callable=mock_open)
    def test_complete_nonexistent_task(self, mock_file):
        with patch("builtins.print") as mock_print:
            self.tm.complete_task(999)
            mock_print.assert_called_with("Tarea no encontrada: #999")

    def test_task_str_format(self):
        pending = Task(3, "Pending task")
        finished = Task(4, "Finished task", completed=True)

        self.assertEqual(str(pending), "[ ] #3: Pending task")
        self.assertEqual(str(finished), "[✓] #4: Finished task")

    def test_load_tasks_from_json(self):
        data = (
            '[{"id": 1, "description": "Tarea cargada", "completed": true}, '
            '{"id": 2, "description": "Otra tarea", "completed": false}]'
        )

        with patch("builtins.open", new_callable=mock_open, read_data=data):
            tm = TaskManager()

        self.assertEqual(len(tm._tasks), 2)
        self.assertEqual(tm._tasks[0].description, "Tarea cargada")
        self.assertTrue(tm._tasks[0].completed)
        self.assertEqual(tm._next_id, 3)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_tasks_writes_valid_json(self, mock_file):
        self.tm.add_task("Persisted task")

        with patch("builtins.open", new_callable=mock_open) as mock_file_write:
            self.tm.save_tasks()

        mock_file_write.assert_called_once_with(self.tm.FILENAME, "w")
        written = "".join(
            call.args[0] for call in mock_file_write().write.call_args_list
        )
        self.assertIn('"id": 1', written)
        self.assertIn('"description": "Persisted task"', written)
        self.assertIn('"completed": false', written)


if __name__ == "__main__":
    unittest.main()
