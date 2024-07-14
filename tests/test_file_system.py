
import os
import unittest
from unittest.mock import patch, mock_open
import drafter.file_system as fs


class TestFileSystem(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_is_valid_item(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = True
        self.assertTrue(fs.is_valid_item('test_dir'))

        mock_isdir.return_value = False
        mock_isfile.return_value = True
        self.assertTrue(fs.is_valid_item('test_file.py'))

        mock_isdir.return_value = False
        mock_isfile.return_value = False
        self.assertFalse(fs.is_valid_item('invalid_item'))

    @patch('drafter.file_system.iterate_project_path')
    def test_generate_file_structure(self, mock_iterate):
        mock_iterate.return_value = ['test/dir/', 'test/file.py']
        structure = fs.generate_file_structure('test')
        self.assertIn('Project file structure:', structure)


if __name__ == '__main__':
    unittest.main()
