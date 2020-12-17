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

    def run(self, **kwargs):

        with self._run(**kwargs) as r:
            r._outcome = r.results.empty

        silence = kwargs.get("silence_qa")
        if self and not silence:
            assert self._outcome, f"'{self.tag}' did not pass its QA check."

        return self

