# Sql Analytics Dashboard: process flows

## Domain request

Endpoint: `POST /generate`. Input: question. The processing stages below summarize [sqlgen.py](../src/sqldash/sqlgen.py); they are local function behavior, not externally executed tools.

```mermaid
flowchart TD
  A["POST /generate"] --> B{"Non-empty string question?"}
  B -->|"No"| E["HTTP 422"]
  B -->|"Yes"| C{"Contains forbidden write substring?"}
  C -->|"Yes"| E
  C -->|"No"| D{"First matching template keyword?"}
  D -->|"revenue"| R["Return regional revenue SELECT"]
  D -->|"tickets"| T["Return ticket status count SELECT"]
  D -->|"None"| E
  R --> O["SQL string + read_only true; no execution"]
  T --> O
```

Refusal responses, where implemented, are normal domain results rather than successful execution of a requested write. Detailed edge cases are covered in [INTERVIEW_QA.md](../INTERVIEW_QA.md).

## Workspace and job approval

```mermaid
flowchart TD
  C["Create tenant-scoped workspace"] --> J["Submit job: workspace + payload + target"]
  J --> V{"Workspace belongs to selected tenant?"}
  V -->|"No"| E["HTTP 404"]
  V -->|"Yes"| P{"Target is prod or production?"}
  P -->|"Yes"| Q["pending_approval"]
  P -->|"No"| L["queued"]
  Q --> A["Approval request"]
  A --> X["HTTP 403: production apply disabled"]
  L --> B["Approval request"]
  B --> K["approved: status update only"]
  K --> S["No executor / no production apply"]
```

Approval first checks job ownership using the selected tenant. Status changes and audit records remain in memory. The approval endpoint does not enforce a full transition state machine: repeated lab approval is possible. The domain request flow and this job-record flow are independent. Source: [ops.py](../src/sqldash/ops.py).
