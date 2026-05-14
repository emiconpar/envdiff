# envdiff

> Utility to compare environment variable sets across `.env` files and running processes.

---

## Installation

```bash
pip install envdiff
```

Or install from source:

```bash
git clone https://github.com/yourname/envdiff.git && cd envdiff && pip install .
```

---

## Usage

Compare two `.env` files:

```bash
envdiff .env.development .env.production
```

Compare a `.env` file against the current running environment:

```bash
envdiff .env --process
```

Compare environment variables of two running processes by PID:

```bash
envdiff --pid 1234 --pid 5678
```

### Example Output

```
KEY              .env.development    .env.production
───────────────────────────────────────────────────
DATABASE_URL     ✔ set               ✔ set (differs)
DEBUG            ✔ set               ✗ missing
SECRET_KEY       ✗ missing           ✔ set
```

Use `--json` to output results as JSON, or `--only-missing` to filter the diff to missing keys only.

---

## Options

| Flag             | Description                              |
|------------------|------------------------------------------|
| `--process`      | Compare file against current environment |
| `--pid`          | Compare against a running process by PID |
| `--only-missing` | Show only keys absent in one or more sources |
| `--json`         | Output diff as JSON                      |

---

## License

MIT © [yourname](https://github.com/yourname)