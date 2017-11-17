import unittest
import repo_data as rd


class DataSiteTest(unittest.TestCase):

    def test_language_Of_File(self):
        self.assertEqual(rd.language_of_file("test.py"), "Python")
        self.assertEqual(rd.language_of_file("ASDJAPOksnaldkns.java"), "Java")
        self.assertEqual(rd.language_of_file(")@)$@#RKLLS.rb"), "Ruby")
        self.assertEqual(rd.language_of_file("matlabforsomereason.m"), "MatLab")
