import sys
import builtins
import pytest
from aita import main as aita_main


def test_main_version(mocker, capsys):
    # Simulate running with --version argument
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=type("Args", (), {"version": True, "prompt": None}),
    )
    mocker.patch("aita.main.get_version", return_value="1.2.3")

    aita_main.main()
    captured = capsys.readouterr()
    assert "AitA Version: 1.2.3" in captured.out


def test_main_missing_prompt(mocker, capsys):
    # Simulate running without --version and no --prompt
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=type("Args", (), {"version": False, "prompt": None}),
    )
    mock_exit = mocker.patch("builtins.exit", side_effect=SystemExit)

    with pytest.raises(SystemExit):
        aita_main.main()

    captured = capsys.readouterr()
    assert "Error: --prompt is required" in captured.out


def test_main_missing_env_keys(mocker, capsys):
    args = type("Args", (), {"version": False, "prompt": "Find flights to Paris"})
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)
    mocker.patch("aita.main.load_dotenv")

    env_values = {
        "CURRENCY": None,
        "FLIGHT_API_BASE_URL": "url",
        "FLIGHT_API_KEY": None,
        "HOTEL_API_BASE_URL": "url",
        "HOTEL_API_KEY": None,
    }

    def getenv_side_effect(key):
        return env_values.get(key)

    mocker.patch("os.getenv", side_effect=getenv_side_effect)
    mock_exit = mocker.patch("builtins.exit", side_effect=SystemExit)

    with pytest.raises(SystemExit):
        aita_main.main()

    captured = capsys.readouterr()
    assert "Missing keys in .env file:" in captured.out
    assert "CURRENCY" in captured.out
    assert "FLIGHT_API_KEY" in captured.out
    assert "HOTEL_API_KEY" in captured.out


def test_main_successful_flow(mocker, capsys):
    args = type("Args", (), {"version": False, "prompt": "Find flights to Paris"})
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)
    mocker.patch("aita.main.load_dotenv")
    mocker.patch("os.getenv", side_effect=lambda key: "https://valid.url")

    # Mock Filters.from_prompt to return a Filters object with known values
    from aita.core.filters import Filters

    filters_instance = Filters(
        origin="Berlin",
        destination="Paris",
        start_date="5 January",
        duration_min=3,
        duration_max=3,
        flexibility=0,
    )
    mocker.patch("aita.core.filters.Filters.from_prompt", return_value=filters_instance)

    # Mock generate_query_dates to return a known dict
    from datetime import datetime
    from aita.core.query_dates import QueryDates

    query_dates_dict = {
        0: QueryDates(start_date=datetime(2025, 1, 5), end_date=datetime(2025, 1, 8))
    }
    mocker.patch(
        "aita.core.query_dates.generate_query_dates", return_value=query_dates_dict
    )

    # Mock pretty_print_query_dates to just print a known string
    mocker.patch(
        "aita.core.query_dates.pretty_print_query_dates",
        side_effect=lambda qd: print("ID 0: Start = 2025-01-05, End = 2025-01-08"),
    )

    # Mock Filters.pretty_print to print a known string
    mocker.patch.object(
        Filters,
        "pretty_print",
        side_effect=lambda: print(
            "origin: Berlin\ndestination: Paris\nstart_date: 5 January\nduration_min: 3\nduration_max: 3\nflexibility: 0"
        ),
    )

    aita_main.main()
    captured = capsys.readouterr()

    assert "All required .env keys are present" in captured.out
    assert "Parsed Filters:" in captured.out
    assert "origin: Berlin" in captured.out
    assert "destination: Paris" in captured.out
    assert "Query Dates:" in captured.out
    assert "ID 0: Start = 2025-01-05, End = 2025-01-08" in captured.out
