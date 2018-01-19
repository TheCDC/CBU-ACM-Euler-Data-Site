import repo_data


class Contributor:
    username = ""  # name of the contributor

    def __init__(self, username):
        # if the username is not a contributor thr
        if username not in repo_data.get_contributors():
            raise NameError("Contributor of \'username\' does not exist")
        self.username = username

    def get_rank(self):
        """Gets the current rank of the user"""
        rank = 1

        # looks for user while incrementing rank
        for contributor in repo_data.top_contributors():
            # if this is the contributor returns rank
            if contributor == self.username:
                return rank
            # increments rank
            rank += 1
        # if contributor not found returns 0
        return 0

    def get_problems(self):
        return repo_data.problems_solved_by(self.username)


class Problem:
    problem_number = 0  # the problem number

    def __init__(self, problem_number):
        # if the problem is not a problem raises an error
        if problem_number not in repo_data.get_problems():
            raise NameError("Problem of \'problem number\' does not exist")
        self.problem_number = problem_number

    def get_who_solved(self):
        return repo_data.who_solved(self.problem_number)

    def get_popularity(self):
        """gets the popularity of the problem"""
        rank = 1

        # looks for problem while incrementing rank
        for problem in repo_data.most_popular_problems():
            # if this is the problem returns rank
            if problem == "Euler " + self.problem_number:
                return rank
            rank += 1

        # if problem not found returns 0
        return 0
