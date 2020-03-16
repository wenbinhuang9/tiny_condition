import unittest
from threading import Thread
from condition import Condition

class Count():
    def __init__(self, count=0):
        self.count = count
        self.cond = Condition()

    def increase(self):
        print("begin increase")
        with self.cond:
            self.count += 1
            self.cond.notify_all()
        print("count increase to {0}".format(self.count))

    def decrease(self):
        print("begin decrease")
        with self.cond:
            if self.count <= 0:
                self.cond.wait()
            self.count -= 1
        print("count decrease to {0}".format(self.count))

class MyTestCase(unittest.TestCase):
    def test_condition(self):
        c = Count()

        def decrease(count):
            print("begin thread function decrease")
            count.decrease()
        t = Thread(target=decrease, args=(c, ))
        t.start()
        c.increase()

if __name__ == '__main__':
    unittest.main()