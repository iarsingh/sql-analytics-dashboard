# Sql Analytics Dashboard: interview questions and answers

Answers describe this repository's current implementation. Suggested production changes are explicitly labeled as future work.

## 1. Does this service execute SQL?

No. `generate` returns one of two constant SELECT strings with `read_only: true`. There is no database connection, query execution, result table, or dashboard UI in the current implementation.

Source: [src/sqldash/sqlgen.py](src/sqldash/sqlgen.py).

## 2. How is a revenue question mapped?

A question containing `revenue` returns `SELECT region, SUM(revenue) FROM orders GROUP BY region`. A question containing `tickets` returns the status count query. Matching is case-insensitive and uses complete tokens.

Source: [src/sqldash/sqlgen.py](src/sqldash/sqlgen.py).

## 3. What if both mapping keywords occur?

The request is rejected as ambiguous with HTTP 422. Exactly one recognized keyword must match. `GET /templates` lists the two supported templates.

Source: [src/sqldash/sqlgen.py](src/sqldash/sqlgen.py).

## 4. Which inputs return HTTP 422?

An empty or non-string question, a question containing a forbidden write keyword, or a question with no mapping raises `InputError` and becomes 422 in the handler.

Source: [src/sqldash/sqlgen.py](src/sqldash/sqlgen.py).

## 5. Why can the keyword guard reject a harmless question?

It now checks complete lowercase tokens for `drop`, `delete`, `update`, `insert`, and `alter`, avoiding substring matches such as `altered`. It is still a natural-language guard, not a SQL parser or database permission system.

Source: [src/sqldash/sqlgen.py](src/sqldash/sqlgen.py).

## 6. Is read_only true a database permission?

No. It describes the returned template. There is no connected database. A future executor would need read-only credentials, query validation, limits, and timeouts.

Source: [src/sqldash/sqlgen.py](src/sqldash/sqlgen.py).

## 7. What is the query injection boundary today?

The service does not interpolate user text into SQL: both outputs are constants. If parameters are added, use parameter binding and a controlled template registry instead of string concatenation.

Source: [src/sqldash/sqlgen.py](src/sqldash/sqlgen.py).

## 8. How would you validate the mappings?

The existing test sends `revenue by region` and checks for `SUM(revenue)` and the read-only flag, then verifies a delete question returns 422. Regression tests cover ambiguous requests, complete-token matching, and template discovery.

Source: [src/sqldash/sqlgen.py](src/sqldash/sqlgen.py).

## 9. How are the domain API and ops plane connected?

The app registers the ops router under `/v1`, alongside the domain endpoint. Creating or approving a job updates ops records; it does not call the domain function. There is no background worker or job executor.

Source: [src/sqldash/main.py](src/sqldash/main.py).

## 10. Does X-Tenant-Id authenticate a user?

No. It is a caller-supplied header defaulting to `default`. Workspace and job reads filter by that value, but a caller can choose another value. Real identity and authorization would need to precede this lab tenant selector.

Source: [src/sqldash/ops.py](src/sqldash/ops.py).

## 11. What survives a process restart?

Nothing in the ops dictionaries or audit list is persisted. Multiple server workers would also have separate state. Durable storage, transactions, and a shared job queue are future changes.

Source: [src/sqldash/ops.py](src/sqldash/ops.py).

## 12. What happens when a production job is approved?

Targets are trimmed and normalized to lowercase before policy checks. `prod` and `production`, including case/padding variants, create a `pending_approval` job and approval returns HTTP 403. Repeated lab approval is idempotent; approval changes a record only, without executing a workload.

Source: [src/sqldash/ops.py](src/sqldash/ops.py).

## 13. Are audit and metrics equally tenant-scoped?

Audit results filter events by the tenant and its workspace/job identifiers. `/v1/metrics` returns process-wide counters without tenant filtering, so it is not a tenant-specific dashboard. Domain requests are not automatically audited.

Source: [src/sqldash/ops.py](src/sqldash/ops.py).

## 14. What would you prioritize before a customer deployment?

Define authenticated identities and permission checks, durable state, typed domain inputs, bounded requests, concurrency behavior, and observable execution semantics. Use the existing tests as a baseline, then test failure and access boundaries rather than claiming the lab is production-ready.

Source: [src/sqldash/ops.py](src/sqldash/ops.py).
