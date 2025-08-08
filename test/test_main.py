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
    mocker.patch("aita.main.get_version", return_value="1.2.3")  # <--- patch here

    aita_main.main()
    captured = capsys.readouterr()
    assert "AitA Version: 1.2.3" in captured.out


def test_main_missing_prompt(mocker, capsys):
    # Simulate running without --version and no --prompt
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=type("Args", (), {"version": False, "prompt": None}),
    )

    # Patch exit to raise SystemExit so the function stops after printing
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

    # Patch exit to raise SystemExit to stop execution after error message
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

    # Mock os.getenv to return valid keys
    mocker.patch("os.getenv", side_effect=lambda key: "https://valid.url")

    # Mock parse_prompt in the main namespace
    filters = {"destination": "Paris", "dates": "2025-12-20:2025-12-25"}
    mocker.patch("aita.main.parse_prompt", return_value=filters)

    # Mock search_travel_combinations in the main namespace
    flights = [{"flight_id": "FL123", "price": 500}]
    hotels = [{"hotel_id": "HT456", "price_per_night": 150}]
    mocker.patch(
        "aita.main.search_travel_combinations",
        return_value={"flights": flights, "hotels": hotels},
    )

    aita_main.main()
    captured = capsys.readouterr()

    assert "All required .env keys are present" in captured.out
    assert "Parsed Filters:" in captured.out
    assert "destination: Paris" in captured.out
    assert "Flight Results:" in captured.out
    assert "FL123" in captured.out
    assert "Hotel Results:" in captured.out
    assert "HT456" in captured.out
