from django.test import TestCase
from ophasebase.models import Building, Ophase, OphaseCategory, Room
from staff.models import TutorGroup
from students.models import Student

from .models import Assignment, ExamRoom, PersonToExamRoomAssignment as ptr


class examAssigment(TestCase):
    def setUp(self):
        self.oc = OphaseCategory.objects.create(name="Test Cat", slug="slug", lang="de", priority=1)
        self.op = Ophase.objects.create(name="testOphase", is_active=True, contact_email_address = "test@example.com")
        self.tg = TutorGroup.objects.create(ophase=self.op, name="Test Group", group_category=self.oc)

        self.asg = Assignment(ophase = Ophase.current(), group_category = self.oc, spacing = 2)

        sb = Building.objects.create(area="S", subarea=2, number="02")

        room_big = Room.objects.create(building=sb, number="Big", type="HS", has_beamer=True, capacity=40)
        room_medium = Room.objects.create(building=sb, number="Medium", type="HS", has_beamer=True, capacity=20)
        room_small = Room.objects.create(building=sb, number="Small", type="HS", has_beamer=True, capacity=10)

        self.big = ExamRoom.objects.create(room=room_big, available=True, capacity_1_free=20, capacity_2_free=10)
        self.medium = ExamRoom.objects.create(room=room_medium, available=True, capacity_1_free=10, capacity_2_free=5)
        self.small = ExamRoom.objects.create(room=room_small, available=True, capacity_1_free=6, capacity_2_free=3)


    def create_exam_writer(self, no_writer):
        """
        Set the given number of students which want to wirte an exam
        :param no_writer: the number of students which want to write an exam
        :return:
        """
        for i in range(0, no_writer):
            dn = "{:02}".format(i)
            dn_no = dn + "No exam"
            Student.objects.create(want_exam=True, prename=dn, name=dn, tutor_group=self.tg, ophase=self.op)
            Student.objects.create(want_exam=False, prename=dn_no, name=dn_no, tutor_group=self.tg, ophase=self.op)

    def test_create_exam_wirter(self):
        """
        test the create_exam_writer method
        :return:
        """
        no_writer = 5
        self.create_exam_writer(no_writer)
        self.assertEqual(no_writer * 2, Student.objects.count())
        self.assertEqual(no_writer, Student.objects.filter(want_exam=True).count())
        self.assertEqual(no_writer, Student.objects.filter(want_exam=False).count())

    def test_assign_average_all_rooms_normal(self):
        """
        15 students want to write the exam we want to use all rooms
        """
        number_writer = 15
        self.create_exam_writer(number_writer)
        self.assertEqual(number_writer, Student.objects.filter(want_exam=True).count())
        self.assertEqual(0, ptr.objects.count())

        self.asg.mode=1
        with self.assertNumQueries(9):
            self.asg.save()

        self.assertEqual(number_writer, ptr.objects.count())
        self.assertEqual(9, ptr.objects.filter(room=self.big).count())
        self.assertEqual(5, ptr.objects.filter(room=self.medium).count())
        self.assertEqual(1, ptr.objects.filter(room=self.small).count())

    def test_assign_average_all_rooms_overfull(self):
        """
        20 students want to write the exam we want to use all rooms
        """
        number_writer = 20

        self.create_exam_writer(number_writer)
        self.assertEqual(number_writer, Student.objects.filter(want_exam=True).count())
        self.assertEqual(0, ptr.objects.count())

        self.asg.mode=0
        with self.assertNumQueries(9):
            self.asg.save()

        self.assertEqual(number_writer, ptr.objects.count())
        self.assertEqual(12, ptr.objects.filter(room=self.big).count())
        self.assertEqual(6, ptr.objects.filter(room=self.medium).count())
        self.assertEqual(2, ptr.objects.filter(room=self.small).count())

    def test_assign_min_rooms_normal(self):
        """
        14 students want to write the exam we want to use only the minimum required rooms
        """
        number_writer = 14
        self.create_exam_writer(number_writer)
        self.assertEqual(number_writer, Student.objects.filter(want_exam=True).count())
        self.assertEqual(0, ptr.objects.count())

        self.asg.mode=1
        with self.assertNumQueries(9):
            self.asg.save()

        self.assertEqual(number_writer, ptr.objects.count())
        self.assertEqual(9, ptr.objects.filter(room=self.big).count())
        self.assertEqual(5, ptr.objects.filter(room=self.medium).count())
        self.assertEqual(0, ptr.objects.filter(room=self.small).count())


    def test_assign_min_rooms_overfull(self):
        """
        20 students want to write the exam we want to use only the minimum required rooms
        This reproduces the bug from https://github.com/d120/pyophase/issues/268
        """
        number_writer = 20
        self.create_exam_writer(number_writer)
        self.assertEqual(number_writer, Student.objects.filter(want_exam=True).count())
        self.assertEqual(0, ptr.objects.count())

        self.asg.mode=1
        with self.assertNumQueries(9):
            self.asg.save()

        self.assertEqual(number_writer, ptr.objects.count())
        self.assertEqual(12, ptr.objects.filter(room=self.big).count())
        self.assertEqual(6, ptr.objects.filter(room=self.medium).count())
        self.assertEqual(2, ptr.objects.filter(room=self.small).count())
