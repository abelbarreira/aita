# ToDo

✅ Current Status Summary
Your project includes:

Core project structure (app/, test/, docs/, scripts/, tools/)

Dev tooling (.vscode/, Makefile, requirements.txt, dev-requirements.txt)

Early implementation

Likely includes: main.py, prompt_parser, .env.example, etc.

Documentation started: README.md, ROADMAP.md

You're organized and well-positioned to build out functionality quickly.

🔜 Next Steps (Short-Term — MVP Completion)

1. 🔍 Finalize Prompt Parsing Logic
✅ prompt_parser.py exists

➕ Add GPT-based alternative in ai_parser.py

➕ Option in CLI to choose between regex and GPT parser

2. ✈️ Stub External APIs

Create flights_api.py and hotels_api.py

Use dummy/free API or mock response JSONs

Support filters like time windows, distance from beach, stars, etc.

1. 🔗 Implement Combo Engine
In combo_engine.py (or core/combo_engine.py)

Combine flight + hotel results

Sort and score by total cost, proximity, duration, etc.

4. 🧪 Write Tests
Use pytest in test/

Test:

Prompt parsing (regex + GPT)

API module stubs

Combo logic (using mock data)

Add test data in test/data/

5. 📦 Improve CLI Interface
Allow running main.py with:

bash
Copy
Edit
python app/main.py --prompt "..." --parser ai
6. 🔧 .env Integration
Use python-dotenv in main.py

Store API keys and config in .env (use .env.example as template)

7. ⚙️ CI/CD
Setup GitHub Actions from .github/workflows/

Python tests

Linting

Optionally: Zip & upload to S3 or GitHub Releases for testing

🛣️ Mid-Term Roadmap (After MVP)
🔮 LLM Enhancements
Refine GPT parsing with structured output (json_mode=True)

Option to fine-tune or prompt-chain for:

Best trip analysis

Cost vs. convenience decisions

🗺️ UX Enhancements
Output HTML report or simple web UI (use Flask or FastAPI)

Add plotting for price-per-day (use Plotly or Matplotlib)

📈 Learning Model
Track past results

Refine scoring algorithm based on user preferences (basic reinforcement)

🔧 Would You Like Me To Generate?
ai_parser.py with GPT integration?

flights_api.py and hotels_api.py stubs?

combo_engine.py scaffold?

test/test_prompt_parser.py and mocks?

Let me know which parts you want generated or reviewed next
