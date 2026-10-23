---
name: data-structures
description: Choose the right data structure in code, in the database and in caches, covering arrays and lists, hash maps and sets, deques and queues, heaps and priority queues, trees and sorted maps, tries, graphs, ring buffers, LRU caches, bloom filters and bitsets, each language's built-ins (Python, TypeScript, Go, Dart), Postgres index types (B-tree, GIN, GiST, BRIN, partial, covering), and Redis structures (sorted sets, streams, HyperLogLog). Use whenever deciding how to store or index data, a lookup or membership check is slow, modeling queues, leaderboards, schedules, hierarchies, graphs or caches, choosing a Postgres index or Redis type, or when someone asks which data structure to use.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [engineering, data-structures, performance, fundamentals]
---

# Data structures

Pick the structure by the **operations you do most** (lookup, insert,
ordered iteration, min/max, range query, membership), then use the
language's built-in or the database's index for it. Hand-rolled structures
are rarely needed.

## 1. Choose by operation

| You mostly need… | Use | Cost |
|---|---|---|
| Index access, append, iterate in order | Array / list / slice | O(1) access, O(1) amortized append |
| Lookup by key, counting, grouping | Hash map | O(1) average |
| "Have I seen this?" / dedupe | Hash set | O(1) average |
| Add/remove at both ends (BFS, sliding window, job buffer) | Deque | O(1) |
| FIFO work queue | Queue (deque or a real queue service across processes) | O(1) |
| Repeatedly take the min/max (scheduling, top-k, Dijkstra) | Heap / priority queue | O(log n) push/pop |
| Keys kept sorted, range queries, floor/ceiling | Balanced tree / sorted map, or a sorted list + binary search | O(log n) |
| Prefix lookup (autocomplete, routing) | Trie | O(key length) |
| Relationships (follows, dependencies, routes) | Graph: adjacency lists (map of id → neighbours) | O(V + E) traversal |
| Last N events, fixed memory | Ring buffer | O(1) |
| Bounded cache with eviction | LRU (hash map + linked list / ordered map) | O(1) |
| Huge "probably contains" with tiny memory | Bloom filter | O(k), false positives only |
| Dense flags over small integer IDs | Bitset | O(1), 1 bit per item |
| Hierarchies (categories, org charts) | Parent pointers + recursive query, or materialized path / closure table in SQL | depends on reads vs writes |

## 2. Built-ins per language

| Need | Python | TypeScript | Go | Dart |
|---|---|---|---|---|
| List | `list` | `Array` | slice | `List` |
| Map / set | `dict` / `set` | `Map` / `Set` | `map[K]V` / `map[K]struct{}` | `Map` / `Set` |
| Deque / queue | `collections.deque` | (index-based or small lib) | slice/channel, `container/list` | `Queue` (`ListQueue`) |
| Heap | `heapq` | (small lib) | `container/heap` | `PriorityQueue` (`package:collection`) |
| Sorted | `bisect` on a list; `sortedcontainers` | sorted array + binary search | `slices.BinarySearch` | `SplayTreeMap` |
| Counter / default | `Counter`, `defaultdict` | `Map` + `?? 0` | `map[K]int` | `update(..., ifAbsent:)` |
| Immutable record | `@dataclass(frozen=True)`, `NamedTuple` | `readonly` types | struct values | `freezed` / `final` fields |

Language gotchas: plain JS objects as maps (prototype keys, string-only
keys) → use `Map`. Go maps aren't safe for concurrent writes → mutex or
`sync.Map`. Python mutable default args and mutating while iterating.

## 3. In the database (Postgres)

| Access pattern | Index |
|---|---|
| Equality, range, sort, prefix `LIKE 'abc%'` | **B-tree** (default) |
| JSONB containment, arrays, full-text search | **GIN** |
| Geo, ranges, nearest-neighbour, exclusion constraints | **GiST** |
| Huge append-only time-series filtered by time | **BRIN** |
| Queries on a subset (`WHERE status = 'pending'`) | **Partial** index |
| Index-only scans for frequent queries | **Covering** (`INCLUDE (...)`) |
| Case-insensitive or computed lookups | **Expression** index (`lower(email)`) |
| Multi-column filters | Composite B-tree; leading column must be in the filter |

Model with tables first; use `jsonb` for genuinely variable attributes, not
to avoid schema design (`postgres`).

## 4. In the cache (Redis or similar)

| Need | Redis type |
|---|---|
| Cached object/JSON, counters, locks with expiry | String (+ `INCR`, `SET NX PX`) |
| Object fields updated independently | Hash |
| Leaderboards, rate-limit sliding windows, delayed jobs by time | **Sorted set** |
| Simple queues | List (or Streams for consumer groups) |
| Event log with consumer groups | Stream |
| Unique visitors at scale (approximate) | HyperLogLog |
| Daily active flags per user ID | Bitmap |

Always set TTLs on cache keys; the database stays the source of truth.

## 5. Pitfalls

- A list where a set/map belongs (membership checks in loops; see
  `algorithms-complexity`).
- Building a custom tree/graph/cache when the DB, a library or Redis
  already provides it.
- Storing derived data without a plan to keep it consistent (cache
  invalidation, denormalized counters).
- Unbounded in-memory structures in long-running servers (memory leaks).
  Bound them or evict.

See `algorithms-complexity/references/complexity-cheatsheet.md` for
per-operation costs.
