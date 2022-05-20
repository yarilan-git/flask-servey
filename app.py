from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.secret_key = '123'


@app.route('/')
def show_servey():
    """Show the survey's home page and request user input"""

    session['responses'] = []
    global next_q
    global num

    next_q = 0
    num = 0

    return render_template('survey.html', title=satisfaction_survey.title, 
    name=satisfaction_survey.title,
    instructions=satisfaction_survey.instructions)


@app.route('/questions/<int:num>')
def question(num=0):
    """Show one question at a time, with its answer options. Do not allow a manual redirection 
       to a quesion that is out of order"""
    if num != next_q:
        flash("Changing the order of the questions is not allowed!")
        return redirect(f"/questions/{next_q}")
    else:        
        title_text = f"Question {num+1}"
        return render_template('questions.html', question= satisfaction_survey.questions[num].question, choices=satisfaction_survey.questions[num].choices)

@app.route('/answer', methods=['post'])
def answer ():
    """Load the user's answers into the responses list. After the last question, thank the user."""
    
    global next_q

    if request.form.get('choices'):
        i = int(request.form['choices'])
        response_list = session['responses']
        response_list.append(satisfaction_survey.questions[next_q].choices[i])    
        session['responses'] = response_list
        next_q += 1
        if len(satisfaction_survey.questions) == next_q:
            target = "/thank-you"
        else:
            target = f"/questions/{next_q}"
        
        return redirect(target)  
    else:
        flash("Please select an option below!")
        return render_template('questions.html', question= satisfaction_survey.questions[num].question, choices=satisfaction_survey.questions[num].choices)

@app.route('/thank-you')  
def thanks():
    """Thank the user for participating in the survey"""

    return render_template('thank-you.html')
