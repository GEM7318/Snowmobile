"""
`qa-empty` statement object.
"""
from snowmobile.core import Connector
from .statement import Statement


class Empty(Statement):
    """QA class for results expected to be empty."""

    # TODO: Give each QA statement a default error message that can be passed
    #   be passed explicitly as a statement argument.
    _note: str = """
**Note**: This will only return results if the test has failed.
"""

    def __init__(self, sn: Connector, **kwargs):
        super().__init__(sn=sn, **kwargs)

    def process(self):
        self._outcome = self.results.empty
        return self
