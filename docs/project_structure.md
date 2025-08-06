# 🔧 Project Structure

```yaml
AitA/
│
├── src/
│ ├── __init__.py
│ ├── main.py # Entry point for CLI
│ ├── version.py # Versioning module
│ ├── cli.py # Future CLI argument parsing
│ ├── core/
│ │ ├── prompt_parser.py # Natural-language prompt parsing
│ │ ├── query_builder.py # Translate filters to API queries
│ │ └── combo_engine.py # Combine flight + hotel options
│ ├── api/
│ │ ├── flights_api.py # Flight API integration
│ │ └── hotels_api.py # Hotel API integration
│ └── web/
│ └── server.py # Placeholder for web backend (Flask/FastAPI)
│
├── test/ # Unit tests
│
├── tools/ # Tools
│
├── scripts/ # Run and test bash scripts
│
├── docs/ # Project documentation
│
├── .github/
│
├── .vscode/ # VS Code workspace and config
│
├── .env.example
├── .gitignore # Ignore compiled and secret files
├── .python-version
├── aita.code-workspace # Workspace config
├── LICENSE # MIT License
├── pyproject.toml
├── README.md
└── ROADMAP.md
```
