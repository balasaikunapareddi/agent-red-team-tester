from agent_red_team_tester.catalog import CATALOG, CATEGORIES, by_category


def test_all_categories_present():
    grouped = by_category()
    assert set(grouped) == set(CATEGORIES)
    for category, cases in grouped.items():
        assert len(cases) >= 2, f"{category} needs at least 2 cases"


def test_case_ids_unique():
    ids = [c.id for c in CATALOG]
    assert len(ids) == len(set(ids))


def test_every_case_has_markers_and_holding():
    for case in CATALOG:
        assert case.payload.strip()
        assert case.holding.strip()
        assert case.forbidden_markers, f"{case.id} has no forbidden markers"


def test_catalog_size():
    assert len(CATALOG) == 14
