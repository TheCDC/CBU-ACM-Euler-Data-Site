from git import Repo
import os

TARGET_DIR = os.path.join(os.path.expanduser('~'), 'cbu_csse_euler')


def setup():
    # clone the euler repository into the user's home directory
    Repo.clone_from(
        "https://github.com/TheCDC/cbu_csse_euler.git", TARGET_DIR)


def language_of_file(filename):
    """Return the name of the Programming language
    in which filename was written."""
    pass


def count_all_solutions():
    """Return the total number of solutions across the entire repo.
    """
    pass


def who_solved(problem_number):
    """Return a list of the names of users who have solved problem_number."""
    pass


def which_solved():
    """Return a list of the numbers of problems that have
    at least one solution."""
    pass


def is_solved(problem_number):
    """Return a boolean indicating whether a problem has been solved."""
    return bool(who_solved(problem_number))


def problems_solved_by(username):
    """Return a list of the numbers of the problems solved by username."""
    pass


def most_popular_problems():
    """Return a list of numbers of problems in descending order of 
    popularity."""
    pass


def top_contributors():
    """Return a list of user in descending order of
    number of problems solved."""
    pass


def find_solution_files(problem_number, username):
    """Return a list of the locations of all files for the solutions of
    problem_number by username."""
    pass


def most_average_user():
    """Return the username of the user whose numer of problems solved
    is closest to the average."""
    pass


def main():
    print(TARGET_DIR)
    # print(language_of_file.__doc__)


if __name__ == '__main__':
    main()
