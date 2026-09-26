# Preparation evidence

Prepared on 2026-09-26 before constructing a candidate. The fixed corpus has
120 distinct legal 3-SAT formulas: 20 hand-labelled edge cases and 100 seeded
random cases, with 64 SAT and 56 UNSAT decisions, zero to six variables and
zero to ten clauses. `generate_cases.py` records the generator and seeds;
`cases.json` stores expected outputs. Z3 4.16.0's source clauses are exact
Boolean disjunctions. Every model is checked by direct clause evaluation;
UNSAT is conclusive and unknown is an error. Exhaustive Boolean assignment
enumeration agreed with all 120 labels.

The target Z3 oracle has one integer color per vertex, enforces the color
budget and proper edges, and forbids equal colors at opposite positions of
each simple four-vertex path. Under proper coloring, such equalities are
exactly a bichromatic path. Every model is checked again by enumerating graph
edges and paths directly. Exhaustive color enumeration agreed on 416 small
split-graph/color-budget combinations with up to three clique vertices, two
independent vertices and three colors. Hand fixtures include a two-color
triangle obstruction, a bichromatic four-vertex path, an alternate valid
three-coloring and invalid cross edge.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/split-proper-star-colouring/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates seeded formulas,
rechecks labels and source witnesses, and compares target decisions with
exhaustive enumeration. The candidate runner uses separate forward and
recovery subprocesses and up to three target colorings per source. An
incorrect injected candidate was rejected after its target was solved and
its recovered NO-SOLUTION was directly invalidated. No actual reduction
candidate exists; these finite checks do not prove hardness or a reduction.
