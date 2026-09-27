# Research instructions

Read the [fixed question](campaigns/split-proper-star-colouring/question.md), [prior state](campaigns/split-proper-star-colouring/state.md) and [preparation notes](campaigns/split-proper-star-colouring/work/preparation.md). The fixed [test corpus](campaigns/split-proper-star-colouring/work/cases.json) and [verifier](campaigns/split-proper-star-colouring/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/split-proper-star-colouring/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
