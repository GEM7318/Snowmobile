"""Tests for snowmobile.statement.Diff."""
# import pytest
#
#
# # noinspection SqlResolve
# @pytest.fixture()
# def sample_diff_object(sn):
#     """An example statement object for testing."""
#     from snowmobile.core.statement import Diff
#
#     # creating an example table for fixture
#     sn.ex('drop table if exists an_example_table')
#     sn.ex('create temp table an_example_table as select 1 as sample_col')
#
#     # sql for statement object
#     sql = """
# select
#     *
# from an_example_table a;
# """
#
#     return Statement(
#         sn=sn,
#         statement=sn.cfg.script.ensure_sqlparse(sql=sql.strip('\n')),
#         index=1
#     )
