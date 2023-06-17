def pytest_collection_modifyitems(config, items):  # pylint: disable=unused-argument
    """Ensure all tests are marked with one of the
    defined markers
    """
    marks = {"unit", "perft"}

    unclassified_tests = set()
    overclassified_tests = set()

    for item in items:
        found = set(item.keywords) & marks
        if not found:
            unclassified_tests.add(item.name)
        elif len(found) > 1:
            overclassified_tests.add(item.name)

    if unclassified_tests or overclassified_tests:
        raise ValueError(
            "Found the following misclassified tests: "
            f"{unclassified_tests | overclassified_tests}"
        )
