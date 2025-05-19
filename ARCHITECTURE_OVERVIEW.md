# Network Automation – SSH Config Collector

## Overview

A CLI tool to retrieve and archive running configurations from a list of network devices over SSH.

## Purpose

- Automate device configuration backup
- Store raw, unaltered `.cfg` files
- Support audit trails, compliance checks, and disaster recovery

---

## Architecture Diagram

```plaintext
         +------------------------+
         |      Cron Job         |
         |  (runs every Monday)  |
         +----------+------------+
                    |
                    v
          +---------------------+
          |    CLI Entrypoint   |
          |  (argparse parser)  |
          +----------+----------+
                     |
                     v
          +---------------------+
          | SSH Collector Logic |
          | (loop over devices) |
          +----+-----------+----+
               |           |
       +-------+       +---+------------+
       |                    |           |
+------+-----+    +----------------+    |
| SSH Utils  |    | File Writer    |    |
| (paramiko) |    | (.cfg files)   |    |
+------------+    +----------------+    |
                                     |
                         +-----------+---------+
                         | Logger Utils        |
                         | Logs to file + CLI  |
                         +---------------------+
```

---

## Modules

| Layer    | Module                     | Responsibility                        |
|----------|----------------------------|----------------------------------------|
| CLI      | `cli/main.py`              | Parses arguments, calls service logic |
| Service  | `services/ssh_collector.py`| Orchestrates the collection flow      |
| Utility  | `utils/ssh_utils.py`       | Handles SSH connections (paramiko)    |
| Utility  | `utils/file_utils.py`      | Saves configs as `.cfg` files         |
| Utility  | `utils/logger_utils.py`    | Logs to console and file              |
| Config   | `config/config.py`         | Loads YAML + dotenv config            |
| Model    | `models/device_model.py`   | Defines the device schema             |

---

## Configuration and Secrets

- Secrets (e.g., SSH_USERNAME, SSH_PASSWORD) are loaded via `.env`
- Main app config is in `config/settings.yaml`
- All configs are schema-validated using Pydantic
- No secrets are hardcoded or logged

---

## Testing Strategy

- `pytest`, `pytest-mock`, `mypy` used for test and type coverage
- SSH sessions, file I/O, and device input are fully mocked
- Mirror structure under `tests/` ensures maintainability
- `conftest.py` used for reusable fixtures
- CI pipeline runs tests and linters on every push and PR

---

## CI/CD and Linting

- GitHub Actions `.github/workflows/test.yml` runs:
  - `pytest` with coverage
  - `ruff`, `black`, `isort`, and `mypy` for static checks
- `pre-commit` ensures consistent style before commits

---

## Deployment

- Dockerfile included for containerized usage
- Makefile includes `docker-run` and local CLI targets
- CRON-ready or CI-executable (GitHub Actions, Jenkins, etc.)

---

## Observability

- Logs to both terminal and rotating file via `logger_utils`
- Logs include: hostname, job start/end, connection status, errors

---

## Sample Output

```
configs/
├── router1_20250518.cfg
├── router2_20250518.cfg
```

---

## Sample CRON Job

```cron
0 0 * * 1 /path/to/python /app/scripts/run_ssh_backup.py --devices-file /app/config/devices.yaml
```
