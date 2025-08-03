# 🧳 AitA - AI Travel Assistant

[![Python](https://img.shields.io/badge/python-3.10-yellow)](https://www.python.org/downloads/release/python-31012/)
![License](https://img.shields.io/github/license/abelbarreira/CppProjectTemplate)
[![Pull Requests Welcome](https://img.shields.io/badge/pull%20requests-welcome-brightgreen.svg)](https://github.com/python/typeshed/blob/main/CONTRIBUTING.md)

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

# 🔧 Project Structure

[Project Structure](docs/project_structure.md)

## 🧠 Example Prompts

[Example Prompts](docs/example_prompts.md)

---

## 🚀 Quick Start

### 🐍 Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 📦 Install Requirements

```bash
pip install -r requirements.txt
```

### 🧪 Run CLI Prompt Parser

```bash
make run
```

### ✅ Run Tests

```bash
make test
```

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
