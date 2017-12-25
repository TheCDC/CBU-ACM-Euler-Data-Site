import repo_data
import os
from repo_data import Objects
import sqlite3
from flask import Flask, render_template,g

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data_site.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('DATA_SITE_SETTINGS', silent=True)


def connect_database():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def get_database():
    """creates a new connection to the database"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_database()
    return g.sqlite_db


def init_database():
    database = get_database()
    with app.open_resource('schema.sql', mode='r') as f:
        database.cursor().executescript(f.read())
    database.commit()
    create_contributors()


@app.cli.command('init_database')
def init_database_command():
    init_database()
    print('Database initialized')


@app.teardown_appcontext
def close_db(error):
    """closes the database at the end of the request"""
    database = getattr(g, 'sqlite_db', None)


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
    # loops through contributors, creating contributor objects
    for contributor in repo_data.top_contributors():
        # creates a new contributor and adds it on
        add_contributor(contributor)


def add_contributor(user):
    # gets the database and selects all users
    database = get_database()
    cur = database.execute('SELECT username FROM Contributors')

    # if the user is not already in the database creates a new record
    if user.username not in cur.fetchall():
        # tries to create a new contributor of name user
        try:
            contributor = Objects.Contributor(user)
        except NameError:
            return

        cur = database.execute('INSERT INTO Contributors (username, rank, number_solved) VALUES (?, ?, ?)',
                               contributor.username, contributor.get_rank(), len(contributor.get_problems()))


@app.route('/Contributors_List')
def contributors():
    database = get_database()
    return render_template('Contributors_List.html',
                           contributors=database.execute('SELECT * FROM Contributors ORDER BY rank DESC').fetchall())


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



