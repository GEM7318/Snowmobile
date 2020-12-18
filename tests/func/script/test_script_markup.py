"""
This file stores setup and tests for snowmobile.Markup.

See `context.md` within `/tests/func/data/sql` for more information on the
directory structure/approach to this part of the testing.
"""
import pytest

from tests.func.fixtures import (
    get_script,
    get_validation_file,
    contents_are_identical
)


# noinspection PyProtectedMember
def _export_all_markup_test_cases():
    """Exports a set of .sql and .md files for comparison to a validation set.

    ..note:
        *   This method instantiates several script objects and exports
            different mutations of that object to the local file system.
        *   It returns a list of the paths that were exported which is passed
            to :meth:`get_validation_file()` to retrieve the path to the file
            it is supposed to be validated against.
        *   The pair of paths is then passed to :meth:`contents_are_identical()`,
            the return value of which (bool) is used for the assertion under test.

    ..warning:
        *   In the body of the below method, a private attribute of each
            statement within the script is modified.
        *   The modification made is adding the `execution_time_txt` to
            a list of attributes that will be excluded from any exports; this
            is done so that small changes in the execution time across test
            runs not cause failures due to the test set not matching the
            validation set.

    The data structures below mirror those that the validation instances were
    created with - context on their contents are as follows:

        script_dtl (List[Tuple[str, bool, Dict]]):
            A list of tuples containing:
                1.  The script name from
                        *   From which a path is found/script object is created
                2.  A boolean indicator of whether or not to run the script
                        *   This is based on whether or not the script object
                            from which the validation files were exported was
                            run prior to exporting or not.
                3.  A dictionary of kwargs for script.run()
                        *   To be provided in instances when (2) is `True` in
                            order for the script to reach the intended state
                            while running; this most often contains a single
                            argument `silence_qa=True` so assertion errors
                            won't be raised when intentional failures are hit.
        args (List[Dict]):
            A list of dictionaries containing:
                1.  A set of kwargs for markup.config()
                        *   Most often alternate file prefixes.
                2.  A set of kwargs from markup.export()
                        *   Most often `markdown_only=True` or `sql_only=True`.

    """
    # (1)
    script_dtl = [
        ('markup_no_results.sql', False, {}),
        ('markup_with_results.sql', True, {'silence_qa': True}),
        ('markup_template_anchor.sql', False, {})
    ]
    # (2)
    args = [
        {
            'config': {'alt_file_prefix': '(default) '},
            'export': {}
        },
        {
            'config': {'alt_file_prefix': '(no sql) '},
            'export': {'md_only': True}
        },
        {
            'config': {'incl_markers': False, 'alt_file_prefix': '(no markers) '},
            'export': {}
        },
        {
            'config': {
                'incl_markers': False,
                'sql_incl_export_disclaimer': False,
                'alt_file_prefix': '(no disclaimer, no markers) ',
            },
            'export': {'sql_only': True}
        },
    ]
    try:
        export_dtl = []
        for s in script_dtl:
            script_nm, run, run_kwargs = s
            script = get_script(script_name=script_nm)

            if run:
                script.run(**run_kwargs)
                for i, st in script.executed.items():
                    st._exclude_attrs.append('execution_time_txt')

            for arg in args:
                doc = script.doc().config(**arg['config'])
                doc.export(**arg['export'])

                for p in doc.exported:
                    if p.exists():
                        export_dtl.append(
                            {'path': p, 'args': arg}
                        )

        return export_dtl
    except Exception as e:
        raise e


def _setup_for_markup_test_cases():
    """Exports test cases, locates validation paths, generates IDs."""
    # export test cases
    export_dtl = _export_all_markup_test_cases()
    # list of tuples containing (test path, validation path)
    test_cases = [
        (a['path'], get_validation_file(a['path']))
        for a in export_dtl
    ]
    # list of strings for pytest IDs
    ids = [
        f"File='{a['path'].name}', Args={a['args']}"
        for a in export_dtl
    ]

    return ids, test_cases


ids, test_cases = _setup_for_markup_test_cases()


@pytest.mark.markup
@pytest.mark.parametrize(
    "markups", test_cases, ids=ids
)
def test_markup_exports(markups):
    """Testing primary functionality of markup/export functionality."""
    path_to_test_export, path_to_validation_export = markups
    assert contents_are_identical(
        path1=path_to_test_export,
        path2=path_to_validation_export
    )
