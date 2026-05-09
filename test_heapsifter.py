from click.testing import CliRunner
from hypothesis import given, example
from hypothesis.strategies import text
import heapsifter

from heapsifter import TODO
from heapsifter import is_heap

def test_empty_pop():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(heapsifter.pop)
        assert result.exit_code == 0
        assert result.output == "No todos!\n"

def test_add_todo():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(heapsifter.add, input="Write a test.")
        assert result.exit_code == 0

# @given(text())
# def test_add_todo(text_arg):
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         result = runner.invoke(heapsifter.add, input=text_arg)
#         assert result.exit_code == 0 

def test_add_arg():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(heapsifter.add, ["-i", "Pass todo directly."])
        assert result.exit_code == 0
        with open('todo.txt') as todos:
            assert todos.read() == "Pass todo directly.\n"

def test_is_heap():
    heap = [1, 2, 3, 4]
    assert is_heap(heap)
    not_heap = [34, 2, 3, 4, 10]
    assert not is_heap(not_heap)
    sorted_heap = sorted(not_heap)
    assert is_heap(sorted_heap)

def test_heap():
    pass

def test_sift_one():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("first.txt", 'w') as first:
            first.write("Call thing x.\n")
            first.write("File reciepts.\n")
            first.write("Remove thumbtacks.\n")
        with open("second.txt", 'w') as second:
            second.write("Add stuff.\n")
            second.write("Break things.\n")
            second.write("Delete other thing.\n")
        heapsifter.TODO = dummy_todo
        runner.invoke(heapsifter.sift_one, ["--source", "second.txt", "--target", "first.txt"]) 
        # Actually read the items and check is_heap
        first = heapsifter.read_todos('first.txt')
        second = heapsifter.read_todos('second.txt')
        assert any(todo.text == "Add stuff." for todo in first) 

class dummy_todo(TODO):
    """This class is easily sorted because it always compares
    in importancy by lexographical order."""
    def __lt__(self, other):
        return self.text < other.text
    def __eq__(self, other):
        return self.text == other.text
