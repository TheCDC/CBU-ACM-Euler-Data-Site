from git import Repo
import os

TARGET_DIR = os.path.join(os.path.expanduser('~'), 'cbu_csse_euler')


def leftpad(s, c, l):
    return c * (l - len(s)) + s


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
    # construct the name of the folder in which solutions will be found
    problem_filename = 'euler_{}/'.format(leftpad(str(problem_number), '0', 3))
    # locate the folder with name that within the repo
    problem_directory = os.path.join(TARGET_DIR, problem_filename)
    # get the list of files/directories within it
    files_list = os.listdir(problem_directory)
    # a place the put our output
    folders = []
    # loop over all the found files/directories
    for f in files_list:
        # construct the absolute path of each
        final_directory = os.path.join(problem_directory, f)
        # check whether its a file or folder
        if os.path.isdir(final_directory):
            # if it is, append it to our output
            folders.append(final_directory)
    return folders


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
    print(who_solved(1))
    # print(language_of_file.__doc__)


if __name__ == '__main__':
    main()
