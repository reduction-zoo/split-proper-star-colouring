"""Independent 3-SAT and split-graph star-coloring oracles."""

import argparse
import json
import subprocess
import sys
from itertools import permutations, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target, dict):
        return False
    c, s, k = (target.get(key) for key in ("clique", "independent", "colors"))
    crosses = target.get("cross_edges")
    return (all(type(value) is int and value >= 0 for value in (c, s, k))
            and isinstance(crosses, list)
            and all(isinstance(edge, list) and len(edge) == 2
                    and type(edge[0]) is int and 0 <= edge[0] < c
                    and type(edge[1]) is int and 0 <= edge[1] < s for edge in crosses)
            and len({tuple(edge) for edge in crosses}) == len(crosses))


def graph_edges(target):
    c = target["clique"]
    return [(u, v) for u in range(c) for v in range(u+1, c)] + [
        (u, c+v) for u, v in target["cross_edges"]]


def four_paths(target):
    n = target["clique"] + target["independent"]
    adjacency = [set() for _ in range(n)]
    for u, v in graph_edges(target):
        adjacency[u].add(v)
        adjacency[v].add(u)
    for path in permutations(range(n), 4):
        if path < path[::-1] and all(path[i+1] in adjacency[path[i]] for i in range(3)):
            yield path


def direct_coloring(target, coloring):
    if not legal_target(target) or not isinstance(coloring, list):
        return False
    n, k = target["clique"] + target["independent"], target["colors"]
    return (len(coloring) == n
            and all(type(color) is int and 0 <= color < k for color in coloring)
            and all(coloring[u] != coloring[v] for u, v in graph_edges(target))
            and all(not (coloring[a] == coloring[c] and coloring[b] == coloring[d])
                    for a, b, c, d in four_paths(target)))


def target_solutions(target, limit=3):
    if not legal_target(target):
        raise ValueError("Illegal split-graph coloring instance")
    n, k = target["clique"] + target["independent"], target["colors"]
    colors = [z3.Int(f"color_{i}") for i in range(n)]
    solver = z3.Solver()
    for color in colors:
        solver.add(color >= 0, color < k)
    for u, v in graph_edges(target):
        solver.add(colors[u] != colors[v])
    for a, b, c, d in four_paths(target):
        solver.add(z3.Or(colors[a] != colors[c], colors[b] != colors[d]))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        answer = [model.eval(color).as_long() for color in colors]
        if not direct_coloring(target, answer):
            raise AssertionError("Z3 coloring violates direct predicate")
        outputs.append({"coloring": answer})
        solver.add(z3.Or(*[color != value for color, value in zip(colors, answer)]))
    return outputs or [{"status": "NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target, 1)[0]


def valid_target(target, output):
    if not legal_target(target) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"coloring"} and direct_coloring(target, output["coloring"])


def exhaustive_target(target):
    for coloring in product(range(target["colors"]), repeat=target["clique"]+target["independent"]):
        if direct_coloring(target, list(coloring)):
            return {"coloring": list(coloring)}
    return {"status": "NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable, str(root / "research/validate_preparation.py"), str(path)], check=True, cwd=root)
    cases = json.loads(path.read_text())
    for n, clauses, answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars": n, "clauses": clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                         for clause in source["clauses"])
                     for bits in product((False, True), repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source, current) and valid_source(source, case["expected"])
    assert not valid_source({"num_vars": 1, "clauses": [[1]]}, {"assignment": [False]})
    test_hand_cases()
    checked = 0
    for c in range(4):
        for s in range(3):
            slots = [(u, v) for u in range(c) for v in range(s)]
            for mask in range(1 << len(slots)):
                crosses = [list(edge) for i, edge in enumerate(slots) if mask & (1 << i)]
                for k in range(4):
                    target = {"clique": c, "independent": s, "cross_edges": crosses, "colors": k}
                    assert ("coloring" in solve_target(target)) == ("coloring" in exhaustive_target(target))
                    checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive split-graph thresholds")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable, str(path)], input=json.dumps(source), text=True, capture_output=True, check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal split-graph target: {target}")
        for output in target_solutions(target):
            if not valid_target(target, output):
                raise AssertionError(f"Target oracle returned invalid output: {output}")
            payload = {"source": source, "target_solution": output}
            extraction = subprocess.run([sys.executable, str(path), "--extract"], input=json.dumps(payload), text=True, capture_output=True, check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source, recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
