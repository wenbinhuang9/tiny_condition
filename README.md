# tiny_condition
A simple implementation to condition variable.

1. Using mutual lock
2. Using a waiter lock queue 

# Code
```
cond = Condition()

cond.wait()

cond.notify()

cond.notify_all()
```