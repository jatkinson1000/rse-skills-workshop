# Exercise 5 - Naming for code clarity and magic numbers

It may seem inconsequential, but carefully naming variables and methods can greatly
improve the readability of code.
Since _“code is read more than it is run”_, this is important for future you, but also
for anyone you collaborate with.

## Naming

Well-considered naming helps to make code self-documenting, reducing potential for
future bugs due to misunderstandings.

Some key points to consider:

- Show the intention -- how will someone else (future you) read it?
- Use readable, pronounceable, memorable, and searchable names:
  ```
  ms    --> mass
  chclt --> chocolate
  stm   --> stem
  ```
  avoid abbreviations and single letters unless commonly used
- Employ concept consistency \
  e.g. only one of `get_`, `retrive_`, `fetch_` in the code base
- Describe content rather than storage type \
  Use plurals to indicate groups \
  Name booleans using prefixes like `is_`, `has_`, `can_` and avoid negations like `not_`:
  ```
  array       --> dogs                    float_or_int --> returns_int
  age_int     --> age                     not_plant    --> is_plant
  country_set --> countries               sidekick     --> has_sidekick
  ```


## Explaining variables

Explaining variables are intermediate variables that help clarify the code for readers.

For example, the following code is rather unclear as to what it achieves:

```python
import re

re.search("^\\+?[1-9][0-9]{7,14}$", "Sophie: CV56 9PQ, +12223334444")
```

Whilst the following has the same functionality, but uses explaining variables to
make the intention clear.
The code is more self-documenting.

```python
import re

phone_number_regex = "^\\+?[1-9][0-9]{7,14}$"
re.search(phone_number_regex, "Sophie: CV56 9PQ, +12223334444")
```


## Magic numbers

Magic numbers are numerical values in code that are not immediately obvious.
They are:

- Hard to read
- Hard to maintain
- Hard to adapt

To handle these we have a few options, depending on the context:

- Set to a constant
- Add an explaining variable conveying meaning
- Use a comment to explain the value

For example, consider the code in `pendulum.py`.
Can you identify the magic numbers in this code?
How do you think each should be addressed?

You can look at the updated code in  `pendulum_no_magic.py` for an improved version.


## Exercise

Look through the precipitation code for any names of variables or methods that could be
improved or clarified and update them.^[Note if you are using an IDE like Intellij or
VSCode you can use automatic renaming. Or try :%s/<old>/<new>/gc in vim.]

Look through the code and identify any magic numbers.
Implement what you feel to be the best approach in each case.

Does this make the code easier to follow?

Consider the following, can you find an example of each:

- Show the intention -- how will someone else (future you) read it
- Use readable, pronounceable, memorable, and searchable names
- Keep it simple using technical terms where appropriate
- Employ concept consistency in the code base
- Describe content rather than type
- Use plurals to indicate groups
- Name booleans using prefixes 
- Use explaining variables
