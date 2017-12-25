import repo_data
from repo_data import Objects
from flask import Flask, render_template
app = Flask(__name__)


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


@app.route('/Contributors_List')
def contributors():
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
