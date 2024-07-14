
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
import drafter.llm_interface as llm_interface


class TestLLMInterface(unittest.TestCase):

    @patch.dict(os.environ, {"OPENAI_API_KEY": "testkey"})
    @patch('drafter.llm_interface.client')
    def test_get_iteration(self, mock_openai):
        mock_openai.chat.completions.create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content="[PROPOSAL] [ADD] test.txt\n```Hello World!```"
                    )
                )
            ]
        )
        command = "Add a test file"
        response = llm_interface.get_iteration(command)
        self.assertIn("[PROPOSAL] [ADD] test.txt", response)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_write_file(self, mock_makedirs, mock_file):
        llm_interface.write_file('test.txt', 'Hello World')
        mock_file.assert_called_once_with('test.txt', 'w')
        mock_file().write.assert_called_once_with('Hello World')
        mock_makedirs.assert_called_once_with('', exist_ok=True)

    @patch('os.remove')
    def test_delete_file(self, mock_remove):
        llm_interface.delete_file('test.txt')
        mock_remove.assert_called_once_with('test.txt')

    def test_parse_action(self):
        method, path = llm_interface.parse_action('[PROPOSAL] [ADD] test.txt')
        self.assertEqual(method, llm_interface.create_file)
        self.assertEqual(path, './test.txt')

        method, path = llm_interface.parse_action('[PROPOSAL] [EDIT] test.txt')
        self.assertEqual(method, llm_interface.edit_file)
        self.assertEqual(path, './test.txt')

        method, path = llm_interface.parse_action('[PROPOSAL] [DELETE] test.txt')
        self.assertEqual(method, llm_interface.delete_file)
        self.assertEqual(path, './test.txt')

    @patch('drafter.llm_interface.create_file')
    def test_run_operation_create(self, mock_create):
        llm_interface.run_operation(llm_interface.create_file, 'test.txt', ['Hello', 'World'])
        mock_create.assert_called_once_with('test.txt', 'Hello\nWorld')

    @patch('drafter.llm_interface.edit_file')
    def test_run_operation_edit(self, mock_edit):
        llm_interface.run_operation(llm_interface.edit_file, 'test.txt', ['Hello', 'World'])
        mock_edit.assert_called_once_with('test.txt', 'Hello\nWorld')

    @patch('drafter.llm_interface.delete_file')
    def test_run_operation_delete(self, mock_delete):
        llm_interface.run_operation(llm_interface.delete_file, 'test.txt', None)
        mock_delete.assert_called_once_with('test.txt', '')


if __name__ == '__main__':
    unittest.main()
