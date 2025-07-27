from unittest import TestCase, main

from project.student import Student

class TestStudent(TestCase):
    def setUp(self):
        self.student1 = Student("Student_1", {"Python":["n1", "n2", "n3"], "JS":["n1", "n2"]})
        self.student2 = Student("Student_2")

    def test_init_with_courses(self):
        self.assertEqual("Student_1", self.student1.name)
        self.assertEqual({"Python":["n1", "n2","n3"], "JS":["n1", "n2"]}, self.student1.courses)

    def test_init_without_courses(self):
        self.assertEqual("Student_2", self.student2.name)
        self.assertEqual({}, self.student2.courses)

    def test_enroll_existing_course(self):
        result = self.student1.enroll("Python", ['n4', "n5"],"Y")
        self.assertEqual("Course already added. Notes have been updated.", result)
        self.assertEqual({"Python":["n1", "n2", "n3", "n4", "n5"], "JS":["n1", "n2"]}, self.student1.courses)

        result = self.student1.enroll("Python", ['n6', "n7"],"")
        self.assertEqual("Course already added. Notes have been updated.", result)
        self.assertEqual({"Python":["n1", "n2", "n3", "n4", "n5", "n6", "n7"], "JS":["n1", "n2"]}, self.student1.courses)

    def test_enroll_not_existing_courses_with_y(self):
        result = self.student1.enroll("C#", ['n1', "n2"], "Y")
        self.assertEqual("Course and course notes have been added.", result)
        self.assertIn("C#", self.student1.courses)
        self.assertEqual(['n1', "n2"], self.student1.courses["C#"])

    def test_enroll_not_existing_courses_with_empty_string(self):
        result = self.student1.enroll("C#", ['n1', "n2"], "")
        self.assertEqual("Course and course notes have been added.", result)
        self.assertIn("C#", self.student1.courses)
        self.assertEqual(['n1', "n2"], self.student1.courses["C#"])

    def test_enroll_not_existing_courses_without_notes(self):
        result = self.student2.enroll("C#", ['n1', "n2"], "N")
        self.assertEqual("Course has been added.", result)
        self.assertIn("C#", self.student2.courses)
        self.assertEqual([], self.student2.courses["C#"])

    def test_add_notes_successful(self):
        result = self.student1.add_notes("JS", "n3")
        self.assertEqual("Notes have been updated", result)
        self.assertIn('n3', self.student1.courses["JS"])

    def test_add_notes_error(self):
        with self.assertRaises(Exception) as e:
            self.student2.add_notes("JS", "n3")
        self.assertEqual("Cannot add notes. Course not found.", str(e.exception))

    def test_leave_course_successful(self):
        result = self.student1.leave_course("Python")
        self.assertEqual("Course has been removed", result)
        self.assertNotIn("Python", self.student1.courses)

    def test_leave_course_error(self):
        with self.assertRaises(Exception) as e:
            self.student2.leave_course("Python")
        self.assertEqual("Cannot remove course. Course not found.", str(e.exception))


if __name__ == "main":
    main()