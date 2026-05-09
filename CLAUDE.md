# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Heapsifter is a CLI todo list manager that uses heap data structures for prioritizing tasks. The core philosophy is that you should focus on the most important tasks while maintaining less important items in a heap structure for efficient retrieval.

## Architecture

- **src/heapsifter/__init__.py**: Main CLI application built with Click framework. Contains the core TODO class with user-guided comparison logic and all CLI commands (add, pop, heap, remove, head, combine, sift_one, triage). Entry point is `heapsifter:cli` (exposed via `[project.scripts]`).
- **fibheapsifter.py**: Fibonacci heap implementation with FibHeap class and Node subclass for advanced heap operations (standalone — not imported by the CLI).
- **test_heapsifter.py**: Test suite using pytest and hypothesis for property-based testing.

### Key Components

- **TODO Class**: Custom comparison class that prompts users to prioritize items interactively
- **Heap Operations**: Uses Python's heapq module for standard heap operations, with custom multi_delete function for heap-preserving removal
- **File I/O**: Text-based storage with simple read/write functions for todo.txt files

## Development Commands

### Testing
```bash
uv run pytest
```

### Installation and Setup
```bash
uv sync  # Creates .venv and installs the project (editable)
```
Note: `requirements.txt` and `setup.py` are legacy and no longer authoritative; uv is the build/dep system.

### Running the CLI
```bash
heapsifter --help
heapsifter add
heapsifter pop
heapsifter head -n 5
```

## Dependencies

- **click**: runtime dep, declared in `[project.dependencies]`.
- **pytest** + **hypothesis**: declared in `[dependency-groups].dev` (installed by `uv sync` by default).

## Gotchas

- **`heapq._siftup` is private**: `multi_delete` and `triage` reach into a private heapq API. Keep behavior covered by tests if you touch it.

## Development Notes

- The project uses direnv for environment management
- Interactive prioritization is core to the TODO class - comparisons prompt users to choose between items
- Heap invariant is maintained through careful use of heapq operations and custom deletion logic
- The codebase includes both a standard binary heap (`src/heapsifter/__init__.py`, via `heapq`) and a Fibonacci heap (`fibheapsifter.py`, standalone — not imported by the CLI).
- Visualization/exploration notebooks (`Visualizing Fibonacci Heapsifter.ipynb`, `fibonacci_heap.ipynb`, `heapsifter_dev.ipynb`, `sift_goodreads.ipynb`) live at the repo root.