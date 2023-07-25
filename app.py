from surveys import satisfaction_survey, personality_quiz

from flask import Flask, request, render_template, redirect, session, flash

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


toolbar = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.route("/")
def home_page():
    return render_template("base.html", satisfaction_survey=satisfaction_survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/complete")
def survey_complete():
    return render_template("complete.html", satisfaction_survey=satisfaction_survey)


@app.route("/questions/<int:num>")
def questions(num):
    responses = session.get(RESPONSES_KEY)
    if responses is None:
        # trying to access question page too soon
        return redirect("/")

    if len(responses) == len(satisfaction_survey.questions):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if len(responses) != num:
        # Trying to access questions out of order.
        flash(f"Invalid question id: {num}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[num]
    return render_template(
        "questions.html",
        satisfaction_survey=satisfaction_survey,
        question=question,
        question_num=num,
    )


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form["answer"]

    # add this response to the session

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(satisfaction_survey.questions):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")
