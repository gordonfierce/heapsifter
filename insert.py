# coding: utf-8
import random, heapq, functools

def insert_todo(todos, text):
    heapq.heappush(todos, TODO(text))

def review(todos):
    item = random.choice(todos)
    print(item.text)
    review = input()
    item.text = review
    
def write_todos(todo_list, file_name):
    with open(file_name, mode='w') as file:
        for item in todo_list:
            print(item.text, file=file)
            
def read_todos(todo_file):
    with open(todo_file) as file:
        todos = [TODO(todo.strip()) for todo in  file if todo != '\n']
    return todos

@functools.lru_cache(maxsize=None)
def prioritize_or_equal(item_a, item_b):
    print("a: {}".format(item_a))
    print("b: {}".format(item_b))
    choice = input("More important? a/b/(e)qual: ")
    if choice == 'b':
        return 'less'
    elif choice == 'a':
        return 'greater'
    else:
        return 'equal'

@functools.total_ordering
class TODO:
    def __init__(self, text):
        self.text = text
    
    def __repr__(self):
        return "TODO({})".format(self.text)
    
    def __str__(self):
        return self.text
    
    def __eq__(self, other):
        if self.text < other.text:
            return prioritize_or_equal(self.text, other.text) == 'equal'
        else:
            return prioritize_or_equal(other.text, self.text) == 'equal'
    
    def __lt__(self, other):
        if self.text < other.text:
            return prioritize_or_equal(self.text, other.text) == 'greater'
        else:
            return prioritize_or_equal(other.text, self.text) == 'less'

todos = read_todos('todo.txt')
text = input()
insert_todo(todos, text)
write_todos(todos, 'todo.txt')

