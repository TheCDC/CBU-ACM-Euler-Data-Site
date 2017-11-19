import unittest
import repo_data as rd


class DataSiteTest(unittest.TestCase):

    def test_language_Of_File(self):
        self.assertEqual(rd.language_of_file("test.py"), "Python")
        self.assertEqual(rd.language_of_file("ASDJAPOksnaldkns.java"), "Java")
        self.assertEqual(rd.language_of_file(")@)$@#RKLLS.rb"), "Ruby")
        self.assertEqual(rd.language_of_file("matlabforsomereason.m"), "MatLab")

    # tests the helper method to get problems
    def test_get_problems(self):
        self.assertListEqual(rd.get_problems()[0:5], ["001", "002", "003", "004", "005"])
        self.assertListEqual(rd.get_problems()[41:46], ["055", "067", "079", "080", "085"])

    # These two test have to be manually updated with the current number of contributors and problems
    # tests the helper method to get contributors
    def test_get_contributors(self):
        self.assertSetEqual(rd.get_contributors(), {"Alex Liu", "Christopher Nugent", "Christopher D Chen", "Craig Mariani",
                                                    "Hannah Bernal", "Micah Steinbock", "Anthony Henson", "Dylan Stump",
                                                    "Chris Nugent", "FIrstName MIddleInitial LastName"})

