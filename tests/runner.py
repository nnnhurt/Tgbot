"""Module for runner."""
from types import MethodType
from typing import Any

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner


def prepare_db(self):
    """
    Prepare the database.

    Connects to the database and creates the 'django_db'
    schema if it does not exist.

    Args:
        self: The instance of the class.
    """
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS django_db;')


class PostgresSchemaRunner(DiscoverRunner):
    """Custom test runner for PostgreSQL databases."""

    def setup_databases(
        self,
        **kwargs: Any,
    ) -> list[tuple[BaseDatabaseWrapper, str, bool]]:
        """
        Set up databases for testing.

        Overrides the default method to prepare the database before setting up.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            list[tuple[BaseDatabaseWrapper, str, bool]]:
            A list of tuples containing
            database wrapper, name, and a boolean indicating
            if it's a test database.

        """
        for conn_name in connections:
            connection = connections[conn_name]
            connection.prepare_database = MethodType(prepare_db, connection)
        return super().setup_databases(**kwargs)
