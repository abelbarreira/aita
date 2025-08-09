# 🔧 Project Structure

```yaml
AitA/
├── .github
│   ├── workflows
│   │   ├── .gitkeep
│   │   └── aita_test_ci.yml
│   ├── CODE_OF_CONDUCT.md
│   └── CONTRIBUTING.md
├── .vscode
│   ├── settings.json
│   └── tasks.json
├── docs
│   ├── api_usage.md
│   ├── architecture.md
│   ├── example_prompts.md
│   ├── filters.md
│   ├── project_structure.md
│   ├── setup.md
│   └── SUMMARY.md
├── scripts
│   ├── doc_generate_project_structure.py
│   ├── generate_vscode_settings.py
│   ├── generate_vscode_settings.sh
│   ├── run_app.sh
│   ├── run_tests.sh
│   └── setup_python.sh
├── src
│   └── aita
│       ├── api
│       │   ├── flights_api.py
│       │   └── hotels_api.py
│       ├── core
│       │   ├── combo_engine.py
│       │   ├── prompt_parser.py
│       │   └── query_builder.py
│       ├── web
│       │   └── server.py
│       ├── main.py
│       ├── version.py
│       └── __init__.py
├── test
│   ├── applicable_tests.json
│   ├── conftest.py
│   ├── test_combo_engine.py
│   ├── test_flights_api.py
│   ├── test_hotels_api.py
│   ├── test_main.py
│   ├── test_prompt_parser.json
│   ├── test_prompt_parser.py
│   ├── test_query_builder.py
│   └── __init__.py
├── tools
│   └── vscode
│       └── aita.code-profile
├── .editorconfig
├── .env
├── .env.example
├── .gitattributes
├── .gitignore
├── .python-version
├── aita.code-workspace
├── LICENSE
├── pyproject.toml
├── README.md
└── ROADMAP.md
```
