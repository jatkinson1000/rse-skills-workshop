# Exercise 3 - Linting

Beyond a consistent formatting style there are often various other ways in which code
can be improved to conform to best practices or avoid certain bugs.

Linting or static analysis uses tools to improve code quality.
They are also a great way to learn better practices and new techniques.

They also help save time and resources by checking code and identifying (some) runtime
issues before execution.


## Run a linter over the code

We will start by running the `ruff` linter over the code.
Since we already installed ruff in exercise 1 to use its formatting tool there is no
need to install anything new.

To warm up take a look at the code in `long_func.py`.
Can you spot anything wrong at a first glance?

Run `ruff check` on the code and observe the warnings.

```bash
ruff check long_func.py
```

> [!TIP]
> When re-running ruff to check fixes you may find it useful to use the
> `--output-format=concise` flag to reduce printed output.

<details>

<summary>Click here for the explanation</summary>

```console
(rse-venv) $ ruff check long_func.py
long_func.py:4:5: ARG001 Unused function argument: `param_two`
long_func.py:4:15: B006 Do not use mutable data structures for argument defaults
long_func.py:5:5: ARG001 Unused function argument: `param_three`
long_func.py:24:5: F821 Undefined name `param_2`
long_func.py:25:12: F821 Undefined name `param_2`
Found 5 errors.

(rse-venv) $
```

We can see from the output that there is a mismatch in name between `param_two` and
`param_2` that would have caused a runtime error.

We can also see that there is some housekeeping to be carried out to remove unused
variables and keep things clean.

Finally, there is a somewhat more cryptic `B006 Do not use mutable data structures`.
To understand this we can ask ruff to provide some explanation by running 

</details>

We can now proceed to running ruff on the full precipitation code:

```
ruff check precipitation_climatology.py
```


## Improving the code

Open the source code in your text editor and modifiy it to fix
the linting errors:

- Try and deal with: `F401` unused imports, `I001` unsorted imports,
  `B006` dangerous default, and `D202` Blank lines
- For a challenge try and fix: `B904` try exceptions

Extensions:

- explore autofixes using the `--fix` flag
- explore rules in development using the `--preview` flag
- try and add linting to your preferred text editor or IDE

As you work through the errors do you understand how adressing them has improved
your code?

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


## Configuration

The default set of linting rules for ruff is quite simple.

The ruleset to be applied can be configured in a `ruff.toml` file, as we do in this project,
or `pyproject.toml` for packaged code.
For full details see the [ruff configuration documentation](https://docs.astral.sh/ruff/configuration/).

Details of the different rules and rulesets that can be selected can be found in the
[ruff rules documentation](https://docs.astral.sh/ruff/rules/).

In this project we use a `ruff.toml` file at the root of the repository.
Take a look and make some changes in preparation for the next
sections:

- We will add the entire `"D"` (pydocstyle) ruleset by adding it to the `select` list.
- We will stop ignoring:
    - `"PLR2004"` (magic number comparisons) and
    - `"E501"` (line length).
  by removing them from the `ignore` list.
- We will add `"D417"` (Missing argument description) by adding it to the
  `extend-select` list.


## Other languages

Similar tools for linting and static analysis exist for other languages:

- C and C++ - [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) and
  [cppcheck](https://cpp-linter.github.io/)
- Fortran - [fortitude](https://github.com/PlasmaFAIR/fortitude)
- Rust - [clippy](https://doc.rust-lang.org/clippy/)
- R - [lintr](https://lintr.r-lib.org/)

More generally see [this list of static analysis tools](https://github.com/analysis-tools-dev/static-analysis).
