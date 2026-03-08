class MyQueue:
    def __init__(self):
        self.max_length = None
        self.queue = []
        self.head = 0
        self.tail = 0

    def set_max_length(self, max_length: int):
        self.max_length = max_length
        self.queue = [None for _ in range(max_length)]

    def push(self, item):
        if item in self.queue:
            # O(n), could get rid of this with some tweaks to max_length and the movement.
            return
        self.queue.insert(self.tail, item)
        self.inc_tail()

    def pop(self):
        item = self.queue[self.head]
        self.queue[self.head] = None
        self.inc_head()
        return item

    def inc_head(self):
        if self.head == self.max_length:
            self.head = 0
            return
        self.head += 1

    def inc_tail(self):
        if self.tail == self.max_length:
            self.tail = 0
            return
        self.tail += 1

    def __str__(self):
        return str(self.queue)