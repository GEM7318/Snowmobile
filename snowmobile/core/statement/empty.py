from contextlib import contextmanager

from IPython.core.display import Markdown, display
from snowflake.connector.errors import ProgrammingError

from snowmobile.core.connector import Connector
from snowmobile.core.statement.statement import Statement


class Empty(Statement):
    """QA class for results expected to be empty."""

    _note: str = """
**Note**: This will only return results if the test has failed.
"""

    def __init__(self, sn: Connector, **kwargs):
        super().__init__(sn=sn, **kwargs)

    def process(self):
        self._outcome = self.results.empty
        return self
