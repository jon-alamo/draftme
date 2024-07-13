import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
import drafter.llm_interface as llm_interface


class TestResponse(unittest.TestCase):

    @unittest.mock.patch('drafter.llm_interface.write_file')
    def test_response(self, write_file_mock):
        write_file_mock.return_value = None
        with open('tests/fixtures/response.txt', 'r') as f:
            response = f.read()
        llm_interface.execute_response(response)
