import repo_data
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def main_page():
    # renders a template for the main page
    return render_template('Git_Hub_Data_Site.html',
                           top_contributor=repo_data.top_contributors()[0],
                           most_popular_problem=repo_data.most_popular_problems()[0],
                           num_solutions=repo_data.count_all_solutions(),
                           most_average_user=repo_data.most_average_user(),
                           num_contributors=len(repo_data.get_contributors()))



