# 🧠 Architecture Overview

This document explains how AitA is structured and how components interact.

## System Flow

```plaintext
[ User Prompt ]
     ↓
[ NLP Parser (Langchain / OpenAI) ]
     ↓
[ Query Builder ]
     ↓
[ Flight API ] ←→ [ Cache / DB ]
[ Hotel API ]  ←→ [ Cache / DB ]
     ↓
[ Pricing Logic Engine (Combo + Price Grid Builder) ]
     ↓
[ Output Formatter (HTML / UI / JSON) ]
```
