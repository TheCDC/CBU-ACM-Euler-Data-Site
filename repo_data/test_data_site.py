import unittest
import repo_data as rd


class DataSiteTest(unittest.TestCase):

    def test_language_Of_File(self):
        self.assertEqual(rd.language_of_file("test.py"), "Python")
        self.assertEqual(rd.language_of_file("ASDJAPOksnaldkns.java"), "Java")
        self.assertEqual(rd.language_of_file(")@)$@#RKLLS.rb"), "Ruby")
        self.assertEqual(rd.language_of_file("matlabforsomereason.m"), "MatLab")

    def test_which_solved(self):
        self.assertListEqual(rd.which_solved()[0:5], ["Euler 001", "Euler 002", "Euler 003", "Euler 004", "Euler 005"])

    def test_most_popular_problem(self):
        self.assertListEqual(rd.most_popular_problems()[0:5], ["Euler 001", "Euler 002", "Euler 004",
                                                               "Euler 005", "Euler 007"])

    def test_top_contributor(self):
        self.assertListEqual(rd.top_contributors()[0:3],
                            ["Christopher D Chen", "Chris Nugent", "Christopher Nugent"])

    def test_most_average_user(self):
        self.assertEqual(rd.most_average_user(), "Alex Liu")

    def test_find_solution_files(self):
        self.assertListEqual(rd.find_solution_files("1", "Alex Liu"),
                             ['C:\\Users\\Alex Liu\\cbu_csse_euler\\euler_001/Alex Liu'])
        self.assertListEqual(rd.find_solution_files("5", "Alex Liu"), [])

    # tests the helper method to get problems
    def test_get_problems(self):
        self.assertListEqual(rd.get_problems()[0:5], ["001", "002", "003", "004", "005"])
        self.assertListEqual(rd.get_problems()[41:46], ["055", "067", "079", "080", "085"])

    # These two test have to be manually updated with the current number of contributors and problems
    # tests the helper method to get contributors
    def test_get_contributors(self):
        self.assertSetEqual(rd.get_contributors(), {"Alex Liu", "Christopher Nugent", "Christopher D Chen", "Craig Mariani",
                                                    "Hannah Bernal", "Micah Steinbock", "Anthony Henson", "Dylan Stump",
                                                    "Chris Nugent"})

    def test_most_common_language(self):
        self.assertEqual('python', rd.most_common_language())
