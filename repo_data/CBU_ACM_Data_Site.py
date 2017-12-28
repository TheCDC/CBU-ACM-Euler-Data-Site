import repo_data
import os
from repo_data import Objects
import sqlite3
import re
from flask import Flask, render_template, g, request, redirect, url_for

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data_site.db'),
    SECRET_KEY='development key',
))
app.config.from_envvar('DATA_SITE_SETTINGS', silent=True)


def connect_database():
    """establishes a connection to the database"""
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def get_database():
    """creates a new connection to the database"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_database()
    return g.sqlite_db


def init_database():
    """initializes the database with current contributors and problems at time of creation"""
    database = get_database()
    # creates a contributor table
    with app.open_resource('schemas/ContributorsSchema.sql', mode='r') as f:
        database.cursor().executescript(f.read())
    # creates a problem table
    with app.open_resource('schemas/ProblemsSchema.sql', mode='r') as f:
        database.cursor().executescript(f.read())

    # fills with initial data
    create_contributors()
    create_problems()
    # commits
    database.commit()


@app.cli.command('init_database')
def init_database_command():
    init_database()
    print('Database initialized')


def create_problems():
    """method to add all current problems to the database"""
    # loops through problems creating Problems
    for problem in repo_data.get_problems():
        # creates a new problem and adds it to the list
        add_problems(problem)


def create_contributors():
    """method to add all current contributors to the database"""
    # loops through contributors, creating contributor objects
    for contributor in repo_data.top_contributors():
        # creates a new contributor and adds it on
        add_contributor(contributor)


def update():
    """ a method to update the current database for any new contributors or problems"""
    database = get_database()
    create_problems()
    create_contributors()
    database.commit()


@app.teardown_appcontext
def close_db(error):
    """closes the database at the end of the request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['POST', 'GET'])
def main_page():
    database = get_database()
    error = None
    stats = [repo_data.top_contributors()[0], repo_data.most_popular_problems()[0], repo_data.count_all_solutions(),
             repo_data.most_average_user(), len(repo_data.get_contributors()), repo_data.most_common_language()]

    if request.method == 'POST':

        # checks if user in database
        cur = database.execute('SELECT * FROM Contributors WHERE username = ?', (request.form['username'],))
        if cur.fetchall():
            return redirect(url_for('search_username', username=request.form['username']))

        # collects digits inside problem
        digits = re.search('\d', request.form['problem'])
        # checks if digits are in the entry
        if digits:
            # gets substring of just digits
            digits = request.form['problem'][request.form['problem'].index(digits.group(0)):]
            cur = database.execute('SELECT problem_number FROM Problems WHERE problem_number = ?',(int(digits),))
            if cur.fetchall():
                return redirect(url_for('search_problem', problem=int(digits)))
        else:
            # creates an error message for invalid entries
            if request.form['username']:
                error = request.form['username'] + ' is an invalid user \n *Capitalization matters!'
            else:
                error = request.form['problem'] + ' is an invalid problem'

    # renders a template for the main page
    return render_template('Git_Hub_Data_Site.html',
                           stats=stats,
                           error=error,)


def add_contributor(user):
    """helper method to add contributors"""
    # gets the database and selects all users
    database = get_database()
    cur = database.execute('SELECT username FROM Contributors')

    # if the user is not already in the database creates a new record
    if user not in cur.fetchall():
        # tries to create a new contributor of name user
        try:
            contributor = Objects.Contributor(user)
        except NameError:
            return

        # adds contributor info to database
        user_info = [contributor.username, contributor.get_rank(), len(contributor.get_problems()),
                     ', '.join(contributor.get_problems())]
        cur = database.execute('INSERT INTO Contributors (username, rank, number_solved, problems_solved) '
                               'VALUES (?, ?, ?, ?)', user_info)


@app.route('/Contributors_List')
def contributors():
    """renders contributors_list template providing all rows in contributor data"""
    database = get_database()
    return render_template('Contributors_List.html',
                           contributors=database.execute('SELECT * FROM Contributors ORDER BY rank ').fetchall())


def add_problems(number):
    """helper method to add problems"""
    # gets the database and selects all users
    database = get_database()
    cur = database.execute('SELECT problem_number FROM Problems')

    # if the user is not already in the database creates a new record
    if number not in cur.fetchall():
        # tries to create a new contributor of name user
        try:
            problem = Objects.Problem(number)
        except NameError:
            return

        # adds problem information to database
        problem_info = [problem.problem_number, problem.get_popularity(), len(problem.get_who_solved()),
                        ', '.join(problem.get_who_solved())]
        cur = database.execute('INSERT INTO Problems (problem_number, popularity, times_solved, who_solved) '
                               'VALUES (?, ?, ?, ?)', problem_info)


@app.route('/Problems_List')
def problems():
    """renders problem list, providing every row in table problems"""
    database = get_database()
    return render_template('Problem_List.html',
                           problems=database.execute('SELECT * FROM Problems ORDER BY problem_number').fetchall())


@app.route('/search_username/<username>')
def search_username(username):
    """renders Search_User template using given user data"""
    database = get_database()
    cur = database.execute('SELECT * FROM Contributors WHERE username = ?', (username,))
    return render_template('Search_User.html',
                           contributor=cur.fetchone())


@app.route('/search_problem/<problem>')
def search_problem(problem):
    """renders searc_problem template using given data"""
    database = get_database()
    cur = database.execute('SELECT * FROM Problems WHERE problem_number = ?', (problem,))
    return render_template('Search_Problem.html',
                           problem=cur.fetchone())
