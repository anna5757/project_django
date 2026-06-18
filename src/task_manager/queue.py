class EmptyQueueError(Exception):
    pass

class Queue:
    FIFO = "FIFO"
    LIFO = "LIFO"
    STRATEGIES = [FIFO, LIFO]

    def __init__(self, strategy: str = FIFO):
        self.strategy = strategy
        self.storage = []

        if self.strategy not in self.STRATEGIES:
            raise TypeError

    def add(self, item):
        if self.strategy == self.FIFO:
            self.storage.insert(0, item)
        elif self.strategy == self.LIFO:
            self.storage.append(item)

    def remove(self):
        if not self.storage:
            raise EmptyQueueError

        if self.strategy == self.FIFO:
            return self.storage.pop()
        elif self.strategy == self.LIFO:
            return self.storage.pop()

class UniqueQueue(Queue):
    def add(self, item):
        if item in self.storage:
            return
        super().add(item)
        self._last_added = item

    def __len__(self):
        return len(self.storage)

    def last_added(self):
        return getattr(self, "_last_added", None)