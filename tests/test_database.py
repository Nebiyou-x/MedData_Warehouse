import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath('scripts'))
from database import DbConn


class TestDatabase(unittest.TestCase):

    @patch('database.psycopg2.connect')
    def test_database_connection(self, mock_connect):

        db = DbConn()

        mock_connect.assert_called_once_with(
            database= os.getenv('DB_NAME'),
            user= os.getenv('DB_USER'),
            password= os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port= os.getenv('DB_PORT')
        )        



if __name__ == "__main__":
    unittest.main(verbosity= 1)
