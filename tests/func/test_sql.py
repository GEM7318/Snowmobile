"""Unit tests for snowmobile.SQL."""
import pytest

from pydantic import Field
from typing import Dict, Any

from tests import (
    CONFIG_FILE_NM,
    CREDS,
    BaseTest,
    idfn,
)
from .fixtures import path, script

from snowmobile.core import Configuration

INPUT_JSON = 'mod_sql_unit_input.json'
VALIDATION_SQL = 'mod_sql_unit_validation.sql'


# noinspection PyProtectedMember
class SQLUnit(BaseTest):
    """Base object for all unit tests against the methods of :class:`SQL`.
    """

    # -- START: ATTRIBUTES FOR A SPECIFIC TEST INSTANCE -----------------------
    base: Any = Field(
        description='An instantiated instance of the SQL class.',
    )
    base_attrs: Dict = Field(
        description='A dictionary of attributes to set on the SQL instance before running test.',
    )
    method: str = Field(
        description="The literal name of the method under test.",
        alias="method",
    )
    method_args: Dict = Field(
        description="A dict of keyword arguments to path to the method under test.",
        alias="method_kwargs",
    )
    value_returned: str = Field(
        description="The value returned by the method under test.",
        default_factory=str,
    )
    value_expected: str = Field(
        description="The value to validate the returned value against."
    )
    value_expected_id: int = Field(
        description="The integer ID within VALIDATION_SQL of the validation statement."
    )
    # -- END: ATTRIBUTES FOR A SPECIFIC TEST INSTANCE -------------------------

    cfg: Configuration = Field(
        description="snowmobile.Configuration object for use of static methods."
    )

    # noinspection PyProtectedMember
    def __init__(self, **data):
        super().__init__(**data)

        # set the state on the SQL class for this test
        self.base = \
            self.cfg.batch_set_attrs(obj=self.base, attrs=self.base_attrs)

        # get the method as a callable from its namespace
        method_to_run = self.cfg.methods_from_obj(obj=self.base)[self.method]

        # call the method with the specified arguments and store results
        self.value_returned = method_to_run(**self.method_args)

    def __repr__(self) -> str:
        """Full __repr__ string to reproduce the object under test."""
        init_args = (
            ', '.join(f"{k}='{v}'" for k, v in self.base_attrs.items())
            if self.base_attrs else ''
        )
        method_args = (
            ', '.join(f"{k}='{v}'" for k, v in self.method_args.items())
            if self.method_args else ''
        )
        return f"sql({init_args}).{self.method}({method_args})  # {self.value_expected_id}"

    class Config:
        arbitrary_types_allowed = True


# noinspection PyProtectedMember
def setup_for_sql_module_unit_tests():
    """Set up parameter and parameter IDs for sql module unit tests."""
    import json
    import snowmobile

    # importing test inputs from .json and validation for outputs from .sql
    try:
        with open(path(file_nm=INPUT_JSON), 'r') as r:
            statement_test_cases_as_dict = {
                int(k): v for k, v in json.load(r).items()
            }

        statements_to_validate_against: Dict[int, snowmobile.Statement] = (
            script(script_name=VALIDATION_SQL).statements
        )
    except (IOError, TypeError) as e:
        raise e

    # only run tests for ids (int) that exist in input and validation
    shared_unit_test_ids = set(statements_to_validate_against).intersection(
        set(statement_test_cases_as_dict)
    )

    # instantiate a connector object, connection omitted
    sn = snowmobile.Connect(
        creds=CREDS,
        config_file_nm=CONFIG_FILE_NM,
        delay=True
    )
    sn.sql.auto_run = False

    for test_idx in shared_unit_test_ids:

        str_of_sql_to_validate_test_with = statements_to_validate_against[test_idx].sql
        arguments_to_instantiate_test_case_with = statement_test_cases_as_dict[test_idx]

        yield SQLUnit(
            base=sn.sql._reset(),
            cfg=sn.cfg,
            value_expected=str_of_sql_to_validate_test_with,
            value_expected_id=test_idx,
            **arguments_to_instantiate_test_case_with
        )


@pytest.mark.sql
@pytest.mark.parametrize(
    "sql_unit_test",
    setup_for_sql_module_unit_tests(),
    ids=idfn
)
def test_parsing_is_as_expected(sql_unit_test):
    # TODO: Refactor this such that the stripping isn't necessary
    from snowmobile.core.utils.parsing import strip

    value_under_test, value_expected = [
        strip(
            test,
            trailing=True,
            whitespace=True,
            blanks=True
        )
        for test in [
            sql_unit_test.value_returned,
            sql_unit_test.value_expected
        ]
    ]

    assert value_under_test == value_expected


@pytest.mark.sql
def test_defaults(sn_delayed):
    """Test default values on an instance of :class:`SQL`."""
    # arrange
    from snowmobile.core.sql import SQL
    sql = SQL(sn=sn_delayed)
    attrs_expected = {
        'sn': sn_delayed,
        'nm': str(),
        'schema': sn_delayed.cfg.connection.current.schema_name,
        'obj': 'table',
        'auto_run': True,
    }
    attrs_under_test = {
        k: vars(sql)[k]
        for k, v in attrs_expected.items()
    }
    for attr_nm, attr_value in attrs_under_test.items():
        assert attr_value == attrs_expected[attr_nm]
