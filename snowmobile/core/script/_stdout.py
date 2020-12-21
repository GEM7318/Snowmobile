"""
Console output from :class:`snowmobile.Script` object.
"""
from typing import Dict, Union

from snowmobile.core.statement import statement as statements


class Script:
    def __init__(
        self,
        name: str,
        statements: Dict[int, statements.Statement],
        verbose: bool = True,
    ):
        self.name: str = name
        self.statements = statements
        self.verbose = verbose
        self.max_width_outcome = len("<COMPLETED>")
        self.outputs: Dict[int, str] = {}

    @property
    def cnt_statements(self) -> int:
        return len(self.statements)

    @property
    def max_width_progress(self) -> int:
        return max(
            len(f"<{i} of {self.cnt_statements}>")
            for i, _ in enumerate(self.statements.values(), start=1)
        )

    @property
    def max_width_tag_and_time(self) -> int:
        return max(len(f"{s.tag.nm} (~0s)") for s in self.statements.values())

    def console_progress(self, s: statements.Statement) -> str:
        return f"<{s.index} of {self.cnt_statements}>".rjust(
            self.max_width_progress, " "
        )

    def console_tag_and_time(self, s: statements.Statement) -> str:
        return f"{s.tag.nm} ({s.execution_time_txt})".ljust(
            self.max_width_tag_and_time + 3, "."
        )

    def console_outcome(self, s: statements.Statement) -> str:
        return f"<{s.outcome_txt().lower()}>".ljust(self.max_width_outcome, " ")

    def status(
        self, s: statements.Statement, return_val: bool = False
    ) -> Union[None, str]:
        progress = self.console_progress(s)
        tag_and_time = self.console_tag_and_time(s)
        outcome = self.console_outcome(s)
        stdout = f"{progress} {tag_and_time} {outcome}"
        self.outputs[s.index] = stdout
        if self.verbose:
            print(stdout)
        if return_val:
            return stdout

    def display(self, underline: bool = True):
        name = self.name
        if underline:
            bottom_border = "=" * len(name)
            name = f"{bottom_border}\n{name}\n{bottom_border}"
        if self.verbose:
            print(f"{name}")
