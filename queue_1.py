class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def __str__(self):
        return self.data
    
    
class Queue:
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def insert_tail(self, node):
        if self.length == 0:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    def remove_head(self):
        if self.length == 0:
            raise ValueError("Queue is empty. Can't take first element of empty queue")
        node = self.head
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
        node.next = None
        self.length -= 1
        return node

    def empty(self):
        return self.length <= 0
