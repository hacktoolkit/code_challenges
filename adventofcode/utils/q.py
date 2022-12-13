# Python Standard Library Imports
import itertools
from heapq import (
    heappop,
    heappush,
)


class PriorityQueue:
    """An implementation of a priority queue using the native heapq

    https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """

    REMOVED = '<removed-task>'  # placeholder for a removed task

    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.counter = itertools.count()  # unique sequence count

    @property
    def is_empty(self):
        return len(self.entry_finder) == 0

    def contains(self, task):
        return task in self.entry_finder

    def add_task(self, task, priority=None, priority_decrease=None):
        """Add a new task or update the priority of an existing task"""
        if priority is None and priority_decrease is None:
            priority = 0

        if task in self.entry_finder:
            prev_priority, count = remove_task(task)
            if priority is None and priority_decrease is not None:
                priority = prev_priority - priority_decrease

        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        """Mark an existing task as REMOVED.  Raise KeyError if not found."""
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
        priority, count, _ = entry
        return priority, count

    def pop_task(self):
        """Remove and return the lowest priority task. Raise KeyError if empty."""
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return priority, task
        raise KeyError('Pop from an empty priority queue')

    def extract_min(self):
        """Alias of `self.pop_task()"""
        return self.pop_task()

    def add_with_priority(self, task, priority):
        """Alias of `self.add_task()"""
        self.add_task(task, priority=priority)

    def decrease_priority(self, task, decrement):
        self.add_task(task, priority_decrease=decrement)
