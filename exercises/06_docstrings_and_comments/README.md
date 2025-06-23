# Exercise 6 - Docstrings and Comments

This exercise contains the code after addressing some of the issues raised by pylint.

## Comments

First open the code and examine the use of comments.

1. Is there any dead code in here?
  - Does it make sense to delete it.
  - If not how else might we be able to handle it.
2. Are comments used in a sensible fashion?
  - Are there any redundant comments that ought to be removed.
  - Is there anything that is currently unclear and would benefit from a comment?

## Docstrings

Work through the file adding docstrings where they are missing.\
If you are unsure about variable types or meanings at any point you can sneak a look
ahead to the code in exercise 5.


## pydocstyle

```bash
pip install pydocstyle
```

Run pydocstyle on the code and observe the output.

```bash
pydocstyle --convention=numpy precipitation_climatology.py
```

What do you need to change to get it to pass without warning?



Tip: _Don't forget to re-run `black` and `pylint` after you have edited your code to
keep the quality up._

## Extension exercises

