# Complexity cheat sheet: built-in operations

Average-case costs of common operations in our languages. `n` = size of the
collection. Verify unusual cases against the language docs; these are the
well-known figures.

## Python

| Operation | Cost | Note |
|---|---|---|
| `list.append`, `list.pop()` | O(1) amortized | |
| `list.insert(0, x)`, `list.pop(0)` | O(n) | use `collections.deque` |
| `x in list`, `list.index`, `list.remove` | O(n) | use a `set`/`dict` for membership |
| `list[i]`, `len(list)` | O(1) | |
| `list.sort()`, `sorted()` | O(n log n) | Timsort, stable |
| slicing `a[i:j]` | O(j − i) | copies |
| `dict`/`set` get, set, `in`, delete | O(1) average | insertion-ordered dicts |
| `deque.appendleft/popleft` | O(1) | |
| `heapq.heappush/heappop` | O(log n) | min-heap |
| `bisect.bisect_left` | O(log n) | insertion `insort` is O(n) |
| `str` concatenation in a loop | O(n²) total | use `"".join(parts)` |

## TypeScript / JavaScript

| Operation | Cost | Note |
|---|---|---|
| `push`, `pop` | O(1) amortized | |
| `shift`, `unshift`, `splice` at start | O(n) | use an index or a deque implementation |
| `includes`, `indexOf`, `find` | O(n) | use `Set`/`Map` |
| `Map`/`Set` get, set, has, delete | O(1) average | insertion-ordered; prefer over plain objects for dynamic keys |
| `sort` | O(n log n) | stable (ES2019+); default sort compares strings, so pass a comparator for numbers |
| spread/`concat`/`slice` | O(n) | copies; spreading in a loop is O(n²) |
| No built-in heap | — | use a small library or a sorted structure |

## Go

| Operation | Cost | Note |
|---|---|---|
| `append` | O(1) amortized | preallocate with `make([]T, 0, n)` when n is known |
| `map` get, set, delete | O(1) average | iteration order is random; not safe for concurrent writes |
| `slices.Contains`, `slices.Index` | O(n) | |
| `slices.Sort`, `sort.Slice` | O(n log n) | `slices.SortStableFunc` for stable sorting |
| `slices.BinarySearch` | O(log n) | |
| `container/heap` Push/Pop | O(log n) | |
| `strings.Builder` writes | O(1) amortized | instead of `+=` in loops |

## Dart

| Operation | Cost | Note |
|---|---|---|
| `List.add`, `removeLast` | O(1) amortized | |
| `List.insert(0, x)`, `removeAt(0)` | O(n) | use `Queue` (`ListQueue`) |
| `List.contains` | O(n) | use `Set` |
| `Map`/`Set` (default `LinkedHashMap`/`LinkedHashSet`) | O(1) average | insertion-ordered |
| `SplayTreeMap` | O(log n) amortized | sorted keys |
| `PriorityQueue` (`package:collection`) | O(log n) | |

## Postgres (with the right index)

| Query shape | Cost |
|---|---|
| Equality/range on B-tree indexed column | O(log n) + rows returned |
| Same without an index | O(n) sequential scan |
| `ORDER BY ... LIMIT k` using an index | ~O(log n + k) |
| `OFFSET n` pagination | O(n) skipped rows; prefer keyset pagination |
| `count(*)` on a large table | O(n) |
