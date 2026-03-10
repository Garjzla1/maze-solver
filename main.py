import sys

from my_queue import MyQueue


class NullNode:
    def __init__(self):
        self.moveable = False
        self.prev_val = None
        self.value = None
        self.x = False
        self.y = False
        self.is_end = False

    def set_prev_val(self, prev_val):
        self.prev_val = prev_val

    def move(self):
        return

    def __str__(self):
        return "NULL_NODE"


class Node:
    def __init__(self, x, y, moveable: bool, grid):
        self.grid = grid
        self.x = x
        self.y = y
        self.is_start = False
        self.is_end = False
        self.value = None
        self.moveable = moveable
        self.prev_val = None
        self.neighbors = list()  # could make this a tuple
        self.color = None

    def set_is_start(self, is_start: bool):
        self.is_start = is_start

    def set_is_end(self, is_end: bool):
        self.is_end = is_end

    def set_value(self, value):
        self.value = value

    def set_prev_val(self, prev_val):
        self.prev_val = prev_val

    def set_moveable(self, moveable: bool):
        self.moveable = moveable

    def get_value(self):
        return self.value

    def move(self):
        if not self.moveable:
            return
        self.value = self.prev_val + 1
        for neighbor in self.neighbors:
            neighbor.set_prev_val(self.value)
            if not neighbor.moveable:
                continue
            self.grid.push_to_queue(neighbor)
        self.moveable = False

    def get_next(self):
        for neighbor in self.neighbors:
            if neighbor.value is None:
                continue
            if neighbor.value + 1 == self.value:
                return neighbor
        raise Exception("BIG EXPLOSION")

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y


class Grid:
    def __init__(self):
        self.grid = []
        self.queue = MyQueue()
        self.start_node = None
        self.end_node = None

    def add_row(self, r: str):
        row = list(r)
        y = len(self.grid)
        node_row = []
        for x, val in enumerate(row):
            moveable = False if val == "1" else True
            node = Node(x, y, moveable, self)
            if val.upper() == "E":
                self.start_node = node
                node.set_is_start(True)
            node_row.append(node)

        self.grid.append(node_row)

    def set_grid(self, buf: list[str]):
        for l in buf:
            self.add_row(l.strip())

    def set_neighbors_and_end(self):
        x_max = len(self.grid[0])-1
        y_max = len(self.grid)-1
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                if not node.moveable:
                    continue
                top = self.grid[y+1][x] if y != y_max else NullNode()
                right = self.grid[y][x+1] if x != x_max else NullNode()
                bottom = self.grid[y-1][x] if y != 0 else NullNode()
                left = self.grid[y][x-1] if x != 0 else NullNode()
                # neighbors are clockwise
                node.neighbors.append(top)
                node.neighbors.append(right)
                node.neighbors.append(bottom)
                node.neighbors.append(left)

                node.set_is_end((x == 0 or y == 0 or y == y_max or x == x_max) and node.moveable and not node.is_start)

    def set_max_queue_size(self):
        x = len(self.grid[0])
        y = len(self.grid)
        self.queue.set_max_length(x * y)  # this could probably be smaller

    def push_to_queue(self, node: Node):
        self.queue.push(node)

    def print_vals(self):
        s = ""
        for row in self.grid:
            for node in row:
                out = str(node.value)
                color = str(node.color)
                if out == "None":
                    out = "?"
                if color == "None":
                    color = ""
                s += f"\033[{color}m{out:>3}"
            s += "\033[0m\n"
        print(s)

    def solve(self):
        node = self.start_node
        node.set_prev_val(-1)  # when incremented the value will be 0
        while not node.is_end:
            # if moveable
            # node value = prev_val + 1
            # then sets current value to neighbor's prev_val
            # then pushes neighbors to the queue
            node.move()
            # self.print_vals()

            node = self.queue.pop()
            if node is None:
                node = NullNode()

        node.value = node.prev_val + 1
        self.end_node = node
        self.color_solution_smart()
        self.print_vals()

    def find_solution_dumb(self) -> list[Node]:
        solution = []
        node = self.end_node
        while not node.is_start:
            node = node.get_next()
            solution.append(node)
        return solution

    def color_solution_smart(self):
        node = self.end_node
        node.color = 32
        while not node.is_start:
            node = node.get_next()
            node.color = 36
        node.color = 31


def main():
    grid = Grid()
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as input_buffer:
            grid.set_grid(input_buffer.readlines())
    else:
        while True:
            row = input()
            if row == "":
                break
            grid.add_row(row)

    grid.set_neighbors_and_end()
    grid.set_max_queue_size()
    grid.solve()
    solution = grid.find_solution_dumb()
    while solution:
        print(solution.pop())


"""
solve maze make brain go burr
"""


if __name__ == "__main__":
    main()
