import unittest
import random

from src.task_manager.queue import Queue, EmptyQueueError, UniqueQueue

class TestQueue(unittest.TestCase):

    def setUp(self):
        strategy = "FIFO"
        self.queue = Queue(strategy)


    def test_no_exist_strategy(self):
        with self.assertRaises(TypeError):
            queue = Queue("FIFA")


    def test_add_item_to_queue(self):
        item_1 = 5
        self.queue.add(item_1)
        item = self.queue.storage[0]
        self.assertEquals(item_1,item)


    def test_add_and_get_item_from_queue(self):
        item_1 = 5
        self.queue.add(item_1)
        item = self.queue.remove()
        self.assertEquals(item_1,item)


    def test_add_and_get_multi_value_from_queue(self):
        item_1 = 5
        item_2 = 4
        item_3 = 3
        self.queue.add(item_1)
        self.queue.add(item_2)
        self.queue.add(item_3)
        item = self.queue.remove()
        self.assertEquals(item_1,item)
        item = self.queue.remove()
        self.assertEquals(item_2,item)
        item = self.queue.remove()
        self.assertEquals(item_3,item)

    def test_add_many_random_items(self):
        item_1 = 5
        self.queue.add(item_1)
        for _ in range(10):
            self.queue.add(random.randint(10,20))
        item = self.queue.remove()
        self.assertEquals(item_1,item)

    def test_get_item_from_empty_queue(self):
        with self.assertRaises(EmptyQueueError):
            self.queue.remove()


class TestUniqueQueue(unittest.TestCase):

    def setUp(self):
        self.queue = UniqueQueue()

    def test_unique_and_order(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(1)
        self.queue.add(3)

        self.assertEqual(self.queue.storage, [3, 2, 1])

        self.assertEqual(self.queue.remove(), 1)
        self.assertEqual(self.queue.remove(), 2)
        self.assertEqual(self.queue.remove(), 3)

class TestUniqueQueueLengthAndLast(unittest.TestCase):

    def setUp(self):
        self.queue = UniqueQueue()

    def test_len_and_last_added(self):
        self.assertEqual(len(self.queue), 0)
        self.assertIsNone(self.queue.last_added())

        self.queue.add(10)
        self.queue.add(20)
        self.queue.add(10)

        self.assertEqual(len(self.queue), 2)
        self.assertEqual(self.queue.last_added(), 20)

        self.queue.add(30)

        self.assertEqual(len(self.queue), 3)
        self.assertEqual(self.queue.last_added(), 30)


class TestLIFOQueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue(strategy=Queue.LIFO)

    def test_lifo_add_and_remove_single(self):
        self.queue.add(1)
        self.assertEqual(self.queue.remove(), 1)

    def test_lifo_order(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(3)

        self.assertEqual(self.queue.remove(), 3)
        self.assertEqual(self.queue.remove(), 2)
        self.assertEqual(self.queue.remove(), 1)

    def test_lifo_empty_exception(self):
        with self.assertRaises(EmptyQueueError):
            self.queue.remove()


class TestUniqueQueueExtended(unittest.TestCase):

    def setUp(self):
        self.queue = UniqueQueue()

    def test_unique_add(self):
        self.queue.add(1)
        self.queue.add(1)
        self.assertEqual(len(self.queue.storage), 1)

    def test_len_empty(self):
        self.assertEqual(len(self.queue), 0)

    def test_len_after_add(self):
        self.queue.add(1)
        self.queue.add(2)
        self.assertEqual(len(self.queue), 2)

    def test_last_added_initial(self):
        self.assertIsNone(self.queue.last_added())

    def test_last_added_updates(self):
        self.queue.add(1)
        self.queue.add(2)
        self.assertEqual(self.queue.last_added(), 2)

    def test_last_added_ignore_duplicates(self):
        self.queue.add(1)
        self.queue.add(1)
        self.assertEqual(self.queue.last_added(), 1)

    def test_unique_order(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(3)

        self.assertEqual(self.queue.remove(), 1)
        self.assertEqual(self.queue.remove(), 2)
        self.assertEqual(self.queue.remove(), 3)

    def test_len_after_remove(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.remove()
        self.assertEqual(len(self.queue), 1)

    def test_last_added_after_multiple(self):
        self.queue.add(5)
        self.queue.add(10)
        self.queue.add(20)
        self.assertEqual(self.queue.last_added(), 20)

    def test_mixed_operations(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.remove()
        self.queue.add(3)

        self.assertEqual(len(self.queue), 2)
        self.assertEqual(self.queue.last_added(), 3)



if __name__ == '__main__':
    unittest.main()



