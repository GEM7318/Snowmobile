"""Unit tests for snowmobile.SQL."""
import pytest
from typing import Dict, Any

from pydantic import Field

from tests import CONFIG_FILE_NM, CREDS, FILES, BaseTest, idfn, script

from snowmobile.core import Configuration

from tests.unit import INPUT_JSON, VALIDATION_SQL


class SQLUnit(BaseTest):
    """Represents a unit test instance for a method of :class:`snowmobile.SQL`.
    """

    base: Any = Field(description="An instantiated instance of the SQL class.")
    base_attrs: Dict = Field(
        description="A dictionary of attributes to set on the SQL instance before running test."
    )
    method: str = Field(
        description="The literal name of the method under test.", alias="method"
    )
    method_args: Dict = Field(
        description="A dict of keyword arguments to pass to the method under test.",
        alias="method_kwargs",
    )
    value_returned: str = Field(
        description="The actual value returned by the method under test.",
        default_factory=str,
    )
    value_expected: str = Field(
        description="The expected value to be returned by the method under test."
    )
    value_expected_id: int = Field(
        description="The integer ID within VALIDATION_SQL of the expected return value."
    )

    # -- END: ATTRIBUTES FOR TEST INSTANCE ------------------------------------

    cfg: Configuration = Field(
        description="snowmobile.Configuration object for use of static methods."
    )

    # noinspection PyProtectedMember
    def __init__(self, **data):
        """Set remaining attributes with static configuration methods."""
        super().__init__(**data)

        # set the state on the SQL class for this test
        self.base = self.cfg.batch_set_attrs(obj=self.base, attrs=self.base_attrs)

        # get the method as a callable from its namespace
        method_to_run = self.cfg.methods_from_obj(obj=self.base)[self.method]

        # call the method with the specified arguments and store as_df
        self.value_returned = method_to_run(**self.method_args)

    def __repr__(self) -> str:
        """Valid __repr__ to fully reproduce the object under test."""
        init_args = (
            ", ".join(f"{k}='{v}'" for k, v in self.base_attrs.items())
            if self.base_attrs
            else ""
        )
        method_args = (
            ", ".join(f"{k}='{v}'" for k, v in self.method_args.items())
            if self.method_args
            else ""
        )
        return (
            f"sql({init_args}).{self.method}({method_args})  # {self.value_expected_id}"
        )


# noinspection PyProtectedMember
def setup_for_sql_module_unit_tests():
    """Setup for sql module unit tests."""
    import json
    import snowmobile

    try:

        # importing test inputs from .json
        with open(FILES[INPUT_JSON], "r") as r:
            statement_test_cases_as_dict = {int(k): v for k, v in json.load(r).items()}
        # import expected outputs from .sql
        statements_to_validate_against: Dict[int, snowmobile.Statement] = (
            script(script_name=VALIDATION_SQL).statements
        )

    except (IOError, TypeError) as e:
        raise e

    # only run tests for ids (int) that exist in both input and output files
    shared_unit_test_ids = set(statements_to_validate_against).intersection(
        set(statement_test_cases_as_dict)
    )

    # instantiate a connector object, connection omitted
    sn = snowmobile.connect(creds=CREDS, config_file_nm=CONFIG_FILE_NM, delay=True)
    sn.sql.auto_run = False  # turning off so `run=False` is imposed for test

    for test_idx in shared_unit_test_ids:

        # to instantiate test with
        arguments_to_instantiate_test_case_with = statement_test_cases_as_dict[test_idx]

        # required value for test to pass
        str_of_sql_to_validate_test_with = statements_to_validate_against[test_idx].sql

        yield SQLUnit(
            cfg=sn.cfg,
            base=sn.sql._reset(),
            **arguments_to_instantiate_test_case_with,
            value_expected=str_of_sql_to_validate_test_with,
            value_expected_id=test_idx,
        )


@pytest.mark.parametrize("sql_unit_test", setup_for_sql_module_unit_tests(), ids=idfn)
@pytest.mark.sql
def test_sql_module_unit_tests(sql_unit_test):
    # TODO: Refactor this such that the stripping isn't necessary
    from snowmobile.core.utils.parsing import strip

    value_under_test, value_expected = [
        strip(test, trailing=True, whitespace=True, blanks=True)
        for test in [sql_unit_test.value_returned, sql_unit_test.value_expected]
    ]

    assert value_under_test == value_expected


@pytest.mark.sql
def test_defaults(sn_delayed):
    """Test default values on an instance of :class:`SQL`."""
    # arrange
    from snowmobile.core.sql import SQL

    sql = SQL(sn=sn_delayed)
    attrs_expected = {
        "sn": sn_delayed,
        "nm": str(),
        "schema": sn_delayed.cfg.connection.current.schema_name,
        "obj": "table",
        "auto_run": True,
    }
    attrs_under_test = {k: vars(sql)[k] for k, v in attrs_expected.items()}
    for attr_nm, attr_value in attrs_under_test.items():
        assert attr_value == attrs_expected[attr_nm]
