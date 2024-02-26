import pytest
from py21.cli import cli_main


def test_cli(monkeypatch):
    # test general gameplay
    responses = {
        "What's your bankroll? ": "100",
        "Play again? (y/n) ": "n",
        "What would you like to do? ": "s",
        "How much would you like to wager? ": "10",
        "Dealer shows an Ace. Do you want insurance? (y/n) ": "n",
    }
    # test bankroll input
    responses["What's your bankroll? "] = "-100"
    monkeypatch.setattr("builtins.input", InputResponse(responses))
    with pytest.raises(ValueError):
        cli_main(testing=True)
    responses["What's your bankroll? "] = "abc"
    monkeypatch.setattr("builtins.input", InputResponse(responses))
    with pytest.raises(ValueError):
        cli_main(testing=True)
    responses["What's your bankroll? "] = "100"
    monkeypatch.setattr("builtins.input", InputResponse(responses))
    cli_main(testing=True)
    # test all other inputs except splitting
    for i in ["h", "s", "d", "r"]:
        responses["What would you like to do? "] = "r"
        monkeypatch.setattr("builtins.input", InputResponse(responses))
        cli_main(testing=True)


class InputResponse:
    def __init__(self, responses: dict):
        self.responses = responses
        self.prompts_received = []
        self.counter = 0

    def __call__(self, prompt: str) -> str:
        self.prompts_received.append(prompt)
        self.counter += 1
        return self.responses[prompt]
