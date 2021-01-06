"""Tests for snowmobile.utils.parsing."""
import pytest


def setup_schema_parsing_test():
    """Sets up values and IDs for test of parsing.p()"""
    # (input_to_test, tuple[expected_schema, expected_name])
    input_to_expected_output = [
        ("object", ("", "object")),
        (" object ", ("", "object")),
        ("schema.object", ("schema", "object")),
        ("__schema", ("schema", "")),
        (None, ("", "")),
    ]
    ids = [
        f"in='{i[0]}', out=('{i[1][0]}', '{i[1][1]}')" for i in input_to_expected_output
    ]
    return ids, input_to_expected_output


ids, test_cases = setup_schema_parsing_test()


@pytest.mark.parsing
@pytest.mark.parametrize("names", test_cases, ids=ids)
def test_parsing_schema_and_name_from_generic_nm(names):
    """Test parsing.p() produces expected as_df given a nm (str)."""
    from snowmobile.core.utils.parsing import p

    nm, output_expected = names
    output_under_test = p(nm=nm)
    assert output_under_test == output_expected
