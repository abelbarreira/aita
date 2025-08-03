"""
Main entry point for AitA - AI Travel Assistant
"""

from app.core.prompt_parser import parse_prompt

def main():
    prompt = input("Enter your travel request prompt:\n")
    filters = parse_prompt(prompt)
    print("\nParsed Filters:")
    for key, value in filters.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
