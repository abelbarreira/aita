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

## Design

```plaintext

filters = parse_prompt(input prompt)
query_dates_list = generate_query_dates_list(filters)

output_results_combined = []

for each startDate and endDate in query_dates_list:
  query_flights = build_query_flight(startDate, endDate, filters)
  query_hotels = build_query_hotel(startDate, endDate, filters)

  result_flights = search_flights(query_flights)
  results_hotels = search_hotels(query_hotels)

  results_combined = result_flights + results_hotels

  output_results_combined += get_best_results_combined(results_combined, number_of_best_per_date)

print output_results_combined
```

To be continued...
