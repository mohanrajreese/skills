---
name: algorithms-complexity
description: Analyze time and space complexity (Big-O, amortized, worst versus average case, recursion depth) and choose efficient algorithms for real product code, covering what input sizes each complexity can handle, hidden quadratic traps, N+1 queries and network round trips, the classic algorithm patterns (hashing, two pointers, sliding window, prefix sums, binary search, sorting and sweep, heaps and top-k, BFS, Dijkstra, topological sort, union-find, dynamic programming, greedy), streaming for memory, ReDoS, and profiling before optimizing. Use whenever someone asks about time or space complexity or Big-O, code is slow or uses too much memory, a loop over large data or a nested loop is being written, choosing an algorithm, optimizing a query or job, or preparing for an algorithms interview.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [engineering, algorithms, performance, fundamentals]
---

# Algorithms and complexity

Complexity analysis tells you **how cost grows with input size**. In
product code the biggest wins usually come from removing accidental
quadratic work and network round trips, not from clever algorithms. And
always measure before optimising (`design-principles`: no premature
optimisation).

## 1. Analyse

- **Time:** count how many times the innermost work runs as a function of
  input size `n` (and other sizes: `m` items, `k` results). Nested loops
  over the same data → `O(n²)`; halving each step → `O(log n)`; sort →
  `O(n log n)`.
- **Space:** extra memory beyond the input: copies, maps, result lists, and
  **recursion depth** (each call frame). Python's default recursion limit is
  ~1000; deep recursion on user-sized data should be iterative.
- **Amortized:** dynamic array append is `O(1)` amortized even though a
  resize is `O(n)`.
- **Which case:** hash lookups are `O(1)` average but can degrade; quicksort
  is `O(n log n)` average, `O(n²)` worst. State which you mean.
- **Constants and I/O dominate at small n:** one DB round trip (~1 ms) costs
  more than millions of in-memory operations.

## 2. What fits (rule of thumb: ~10⁸ simple operations per second)

| n | Feasible complexity |
|---|---|
| ≤ 20 | `O(2ⁿ)`, `O(n!)` only for tiny n |
| ≤ 1,000 | `O(n²)` fine |
| ≤ 100,000 | `O(n log n)`; `O(n²)` = 10¹⁰, too slow |
| ≤ 10,000,000 | `O(n)` / `O(n log n)` in a compiled language; think about memory |
| Bigger / unbounded | Streaming, chunking, the database, or a batch system |

## 3. Hidden quadratic and I/O traps in product code

- `x in list` / `array.includes()` / `slices.Contains` **inside a loop** →
  build a set/map first.
- String concatenation in a loop (Python `+=`, building huge strings): use
  join/builders.
- `list.pop(0)` / `array.shift()` in a loop → use a deque or an index.
- Sorting or copying inside a loop; re-reading the same file or API.
- **N+1 queries:** one query per item in a list (ORM lazy loading, Firestore
  reads in a loop). Use joins / `select_related` / `prefetch_related` /
  `IN (...)` batches / data loaders.
- One HTTP call per item to a third-party API: use batch endpoints,
  concurrency limits and caching.
- **Regex catastrophic backtracking (ReDoS):** nested quantifiers like
  `(a+)+` on user input. Use simpler patterns or a linear-time engine (Go's
  `regexp` (RE2) is linear; RE2 bindings exist for Python/JS).
- Unbounded `SELECT *` / `findAll` into memory → paginate (keyset) or stream.

## 4. Pattern catalogue (pick by problem shape)

| Problem shape | Pattern | Typical cost |
|---|---|---|
| Lookup, dedupe, count, group | Hash map / set | `O(n)` |
| Pairs in sorted data, merge two lists | Two pointers | `O(n)` |
| "Best window" of consecutive items, rate limiting | Sliding window | `O(n)` |
| Range sums, running totals | Prefix sums | `O(n)` build, `O(1)` query |
| Search in sorted data; "smallest X that works" | Binary search (incl. on the answer) | `O(log n)` per query |
| Intervals, schedules, overlaps | Sort + sweep | `O(n log n)` |
| Top-k, k-way merge, scheduling by priority | Heap | `O(n log k)` |
| Shortest path, unweighted / levels | BFS | `O(V + E)` |
| Shortest path, non-negative weights (routes, costs) | Dijkstra with heap | `O((V + E) log V)` |
| Dependencies, build/migration order, cycles | Topological sort | `O(V + E)` |
| Grouping connected items (dedupe accounts) | Union-find | ~`O(α(n))` per op |
| Overlapping sub-problems (pricing combos, diffs) | Dynamic programming | states × transitions |
| Locally optimal choice is provably optimal | Greedy | usually `O(n log n)` |
| Prefix search, autocomplete | Trie (or DB prefix index) | `O(length)` |
| "Probably seen before?" at huge scale | Bloom filter | `O(k)`, no false negatives |

In production, prefer the **standard library and the database** (sorting,
indexes, `GROUP BY`, window functions, full-text search) over hand-rolled
algorithms.

## 5. Memory: stream, don't load

Iterate with generators/iterators/streams (Python generators, Node streams,
Go `bufio.Scanner`, Dart `Stream`), process in chunks (e.g. 1,000 rows), and
write results incrementally. CSV/Excel exports and imports of user data are
the usual offenders.

## 6. Measure

- Profile first: Python `cProfile` / `py-spy`; Node `--cpu-prof`; Go `pprof`;
  Flutter DevTools; Postgres `EXPLAIN (ANALYZE, BUFFERS)` (`postgres`).
- Benchmark the change on realistic sizes (`pytest-benchmark`, `vitest bench`,
  Go `testing.B` with `b.Loop()`), and keep the benchmark if the code is hot.
- State the result: "export of 50k orders: 42 s → 3 s, memory 1.2 GB →
  80 MB".

See `references/complexity-cheatsheet.md` for operation costs of common
built-ins per language.
