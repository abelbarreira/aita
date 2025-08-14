import pytest
from aita import main as aita_main
from aita.core.filters import Filters
from aita.core.query_dates import QueryDates
from datetime import datetime


class TestAitaMain:
    @classmethod
    def setup_class(cls):
        """Runs once for the entire class"""
        cls.original_env = {}  # Store original environment if needed
        # Any heavy setup shared across tests can go here

    @classmethod
    def teardown_class(cls):
        """Runs once after all tests in the class"""
        # Restore any global state if needed
        cls.original_env.clear()

    def setup_method(self, method):
        """Runs before each test method"""
        # Reset mocks or temp variables if necessary
        self.mocks = []

    def teardown_method(self, method):
        """Runs after each test method"""
        # Clean up mocks or other temporary state
        for m in self.mocks:
            m.stop()

    def test_version_output(self, mocker, capsys):
        mocker.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=type("Args", (), {"version": True, "prompt": None}),
        )
        mocker.patch("aita.main.get_version", return_value="1.2.3")

        aita_main.main()
        captured = capsys.readouterr()
        assert "AitA Version: 1.2.3" in captured.out

    def test_missing_prompt(self, mocker, capsys):
        mocker.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=type("Args", (), {"version": False, "prompt": None}),
        )
        mocker.patch("builtins.exit", side_effect=SystemExit)

        with pytest.raises(SystemExit):
            aita_main.main()

        captured = capsys.readouterr()
        assert "Error: --prompt is required" in captured.out

    def test_missing_env_keys(self, mocker, capsys):
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

        mocker.patch("os.getenv", side_effect=lambda key: env_values.get(key))
        mocker.patch("builtins.exit", side_effect=SystemExit)

        with pytest.raises(SystemExit):
            aita_main.main()

        captured = capsys.readouterr()
        assert "Missing keys in .env file:" in captured.out
        assert "CURRENCY" in captured.out
        assert "FLIGHT_API_KEY" in captured.out
        assert "HOTEL_API_KEY" in captured.out

    def test_successful_flow(self, mocker, capsys):
        args = type("Args", (), {"version": False, "prompt": "Find flights to Paris"})
        mocker.patch("argparse.ArgumentParser.parse_args", return_value=args)
        mocker.patch("aita.main.load_dotenv")
        mocker.patch("os.getenv", side_effect=lambda key: "https://valid.url")

        # Mock Filters.from_prompt
        filters_instance = Filters(
            origin="Berlin",
            destination="Paris",
            start_date="5 January",
            duration_min=3,
            duration_max=3,
            flexibility=0,
        )
        mocker.patch(
            "aita.core.filters.Filters.from_prompt", return_value=filters_instance
        )

        # Mock query_dates
        query_dates_dict = {
            0: QueryDates(
                start_date=datetime(2025, 1, 5), end_date=datetime(2025, 1, 8)
            )
        }
        mocker.patch(
            "aita.core.query_dates.generate_query_dates", return_value=query_dates_dict
        )

        # Mock printing methods
        mocker.patch(
            "aita.core.query_dates.pretty_print_query_dates",
            side_effect=lambda qd: print("ID 0: Start = 2025-01-05, End = 2025-01-08"),
        )
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
