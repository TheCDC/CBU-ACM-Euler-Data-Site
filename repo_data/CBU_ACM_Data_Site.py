import repo_data
import os
from repo_data import Objects
import sqlite3
from flask import Flask, render_template,g
app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'Data_Site.db')


def connect_database():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def get_database():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_database()
    return g.sqlite_db


def init_databse():
    database = get_database()
    with app.open_resource('schema.sql', mode='r') as f:
        database.cursor().executescript(f.read())
    database.commit()



@app.route('/Data_Site')
def main_page():
    # renders a template for the main page
    return render_template('Git_Hub_Data_Site.html',
                           top_contributor=repo_data.top_contributors()[0],
                           most_popular_problem=repo_data.most_popular_problems()[0],
                           num_solutions=repo_data.count_all_solutions(),
                           most_average_user=repo_data.most_average_user(),
                           num_contributors=len(repo_data.get_contributors()),
                           most_common_language=repo_data.most_common_language())


def create_contributors():
    contributors_list = []

    # loops through contributors, creating contributor objects
    for contributor in repo_data.top_contributors():
        # creates a new contributor and adds it on
        contributors_list.append(Objects.Contributor(contributor))

    return contributors_list


def add_contributor():


@app.route('/Contributors_List')
def contributors():
    database = get_database()
    users =
    return render_template('Contributors_List.html',
                           contributors=create_contributors())


def create_problems():
    problems_list = []

    # loops through problems creating Problems
    for problem in repo_data.get_problems():
        # creates a new problem and adds it to the list
        problems_list.append(Objects.Problem(problem))

    return problems_list


@app.route('/Problems_List')
def problems():
    return render_template('Problem_List.html',
                           problems=create_problems())


@app.teardown_appcontext
def close_db(error):
    """closes the database at the end of the request"""
    database = getattr(g, 'sqlite_db', None)
