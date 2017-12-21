import repo_data
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('Git_Hub_Data_Site.html')


@app.route('/top_contributor')
def top_contributor():
    return repo_data.top_contributors()[0]


@app.route('/most_popular_problems')
def most_popular_problem():
    return repo_data.most_popular_problems()[9]


@app.route('/num_solutions')
def num_solutions():
    return len(repo_data.count_all_solutions())


@app.route('/most_average_user')
def most_average_user():
    return repo_data.most_average_user()