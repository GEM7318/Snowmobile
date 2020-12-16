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

    def _run(self):
        self.start()
        self.results = self.sn.query(self.sql, results=True)
        self.outcome = self.results.empty
        self.has_run = True

    def run(self, **kwargs):
        if self:
            try:
                self._run()

            except ProgrammingError as e:
                self.set_outcome(success=False)
                print(f"Error {e.errno} ({e.sqlstate}): " f"{e.msg} (" f"{e.sfqid})")

            finally:
                self.end()
                self.set_outcome(success=self.outcome)

        else:
            self.set_outcome()

        if kwargs.get("render"):
            self.render()

        silence = kwargs.get("silence_qa")
        if self and not silence:
            assert self._outcome, f"'{self.tag}' did not pass its QA check."

        return self

    def summary(self):
        return self.results.head()
