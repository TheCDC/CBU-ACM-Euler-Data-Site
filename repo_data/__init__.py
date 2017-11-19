from git import Repo
import os
import shutil

TARGET_DIR = os.path.join(os.path.expanduser('~'), 'cbu_csse_euler')


def leftpad(s, c, l):
    return c * (l - len(s)) + s


def readonly_handler(func, path, execinfo):
    """Function to ensure the correct user owns the file
    we're trying to delete."""
    os.chmod(path, 128)  # or os.chmod(path, stat.S_IWRITE) from "stat" module
    func(path)


def setup():
    # clone the euler repository into the user's home directory
    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR, onerror=readonly_handler)
    Repo.clone_from(
        "https://github.com/TheCDC/cbu_csse_euler.git", TARGET_DIR)


def language_of_file(filename):
    """Return the name of the Programming language
    in which filename was written."""
    # list of all file extensions of assumed used languages
    file_ext_map = {".c": "C", ".cpp": "C++", ".cs": "C#", ".java": "Java", ".m": "MatLab",
                    ".py": "Python", ".rb": "Ruby"}
    # gets the file extension type
    filename_ext = filename[filename.index(".", 0, len(filename)):]
    # returns the file type
    return file_ext_map.get(filename_ext)


def which_solved():
    """Return a list of the numbers of problems that have
    at least one solution."""
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
    try:
        files_list = os.listdir(problem_directory)
    except FileNotFoundError:
        # the problem might not have any solutions
        return []
    # a place the put our output
    folders = []
    # loop over all the found files/directories
    for f in files_list:
        # construct the absolute path of each
        final_directory = os.path.join(problem_directory, f)
        # check whether its a file or folder
        if os.path.isdir(final_directory):
            # if it is, append it to our output
            folders.append(f)
    return folders


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


def get_contributors():
    """Return a list of all the users that have contributed to the project thus far"""
    # todo find a way to manage the same contributor with different names
    # set of users to prevent repeats
    contributors = set()
    # adds all the users who a have completed a problem
    for problem in get_problems():
        # for every problem adds the users who have solved it
        for contributor in who_solved(problem):
            contributors.add(contributor)
    return contributors


def get_problems():
    """Helper function that returns a list of all the problems"""
    # gets a list of all the problems
    files_list = os.listdir(TARGET_DIR)
    # list to be returned
    problems = []
    # loops through adding problems
    for problem in files_list:
        # checks if the file contains a problem number to add
        if "_" in problem and problem[problem.index("_") + 1:]:
            problems.append(problem[problem.index("_") + 1:])
    return problems


def main():
    setup()
    print(TARGET_DIR)
    print(who_solved(1))
    # print(language_of_file.__doc__)


if __name__ == '__main__':
    main()
