# Prepared input and output contract

The 3-SAT source input is `{"num_vars": n, "clauses": [[signed_literals],
...]}` with `n >= 0`, at most three literals per clause and each nonzero
literal's absolute value at most `n`. A source output is
`{"assignment": [bool, ...]}` satisfying all clauses, or
`{"status": "NO-SOLUTION"}` exactly when none exists.

The split-graph target input is `{"clique": c, "independent": s,
"cross_edges": [[clique_index, independent_index], ...], "colors": k}`
with nonnegative integers `c`, `s`, `k`, valid endpoint indices, and distinct
cross edges. Clique vertices are `0..c-1`, independent vertices `c..c+s-1`;
all clique edges and only listed cross edges exist. A target output is
`{"coloring": [integer, ...]}` with one color in `0..k-1` per vertex,
proper on every edge, and with no simple four-vertex path using only two
colors. `{"status": "NO-SOLUTION"}` is valid only if no such coloring
exists. The empty graph has a valid empty coloring even when `k=0`.

A candidate `algorithm.py` reads source JSON from stdin and writes legal
target JSON to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors, and send
diagnostics to stderr. They must be deterministic and polynomial time, and
recovery must work for every valid target output.

`check.py --candidate PATH` independently solves the target produced for each
fixed source case and validates the recovered assignment or negative answer.
