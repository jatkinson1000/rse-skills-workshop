# Exercise 4 - Linting

This exercise contains the original code after applying black.

## Install pylint

```bash
pip install pylint
```

## Run pylint

Run pylint on the code and observe the warnings and ratings.

```bash
pylint precipitation_climatology.py
```

## Improving the code

Open the source code in your text editor and modifiy it to fix some of
the linting errors.

We will not deal with all of the errors in this exercise.
You can ignore any warnings about `Missing docstrings` or `f-strings` as we'll come to
these in subsequent exercises.

Try and deal with:

- `W0611` - Unused imports - these are straightforward 
- `C0412` - Ungrouped imports - hopefully this makes sense
- `W0102` - Dangerous default - recap the notes/slides

If you feel like it you could try and fix:

- `W0621` - Redefining name - Why is this not ideal? Beware, addressing this has the
  potential to introduce bugs if not careful.
- `W1514` - Unexplicit `open`

Unless you are really keen don't worry about:

- `R0913` - Too many arguments - this is a matter of taste and a simple fix could be
  counterproductive. It usually hints that some refactoring may be required.
- `C0103` - Unconforming naming style - Again, this could be a matter of taste and
  fixing has the potential to introduce bugs if not careful.

As you work through the errors do you understand how adressing them has improved
your code?\
Have you learnt anything new from fixing them?


Tip: _Don't forget to re-run `black` after you have finished editing your code to keep
the formatting rules enforced._

## Extension exercises

- See if you can install some form of pylint (or another linter) in your text editor/IDE
  to highlight mistakes whilst you write!
- If there are any pylint warnings you are going to ignore, see if you can
  [supress them](https://pylint.pycqa.org/en/latest/user_guide/messages/message_control.html)
  so they don't clutter up the report.
- Explore the option of
  [altering the configuration settings](https://pylint.pycqa.org/en/latest/user_guide/configuration/index.html)
  of pylint, either via the command line or using a configuration file.
