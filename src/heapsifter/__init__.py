# coding: utf-8
"""
heapsifter
~~~~~~~~~~

A cli application for treating text file lists as heaps.
"""
import random
import heapq
import functools

import click


def is_heap(passed_list):
    """Returns true if the passed list is a heap."""
    for index in range(len(passed_list)):
        if index * 2 + 1 < len(passed_list):
            if passed_list[index] > passed_list[index * 2 + 1]:
                return False
        if index * 2 + 2 < len(passed_list):
            if passed_list[index] > passed_list[index * 2 + 2]:
                return False
    return True


def insert_todo(todos, text):
    """Pushes the text passed as a TODO item into a heap of todos."""
    heapq.heappush(todos, TODO(text))


def review(todos):
    """Asks the user to retype a random todo."""
    item = random.choice(todos)
    click.echo(item.text)
    review = input()
    item.text = review


def write_todos(todo_list, file_name):
    """Writes a given list of todos to the file with file_name."""
    with open(file_name, mode='w') as my_file:
        for item in todo_list:
            print(item.text, file=my_file)


def read_todos(todo_file):
    """Opens a file as a list of TODO objects."""
    try:
        with open(todo_file) as my_file:
            todos = [TODO(todo.strip()) for todo in my_file if todo != '\n']
        return todos
    except FileNotFoundError:
        return []


def prioritize_or_equal(item_a, item_b):
    """Prompts user to compare two items via cli."""
    click.echo("a: {}".format(item_a))
    click.echo("b: {}".format(item_b))
    choice = click.prompt("More important? a/b/(e)qual")
    if choice == 'b':
        return 'less'
    elif choice == 'a':
        return 'greater'
    else:
        return 'equal'


@functools.total_ordering
class TODO(object):
    """Represents a list item, adding custom comparison for user-guided sorting."""
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


@click.group()
def cli():
    pass


@cli.command()
@click.option('-i', '--insertion', prompt='Your todo',
              help='The string you want to add.')
@click.option('--todo_file', default='todo.txt',
              help='The text file destination.',
              type=click.Path())
def add(todo_file, insertion):
    """Add a todo item to a file. """
    todos = read_todos(todo_file)
    insert_todo(todos, insertion)
    write_todos(todos, todo_file)


@cli.command()
@click.option('--todo_file', default='todo.txt',
              help='The file to heap.',
              type=click.Path())
def heap(todo_file):
    """Heapify an unsorted list of items."""
    todos = read_todos(todo_file)
    heapq.heapify(todos)
    write_todos(todos, todo_file)


@cli.command()
@click.option('--todo_file', default='todo.txt',
              help='The todo file to review.',
              type=click.Path())
def pop(todo_file):
    """Display top item in list and optionally remove or repush it.
    """
    todos = read_todos(todo_file)
    if len(todos) == 0:
        click.echo("No todos!")
        return 0
    click.echo(todos[0])
    choice = click.prompt("Mark [d]one, [r]epush, or [C]urrent?")
    if choice == 'd':
        heapq.heappop(todos)
    elif choice == 'r':
        heapq.heapreplace(todos, todos[0])
    write_todos(todos, todo_file)


def multi_delete(todo_list, indexes):
    """Remove the items specified by the indexes in a heap-preserving way."""
    indexes = list(reversed(sorted(indexes)))
    for index in indexes:
        todo_list[index] = todo_list[-1]
        todo_list.pop()
    list_len = len(todo_list)
    for index in indexes:
        if index < list_len:
            heapq._siftup(todo_list, index)
    return todo_list


@cli.command()
@click.option('--todo_file', default='todo.txt',
              help='The todo file to review.',
              type=click.Path())
def remove(todo_file):
    todos = read_todos(todo_file)
    click.echo("Todos:")
    for item_tuple in enumerate(todos):
        click.echo("{}) {}".format(*item_tuple))
    target_list = []
    while True:
        resp = click.prompt("(q)uit or #")
        if resp == 'q':
            break
        else:
            try:
                target = int(resp)
                target_list.append(target)
            except TypeError:
                pass
    new_list = multi_delete(todos, target_list)
    write_todos(new_list, todo_file)


@cli.command()
@click.option('--todo_file', default='todo.txt',
              help='The todo file to review.',
              type=click.Path())
@click.option('-n', '--number', default=5,
              help='Number of todos to show.',
              type=click.INT)
def head(todo_file, number):
    """Get the n (default 5) top items in the heap."""
    todos = read_todos(todo_file)
    [click.echo(todos[n]) for n in range(number)]


@cli.command()
@click.option('--source', type=click.Path())
@click.option('--target', type=click.Path())
def combine(source, target):
    """Add all of source heap's items to target."""
    src = read_todos(source)
    targ = read_todos(target)
    for item in src:
        insert_todo(targ, item)
    write_todos(src, source)


@cli.command()
@click.option('--source', type=click.Path())
@click.option('--target', type=click.Path())
def sift_one(source, target):
    """Pull one item out of a list and insert it into a heap."""
    src = read_todos(source)
    targ = read_todos(target)
    item = heapq.heappop(src)
    heapq.heappush(targ, item)
    write_todos(src, source)
    write_todos(targ, target)


@cli.command()
@click.option('--source', type=click.Path())
@click.option('--out', type=click.Path())
def triage(source, out):
    """Given a source file, split out selected items from the heap and put them into a new
    or existing heap.
    """
    src = read_todos(source)
    replace_list = []
    new = []
    click.echo("[K]eep or [s]ift: ")
    for item in enumerate(src):
        choice = click.prompt(item[1].text)
        if choice == "s":
            replace_list.append(item[0])
    click.echo(replace_list)
    for index in replace_list:
        heapq.heappush(new, src[index])
    for index in reversed(replace_list):
        last = src.pop()
        src[index] = last
        heapq._siftup(src, index)
    write_todos(src, source)
    write_todos(new, out)


if __name__ == '__main__':
    cli()
