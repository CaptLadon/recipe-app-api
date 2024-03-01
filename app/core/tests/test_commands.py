"""
test commands

"""

# mock behaviour of the db connection
from unittest.mock import patch

# possible error when connecting to db and db not ready
from psycopg2 import OperationalError as Psycopg2OperationalError

# helper function to call command
from django.core.management import call_command

# expecting error when db not ready
from django.db.utils import OperationalError

# testing behaviour if db not ready
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTest(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""
        # mock the behaviour of the connection to the db
        patched_check.return_value = True
        # call the command
        call_command("wait_for_db")
        # check if the check method has been called
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationError"""
        # side_effect allows you to pass different items that get handles differently depending on their type
        # the first 2 times we call the mocked method we want to raise the Psycopg2OperationalError
        # then raise 3 operational errors
        # return the True on the 6th try
        patched_check.side_effect = (
            [Psycopg2OperationalError] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
