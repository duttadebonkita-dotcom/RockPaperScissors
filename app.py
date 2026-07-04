from random import choice

from flask import Flask, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = "rock-paper-scissors-session-key"

CHOICES = ("Rock", "Paper", "Scissors")
WINNING_MOVES = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper",
}


def get_scoreboard():
    """Create or return the scoreboard for the current browser session."""
    if "scoreboard" not in session:
        session["scoreboard"] = {"wins": 0, "losses": 0, "draws": 0}
    return session["scoreboard"]


@app.route("/")
def home():
    return render_template("index.html", scoreboard=get_scoreboard())


@app.route("/play", methods=["POST"])
def play():
    player_choice = request.form.get("choice")

    if player_choice not in CHOICES:
        return redirect(url_for("home"))

    computer_choice = choice(CHOICES)
    scoreboard = get_scoreboard()

    if player_choice == computer_choice:
        result = "Draw"
        result_message = "It's a Draw!"
        scoreboard["draws"] += 1
    elif WINNING_MOVES[player_choice] == computer_choice:
        result = "Win"
        result_message = "You Win!"
        scoreboard["wins"] += 1
    else:
        result = "Lose"
        result_message = "You Lose!"
        scoreboard["losses"] += 1

    session["scoreboard"] = scoreboard
    session.modified = True

    return render_template(
        "index.html",
        scoreboard=scoreboard,
        player_choice=player_choice,
        computer_choice=computer_choice,
        result=result,
        result_message=result_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
