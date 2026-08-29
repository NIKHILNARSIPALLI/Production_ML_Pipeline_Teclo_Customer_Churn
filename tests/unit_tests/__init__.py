"""
The file __init__.py (written with two underscores on each side) serves one main purpose:
it tells Python to treat a directory as an importable module or package. Without it,
Python might just see a folder as a collection of random, separate scripts rather
than a unified project.

1. It Unlocks "Dot" Navigation
    When you write from src.test.test import my_function, Python has to look at your folders
    like steps on a ladder. The presence of __init__.py tells Python: "Yes, it is safe to step
    inside the src folder, and yes, it is safe to step inside the test folder."

2. It Initializes Code Upon Import (Optional)
    Most of the time, __init__.py is kept completely empty. However, if you do put Python code
    inside it, that code will execute automatically the exact millisecond someone imports anything
    from that folder. For example, if you want a specific variable or setup script to run whenever
    your package is touched, you can put it inside __init__.py.
"""