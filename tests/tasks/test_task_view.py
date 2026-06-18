from django.test import Client, TestCase

from task_manager.models import Tasks
from account.models import User
from task_manager.models.tasks import TaskStatus

class TestTaskView(TestCase):

    def test_task_list(self):
        client = Client()

        test_task_name = "test task"
        test_default_status = TaskStatus.CREATED
        test_priority = 1

        test_user_email = "test@test.com"
        test_password = "1234"

        user = User.objects.create_user(
            email=test_user_email,
            password=test_password)

        client.force_login(user)

        Tasks.objects.create(
            name="test task",
            priority=test_priority,
            assignee = user
        )

        response = client.get("/tasks/")

        self.assertEqual(response.status_code,200)

        objects = response.context["object_list"]
        self.assertEqual(len(objects),1)

        self.assertEqual(objects[0].name, test_task_name)
        self.assertEqual(objects[0].priority, test_priority)
        self.assertEqual(objects[0].status, test_default_status)
        self.assertEqual(objects[0].assignee, user)


#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.islower())
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
#
# if __name__ == '__main__':
#     unittest.main()