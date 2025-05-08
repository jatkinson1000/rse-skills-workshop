# Exercise 2 - Formatting

In this exercise we will install Ruff and use it to format our code.


## Install Ruff

To install ruff, from the command line run:
```
pip install ruff
```

This will install it into your virtual environment and make the `ruff` command
available on your command line.


## Run the ruff formatter

We will now run the ruff formatter on the code and observe the changes.

To do this run:
```
ruff format precipitation_climatology.py
```

Note that the file will be reformatted in-place!

You do not need to worry about your code being modified.
As discussed in the workshop, a formatter will only ever change the layout of the code,
and never the intent.


## Inspect the changes

To see what has changed in the file we can compare it to the version of the code
from exercise 01.

For example, using `vimdiff` from the command line:
```
vimdiff ../01_base_code/precipitation_climatology.py precipitation_climatology.py
```

Look at the newly formatted file and note the changes.

- Is it more readable?
- Is there any aspect of the formatting style you find unintuitive?
