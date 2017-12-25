from git import Repo
import os
import shutil
import math
import operator

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
    try:
        filename_ext = filename[filename.index(".", 0, len(filename)):]
    except ValueError:
        return ""
    # returns the file type
    return file_ext_map.get(filename_ext)


def most_common_language():
    # list of all the languages used and the number of times they have been used
    file_ext_map = {"C": 0, "C++": 0, "C#": 0, "Java": 0, "MatLab": 0,
                    "Python": 0, "Ruby": 0}

    # loops through problems checking the languages used for each problem
    for problem in get_problems():
        problem_dir = os.path.join(TARGET_DIR, 'Euler_{}'.format(leftpad(str(problem), '0', 3)))
        # tries to access the list of solutions by problem number
        try:
            files_list = os.listdir(problem_dir)
            # loops through the files incrementing each languages every time its been used
            for file in files_list:
                # gets the file path
                for solution in find_solution_files(problem, file):
                    # language of file
                    language = language_of_file(solution)
                    # checks that the language is is the file_ext_map
                    if language in file_ext_map.keys():
                        file_ext_map[language] += 1
        except FileNotFoundError:
            continue

    # returns max language
    return max(file_ext_map.items(), key=operator.itemgetter(1))[0]


def which_solved():
    """Return a list of the numbers of problems that have
    at least one solution."""
    # list to hold solved problems
    num_solved = []
    # loops through every problem checking if it has a solution
    for problem in get_problems():
        # if it has a solution it is added
        if is_solved(problem):
            num_solved.append('Euler {}'.format(leftpad(str(problem), '0', 3)))
    return num_solved


def count_all_solutions():
    """Return the total number of solutions across the entire repo.
    """
    # the number of solutions
    num_solutions = 0
    # loops through every problem adding the number of solutions it has
    for problem in get_problems():
        num_solutions += len(who_solved(problem))
    return num_solutions


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
    # list of the problems solved by user
    solved = []
    # checks every problem
    for problem in get_problems():
        # if the user has solved problem, problem is added to solved
        if username in who_solved(problem):
            solved.append('Euler {}'.format(leftpad(str(problem), '0', 3)))
    return solved


def most_popular_problems():
    """Return a list of numbers of problems in descending order of 
    popularity."""
    # list of all the problems
    problems = get_problems()
    # sorts based on number of solutions
    problems.sort(key=compare_problems)
    problems = ["Euler " + problem for problem in problems]
    return problems


def compare_problems(p1):
    """A compare function, made to compare problems by the number of solutions"""
    return -len(who_solved(p1))


def top_contributors():
    """Return a list of user in descending order of
    number of problems solved."""
    # Set of all the users casted to a list
    contributors = list(get_contributors())
    # Sorts the list based on number of solutions
    contributors.sort(key=compare_users)
    return contributors


def compare_users(username):
    """A compare function, made to compare user by num solved"""
    return -len(problems_solved_by(username))


def find_solution_files(problem_number, username):
    """Return a list of the locations of all files for the solutions of
    problem_number by username."""
    # list of the location of the user's solution for said problem
    problems = []
    # the folder directory of the problem
    problem_filename = os.path.join(TARGET_DIR, 'euler_{}/'.format(leftpad(str(problem_number), '0', 3)))
    # tries to retrieve a list of all folders in the directory
    try:
        user_filename = os.path.join(problem_filename, username)
        files_list = os.listdir(user_filename)
    except (FileNotFoundError, NotADirectoryError):
        return []
    # for all the files adds the location of all the files of the user
    for file in files_list:
        problems.append(os.path.join(user_filename, file))
    return problems


def most_average_user():
    """Return the username of the user whose number of problems solved
    is closest to the average."""
    # finds tha average number of solutions
    avg = count_all_solutions() / len(which_solved())
    # the current average user
    curr_avg = ""
    # diff from the average
    diff = 999
    # checks every contributor to be average
    for contributor in sorted(get_contributors()):
        # finds the distance from the number solved to the average
        dist_from_avg = math.fabs(len(problems_solved_by(contributor)) - avg)
        # sets curr avg to contributor if dist is less then current diff
        if dist_from_avg < diff:
            curr_avg = contributor
            diff = dist_from_avg
    return curr_avg


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
        if "_" in problem and problem[problem.index("_") + 1:].isnumeric():
            problems.append(problem[problem.index("_") + 1:])
    return problems


def main():
    print(most_common_language())


if __name__ == '__main__':
    main()
