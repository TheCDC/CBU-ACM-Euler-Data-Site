import repo_data
import os
import sqlite3
import re
from flask import Flask, render_template, g, request, redirect, url_for

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data_site.db'),
    SECRET_KEY='development key',
))



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
    # creates a solutions table
    with app.open_resource('schemas/SolutionsSchema.sql', mode='r') as f:
        database.cursor().executescript(f.read())

    # fills with initial data
    create_contributors()
    create_problems()
    # commits
    database.commit()


@app.cli.command('init_database')
def init_database_command():
    repo_data.setup()
    init_database()
    print('Database initialized')


@app.cli.command('update_database')
def update_user():
    """ a method to update the current database for any new contributors or problems"""
    # runs a scan of the current stats
    repo_data.setup()
    # gets database
    database = get_database()
    # creates contributors and problems
    create_contributors()
    create_problems()

    database.commit()
    print('Database updated')


@app.teardown_appcontext
def close_db(error):
    """closes the database at the end of the request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def create_contributors():
    """method to add all current contributors to the database"""
    # loops through contributors, creating contributor objects
    for contributor in repo_data.top_contributors():
        # creates a new contributor and adds it on
        add_contributor(contributor)


def add_contributor(contributor):
    """helper method to add contributors"""
    # gets the database and selects all users
    database = get_database()
    cur = database.cursor()
    cur.execute('SELECT username FROM Contributors')
    contributor_list = [row[0] for row in cur.fetchall()]

    # tries to create a new contributor of name user
    try:
        contributor_info = get_contributor_info(contributor)
    except NameError:
        return

    # if the contributor is not already in the database creates a new record
    if contributor not in contributor_list:

        # adds contributor info to database
        database.execute('INSERT INTO Contributors (username, rank, number_solved) '
                         'VALUES (?, ?, ?)', contributor_info[0: 3])

        for problem in contributor_info[3]:
            database.execute('INSERT INTO Solutions ( problem_number, username) '
                             'VALUES (?, ?)', (problem[problem.index(' '):], contributor_info[0]))
    # else it updates the contributor info
    else:
        database.execute('UPDATE Contributors SET rank = ?, number_solved = ? WHERE username = ?',
                         (contributor_info[1], contributor_info[2], contributor_info[0]))
        # gets a list of all the problems the user has solved
        cur.execute('SELECT problem_number FROM Solutions WHERE username = ?', (contributor_info[0],))
        problems_list = [row[0] for row in cur.fetchall()]
        # loops through every solution adding it to the list
        for problem in contributor_info[3]:
            # if contributor does not already have a solution adds it
            if int(problem[problem.index(' '):]) not in problems_list:
                cur.execute('INSERT INTO Solutions (problem_number, username) Values(?, ?)',
                            (problem[problem.index(' '):], contributor_info[0]))


def get_contributor_info(contributor):
    """Helper method that gets contributor info"""
    if contributor not in repo_data.get_contributors():
        raise NameError('Contributor does not exist')

    problems_solved = repo_data.problems_solved_by(contributor)

    # the contributor info
    return [contributor, repo_data.get_contributor_rank(contributor),
            len(problems_solved), problems_solved]


def create_problems():
    """method to add all current problems to the database"""
    # loops through problems creating Problems
    for problem in repo_data.get_problems():
        # creates a new problem and adds it to the list
        add_problems(problem)


def add_problems(number):
    """helper method to add problems"""
    # gets the database and selects all users
    database = get_database()
    cur = database.execute('SELECT problem_number FROM Problems')
    problems_list = [repo_data.leftpad(str(row[0]), '0', 3) for row in cur.fetchall()]

    # tries to create a new contributor of name user
    try:
        problem_info = get_problem_info(number)
    except NameError:
        return

    # if the user is not already in the database creates a new record
    if number not in problems_list:

        # adds problem information to database
        database.execute('INSERT INTO Problems (problem_number, popularity, times_solved) '
                         'VALUES (?, ?, ?)', problem_info)
    else:
        database.execute('UPDATE Problems SET popularity = ?, times_solved = ? WHERE problem_number = ?',
                         (problem_info[1], problem_info[2], problem_info[0]))


def get_problem_info(problem):
    """Helper method that gets problem info"""
    if problem not in repo_data.get_problems():
        raise NameError('Problem does not exist')

    contributors_solved = repo_data.who_solved(problem)

    return [problem, repo_data.get_problem_popularity(problem), len(contributors_solved)]


@app.route('/', methods=['POST', 'GET'])
def main_page():
    database = get_database()
    error = None
    stats = [repo_data.top_contributors()[0], repo_data.most_popular_problems()[0], repo_data.count_all_solutions(),
             repo_data.most_average_user(), len(repo_data.get_contributors()), repo_data.most_common_language()]

    if request.method == 'POST':

        if request.form['problem']:
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
                    error = request.form['problem'] + ' is an invalid problem'
            else:
                error = request.form['problem'] + ' is an invalid problem'
        else:
            # checks if user in database
            cur = database.execute('SELECT * FROM Contributors WHERE username = ?', (request.form['username'],))
            if cur.fetchall():
                return redirect(url_for('search_username', username=request.form['username']))
            else:
                error = request.form['username'] + ' is an invalid user \n *Capitalization matters!'

    # renders a template for the main page
    return render_template('Git_Hub_Data_Site.html',
                           stats=stats,
                           error=error,)


@app.route('/contributors/<order>')
def contributors(order):
    """renders contributors_list template providing all rows in contributor data"""
    database = get_database()
    if order == 'rank':
        cur = database.execute('SELECT * FROM Contributors ORDER BY rank')
    elif order == 'username':
        cur = database.execute('SELECT * FROM Contributors ORDER BY username ')
    else:
        cur = database.execute('SELECT * FROM Contributors ORDER BY number_solved')
    return render_template('Contributors_List.html',
                           contributors=cur.fetchall())



@app.route('/problems/<order>')
def problems(order):
    """renders problem list, providing every row in table problems"""
    database = get_database()
    if order == 'problem_number':
        cur = database.execute('SELECT * FROM Problems ORDER BY problem_number')
    elif order == 'popularity':
        cur = database.execute('SELECT * FROM Problems ORDER BY popularity')
    else:
        cur = database.execute('SELECT * FROM Problems ORDER BY times_solved')
    return render_template('Problem_List.html',
                           problems=cur.fetchall())


@app.route('/search_username/<username>')
def search_username(username):
    """renders Search_User template using given user data"""
    database = get_database()
    cur = database.cursor()
    # gets the problems solved
    cur.execute('SELECT problem_number FROM Solutions WHERE username = ?', (username,))
    problems_solved = cur.fetchall()
    # gets everything else
    cur.execute('SELECT * FROM Contributors WHERE username = ?', (username,))

    return render_template('Search_User.html',
                           contributor=cur.fetchone(),
                           problems_solved=problems_solved)


@app.route('/search_problem/<problem>')
def search_problem(problem):
    """renders searc_problem template using given data"""
    database = get_database()
    cur = database.cursor()
    # gets who solved
    cur.execute('SELECT username FROM Solutions WHERE problem_number = ?', (problem,))
    who_solved = cur.fetchall()
    # gets everything else
    cur.execute('SELECT problem_number, popularity, times_solved FROM Problems WHERE problem_number = ?',
                (int(problem),))
    return render_template('Search_Problem.html',
                           problem=cur.fetchone(),
                           who_solved=who_solved)
