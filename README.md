# File Handling CLI (Python)

A small interactive command-line program that lets you **create**, **append**, **read**, and **delete** files in the current working directory. It also lists the files/folders it can see before each operation.

## What `main.py` does

When you run `main.py`, it shows a menu:

- `1` → Create a new file and write initial content
- `2` → Add data in a file (append new content to an existing file)
- `3` → Read and print an existing file
- `4` → Delete an existing file

Before each action, the program prints a numbered list of files/folders found under the current directory using recursive search.

## Requirements

- Python 3.8+ (works on Windows/macOS/Linux)

No external packages are required.

## How to run

From the folder that contains `main.py`:

```bash
python main.py
```

> Tip: The script uses `Path(".")`, so it operates relative to **your current terminal folder**.

## Usage examples

### 1) Create a file

1. Choose `1`
2. Enter a filename (example: `notes.txt`)
3. Enter the content to write

Expected result:

- If the file does **not** exist → it is created and written to
- If the file already exists → you will see `FILE ALREADY EXISTS`

### 2) Append to a file

1. Choose `2`
2. Enter an existing filename (example: `notes.txt`)
3. Enter the content to append

Notes:

- Appends text with a leading newline (`\n`) so each entry goes on a new line.

### 3) Read a file

1. Choose `3`
2. Enter an existing filename (example: `notes.txt`)

Expected result:

- The file contents are printed to the terminal

### 4) Delete a file

1. Choose `4`
2. Enter an existing filename (example: `notes.txt`)

Expected result:

- The file is removed using `Path.unlink()`

## Error handling

- Non-numeric menu input is caught as a `ValueError`.
- Each file operation is wrapped in `try/except` and prints a friendly error message.

## Project files

- `main.py` — the interactive file-handling program
- `python.py` — a small test file (prints `hii`)
