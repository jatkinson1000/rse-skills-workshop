# Exercise 4 - Linting

This exercise contains the code after it has been formatted and had naming updates.

## Run a linter over the code

We will start by running the ruff linter over the code.
Since we already installed ruff in exercise 1 to use its formatting tool there is no
need to install anything new.


Run `ruff check` on the code and observe the warnings.

```console
ruff check precipitation_climatology.py
```

> [!TIP]
> When re-running ruff to check fixes you may find it useful to use the
> `--output-format=concise` flag to reduce printed output.

## Improving the code

Open the source code in your text editor and modifiy it to fix some of
the linting errors.

We will not deal with all of the errors in this exercise.
You can ignore any warnings about `D100`/`D103` (missing docstrings) and
`PLR2004` (magic values) as we'll come to these in subsequent exercises.

Try and deal with:

- `F401` - Unused imports - these are straightforward 
- `I001` - Unsorted imports - hopefully this makes sense
- `D202` - Blank lines - hopefully this makes sense
- `B006` - Dangerous default - recap the notes/slides

If you feel like it you could try and fix:

- `B904` - Exceptions raised inside try - Why is this helpful for users?

Unless you are really keen don't worry about:

- `PLR0913` - Too many arguments - this is a matter of taste and a simple fix could be
  counterproductive. It usually hints that some refactoring may be required.
  fixing has the potential to introduce bugs if not careful.

As you work through the errors do you understand how adressing them has improved
your code?\
Have you learnt anything new from fixing them?

> [!TIP]
> Don't forget to re-run `ruff format` after you have finished editing your code to keep
> the formatting rules enforced.

## Extension exercises

- See if you can install some form of ruff (or another linter) in your text editor/IDE
  as a language server to highlight mistakes whilst you write! See [ruff editor integration docs](https://docs.astral.sh/ruff/editors/setup/).
- If there are any warnings you are going to ignore, see if you can
  [supress them](https://docs.astral.sh/ruff/linter/#error-suppression)
  so they don't clutter up the report.
- Explore the option of
  [altering the configuration settings](https://docs.astral.sh/ruff/configuration/)
  in the configuration file.
- Explore the different rulesets available in the
  [ruff rules documentation](https://docs.astral.sh/ruff/rules/).
