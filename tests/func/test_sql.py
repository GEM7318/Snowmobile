"""Unit tests for snowmobile.SQL."""
import pytest
import re

from pydantic import BaseModel, Extra, Field
from typing import Dict, Callable, Any

from tests import (
    CONFIG_FILE_NM,
    CREDS,
)
from .fixtures import path, script

# -- file names
INPUT_JSON = 'mod_sql_unit_input.json'
VALIDATION_SQL = 'mod_sql_unit_validation.sql'


class SQLMethodTester(BaseModel):
    """Base object for all unit tests against the methods of :class:`SQL`.
    """
    instantiated_class_containing_method_to_be_tested: Any = Field(default=None)
    literal_name_of_class_for_namespace_parsing_purposes: str = Field(default=None)
    attrs_to_set_on_the_class_before_running_test: Dict = Field(default_factory=dict)
    name_of_method_under_test: str = Field(default=None)
    method_under_test: Callable = Field(default=None)
    kwargs_for_method_under_test: Dict = Field(default_factory=dict)
    return_value_from_test_method_actual: str = Field(default_factory=str)
    return_value_from_test_method_expected: str = Field(default_factory=str)

    def __init__(self, **data):
        super().__init__(**data)
        if self.instantiated_class_containing_method_to_be_tested:
            self.__post__init()

    # noinspection PyProtectedMember
    def __post__init(self):
        self.instantiated_class_containing_method_to_be_tested._reset()

        self.batch_set_attrs(
            obj=self.instantiated_class_containing_method_to_be_tested,
            attrs=self.attrs_to_set_on_the_class_before_running_test,
        )

        self.method_under_test = self.methods_from_obj(
            obj=self.instantiated_class_containing_method_to_be_tested,
            obj_nm=self.literal_name_of_class_for_namespace_parsing_purposes
        )[self.name_of_method_under_test]

        self.return_value_from_test_method_actual = self.method_under_test(
            **self.kwargs_for_method_under_test
        )

    @staticmethod
    def methods_from_obj(obj, obj_nm: str) -> Dict[str, Callable]:
        callables = [
            getattr(obj, m) for m in dir(obj)
            if isinstance(getattr(obj, m), Callable)
        ]

        pattern = re.compile(f'{obj_nm}\.(\\w+)\\s')
        # pattern = re.compile(re.escape(f'{obj_nm}.(\w+)\s'))
        dict_of_callables = {}
        for c in callables:
            as_str = str(c)
            matches = [m for m in re.finditer(pattern=pattern, string=as_str) if m]
            if matches and not as_str.startswith('__'):
                dict_of_callables[matches[0].group(1)] = c
        return dict_of_callables

    # TODO: Add to configuration
    @staticmethod
    def batch_set_attrs(obj, attrs: dict, to_none: bool = False):
        for k, v in attrs.items():
            if k in vars(obj):
                setattr(obj, k, (None if to_none else v))

    @property
    def id_str(self) -> str:
        nm = self.name_of_method_under_test
        kwargs = self.kwargs_for_method_under_test
        attrs = self.attrs_to_set_on_the_class_before_running_test
        return f"method='{nm}', kwargs={kwargs}, in-state={attrs}"

    def set(
        self,
        base: Any,
        base_name: str,
        attrs: Dict = None,
        method_to_test: str = None,
        with_kwargs: Dict = None,
        expected_return_value: str = None,
    ):
        self.instantiated_class_containing_method_to_be_tested = base
        self.literal_name_of_class_for_namespace_parsing_purposes = base_name
        self.attrs_to_set_on_the_class_before_running_test = attrs
        self.name_of_method_under_test = method_to_test
        self.kwargs_for_method_under_test = with_kwargs
        self.return_value_from_test_method_expected = expected_return_value
        self.__post__init()
        return self

    class Config:
        extra = Extra.allow
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __setattr__(self, key, value):
        vars(self)[key] = value


def setup_for_sql_module_unit_tests():
    import json
    import snowmobile

    sql = snowmobile.SQL(
        sn=snowmobile.Connect(
            creds=CREDS,
            config_file_nm=CONFIG_FILE_NM,
            delay=True
        ),
        auto_run=False,
    )
    script_storing_valid_test_outcomes = script(script_name='mod_sql_unit_validation.sql')
    path_to_test_cases_stored_as_json = path(file_nm='mod_sql_unit_input.json')

    with open(path_to_test_cases_stored_as_json, 'r') as r:
        test_cases_as_dict = json.load(r)

    tests = []
    for arg_idx, args in test_cases_as_dict.items():
        sql_expected = script_storing_valid_test_outcomes.statement(int(arg_idx)).sql
        tests.append(
            SQLMethodTester().set(
                base=sql,
                expected_return_value=sql_expected,
                **args
            )
        )

    test_outcomes_to_expected_outcomes = [
        (
            a.return_value_from_test_method_actual,
            a.return_value_from_test_method_expected
        )
        for a in tests
    ]
    ids = [a.id_str for a in tests]

    return ids, test_outcomes_to_expected_outcomes


test_ids, list_of_test_outcomes_to_expected_outcomes = setup_for_sql_module_unit_tests()


@pytest.mark.sql
@pytest.mark.parametrize(
    "tests", list_of_test_outcomes_to_expected_outcomes, ids=test_ids
)
def test_parsing_is_as_expected(tests):
    from snowmobile.core.utils.parsing import strip
    value_under_test, value_expected = [
        strip(
            test,
            trailing=True,
            whitespace=True,
            blanks=True
        )
        for test in tests
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
