from threading import Lock

## todo support timeout here
class Condition():
    def __init__(self):
        lock = Lock()
        self._lock = lock
        self.waiters = []
        try:
            self._is_owned = lock._is_owned
        except AttributeError:
            pass

    def __enter__(self):
        print("condition __enter__")
        self._lock.__enter__()
        print("locked acquired")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("condition enter, lock released")
        self._lock.__exit__(exc_type, exc_val,exc_tb)

    def __allocate_waiter_lock(self):
        return Lock()

    def _is_owned(self):
        if self._lock.acquire(0):
            self._lock.release()
            return False
        else:
            return True

    def wait(self):
        if not self._is_owned():
            raise ValueError("acquire lock first")
        try:
            waiter = self.__allocate_waiter_lock()
            waiter.acquire()
            print("waiter lock acquired")
            self.waiters.append(waiter)
            self._lock.release()

            waiter.acquire()
        finally:
            self._lock.acquire()


    def notify(self, n = 1):
        if not self._is_owned():
            raise ValueError("un-acquired lock")

        __waiters = self.waiters[:n]

        if not __waiters:
            return
        for waiter in __waiters:
            waiter.release()
            self.waiters.remove(waiter)

    def notify_all(self):
        self.notify(len(self.waiters))
