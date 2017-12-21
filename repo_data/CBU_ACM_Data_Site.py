import repo_data
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def main_page():
    # renders a template for the main page
    return render_template('Git_Hub_Data_Site.html',
                           top_contributor=top_contributor(),
                           most_popular_problem=most_popular_problem(),
                           num_solutions=num_solutions(),
                           most_average_user=most_average_user(),
                           num_contributors=num_contributors())


def top_contributor():
    # returns the top contributor
    return repo_data.top_contributors()[0]


def most_popular_problem():
    # returns the most popular problem
    return repo_data.most_popular_problems()[0]


def num_solutions():
    # returns the number of solutions
    return repo_data.count_all_solutions()


def most_average_user():
    # returns the most average user
    return repo_data.most_average_user()


def num_contributors():
    # returns the number of contributors
    return len(repo_data.get_contributors())
