# 🧳 AitA - AI Travel Assistant

[![Python](https://img.shields.io/badge/python-3.10-yellow)](https://www.python.org/downloads/release/python-31012/)
![License](https://img.shields.io/github/license/abelbarreira/CppProjectTemplate)
[![Pull Requests Welcome](https://img.shields.io/badge/pull%20requests-welcome-brightgreen.svg)](https://github.com/abelbarreira/aita/blob/main/.github/CONTRIBUTING.md)

**AitA (AI Travel Assistant)** helps users find the best combinations of flights and hotels using natural language prompts and smart filters. Designed to be open-source, modular, and easily extensible, AitA provides a framework for travel planning with integration of free APIs, flexible user input, and intelligent trip evaluations.

---

## ✨ Features (MVP)

- 🔍 Search & combine flights + hotels using **free public/test APIs**
- 🗣️ Parse natural language travel prompts into structured filters
- 🧠 Smart logic for evaluating **best stay durations**
- 📊 Display results in a **price-per-day** grid
- 🗂️ Clear separation of concerns (parsing, query building, APIs, etc.)
- 💬 CLI interface for prototyping and testing
- 🌱 Easily scalable with future enhancements (weather, sea temperature, etc.)

---

## 🔧 Project Structure

[Project Structure](docs/project_structure.md)

## 🧠 Example Prompts

[Example Prompts](docs/example_prompts.md)

---

## 🚀 Quick Start

### 🛠 Setup Python Environment

This project uses `pyenv` to manage Python versions and `pipx` for isolated tool installation.

To quickly set up the correct Python version:

```bash
./scripts/setup_python.sh
```

Use `hatch` commands to manage environments, testing, building, and publishing.

### Run the CLI (without installing)

Direct Python module invocation:

```bash
hatch run python -m aita.main --version
```

Via CLI script (using `[project.scripts]`):

```bash
hatch run aita -- --version
```

Interactive shell:

```bash
hatch shell
aita --version
exit
```

### (Optional) Make CLI available system-wide

If you want to use the CLI everywhere (outside Hatch):

```bash
pip install -e .
aita --version
```

## 🧹 Troubleshooting

- If your CLI script isn't working after changes, prune the Hatch environment:

```bash
hatch env prune
```

### 💡 Useful Commands

| Action                           | Command                             |
|-----------------------------------|-------------------------------------|
| Run CLI (module)                  | `hatch run python -m aita.main ...` |
| Run CLI (script)                  | `hatch run aita -- ...`             |
| Interactive shell                 | `hatch shell`                       |
| Prune env (fix stale env issues)  | `hatch env prune`                   |
| Install editable (system-wide)    | `pip install -e .`                  |

### 🧰 Tech Stack

- Language: Python 3.10+
- APIs: Flights + Hotels from free/test public APIs (e.g. RapidAPI, TravelPayouts)
- CLI: Command-line for prompt parsing & testing
- Web: Placeholder for future Flask/FastAPI server
- Tests: Pytest
- Linting: flake8 + black

## Documentation

Refer to [SUMMARY](docs/SUMMARY.md).

## 🤝 Contributing

If you have suggestions for how Open Source Projects Template could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

For more, check out the [Contributing Guide](.github/CONTRIBUTING.md).

## 🛡️ License

MIT License

Copyright (c) 2025 abelbarreira

For more, check out the [License File](LICENSE).

## 🤖 AI-Powered Collaboration

This project is being developed with support and guidance from [ChatGPT](https://chatgpt.com/) and [GitHub Copilot](https://github.com/copilot).

Collaboration started in August 2025.
