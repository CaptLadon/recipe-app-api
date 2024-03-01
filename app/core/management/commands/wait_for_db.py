""" Django command to wait for database to be available """

import time

from psycopg2 import OperationalError as Psycopg2OperationalError

# error that django throws if db not ready
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        """entry point for command"""
        # log message to screen
        self.stdout.write("Waiting for db...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OperationalError, OperationalError):
                self.stdout.write("DB unavailable, waiting...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("DB available."))
