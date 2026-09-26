from check import legal_target, solve_target, valid_target


def test_hand_cases():
    triangle = {"clique": 2, "independent": 1, "cross_edges": [[0, 0], [1, 0]], "colors": 2}
    assert solve_target(triangle) == {"status": "NO-SOLUTION"}
    path = {"clique": 2, "independent": 2, "cross_edges": [[0, 0], [1, 1]], "colors": 2}
    assert not valid_target(path, {"coloring": [0, 1, 1, 0]})
    assert valid_target({**path, "colors": 3}, {"coloring": [0, 1, 1, 2]})
    assert not legal_target({"clique": 1, "independent": 0, "cross_edges": [[0, 0]], "colors": 1})


if __name__ == "__main__":
    test_hand_cases()
