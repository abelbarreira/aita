# 🔧 Project Structure

```yaml
AitA/
│
├── app/
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
├── scripts/ # Run and test bash scripts
│
├── docs/ # Project documentation
│
├── .vscode/ # VS Code workspace and config
│
├── AitA.code-workspace # Workspace config
├── README.md # This file
├── requirements.txt # Runtime dependencies
├── dev-requirements.txt # Development dependencies
├── Makefile # Makefile commands (run, test, lint)
├── CONTRIBUTING.md # How to contribute
├── LICENSE # MIT License
└── .gitignore # Ignore compiled and secret files
```
