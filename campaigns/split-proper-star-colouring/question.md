# 3-SAT → Proper star colouring on split graphs

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

The target gives a split graph and color budget k. Find a proper coloring with at most k colors in which no four-vertex path is bichromatic, or report NO-SOLUTION.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The restriction asks how much complexity survives when the graph decomposes into a clique and an independent set.

## Difficulty

Clique colors and independent-set constraints must force source choices without admitting alternative color identifications.

## Literature context

Ordinary proper coloring of split graphs is not the same task as excluding bichromatic four-vertex paths under a color budget.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Acyclic, Star and Injective Colouring: A Complexity Picture for H-Free Graphs](https://drops.dagstuhl.de/storage/00lipics/lipics-vol173-esa2020/LIPIcs.ESA.2020.22/LIPIcs.ESA.2020.22.pdf): Bok, Jedlickova, Martin, Paulusma and Smith, Acyclic, Star and Injective Colouring: A Complexity Picture for H-Free Graphs, ESA 2020, Section 6, Open Problem 4, explicitly asks for the complexity on split graphs. The nearby co-bipartite hardness construction does not ensure a split output. Injective colouring hardness also has a different witness predicate. The 2025 journal version retains this question in indexed primary-source text; full retrieval of that URL failed during this check, so its updated proofs were not inspected.
- [2025 journal version](https://durham-repository.worktribe.com/OutputFile/4090739): Bok, Jedlickova, Martin, Paulusma and Smith, Acyclic, Star and Injective Colouring: A Complexity Picture for H-Free Graphs, ESA 2020, Section 6, Open Problem 4, explicitly asks for the complexity on split graphs. The nearby co-bipartite hardness construction does not ensure a split output. Injective colouring hardness also has a different witness predicate. The 2025 journal version retains this question in indexed primary-source text; full retrieval of that URL failed during this check, so its updated proofs were not inspected.
- [Star Coloring on Some Subclasses of Chordal Graphs](https://arxiv.org/html/2606.25168v1): Star Coloring on Some Subclasses of Chordal Graphs, arXiv:2606.25168v1 (June 2026), Section 3, gives structural results and certifying algorithms for four and five colours on split graphs. Proposition 3.1 gives the clique-number bounds; Proposition 3.4 gives sufficient obstructions. These do not classify variable-k split inputs. Its introduction also identifies the remaining general 2K2-free complexity gap.
- [The star and biclique coloring and choosability problems](https://arxiv.org/pdf/1210.7269): A terminology collision matters here. Groshaus, Soulignac and Terlisky, The star and biclique coloring and choosability problems, arXiv:1210.7269v2, abstract and Section 7, study absence of monochromatic maximal induced stars. Their split-graph NP-completeness result is not about proper colouring with no bicoloured four-vertex path.

Fixed from board record `website/questions/split-proper-star-colouring.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
