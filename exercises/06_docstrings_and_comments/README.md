# Exercise 6 - Docstrings and Comments


## Comments

Comments in code are tricky, and very much to taste.

Some thoughts:

> "Programs must be written for people to read and [...] machines to execute."\
> &emsp; - Hal Abelson

> "A bad comment is worse than no comment at all."

> "A comment is a lie waiting to happen."

=> Comments have to be maintained, just like the code, and there is no way to check them!

Here are some guidelines to consider when adding comments to your code:

- Comments should not duplicate the code.
- Good comments do not excuse unclear code.
  - Comments should dispel confusion, not cause it.
  - If you can't write a clear comment, there may be a problem with the code.
- Explain unidiomatic code in comments.
- Provide links to:
  - the original source of copied code.
  - external references where they will be most helpful.
- Use comments to mark incomplete implementations.
- Comments are not documentation.
  - Read by developers, documentation is for...

And here are some comments to avoid:

- Dead code e.g.
  ```python
  # plt.plot(time, velocity, "r0")
  plt.plot(time, velocity, "kx")
  # plt.plot(time, acceleration, "kx")
  # plt.ylabel("acceleration")
  plt.ylabel("velocity")
  ```
- Variable definitions e.g.
  ```python
  # Set Force
  f = m * a
  ```
- Redundant comments e.g.
  ```python
  i += 1  # Increment i
  ```

See the [Stackoverflow blog](https://stackoverflow.blog/2021/12/23/best-practices-for-writing-code-comments/)
, and [RealPython comments lesson](https://realpython.com/lessons/importance-writing-good-code-comments/)
for more.


## Docstrings

Docstrings and documentation is what makes your code reusable by yourself and others.

In python docstrings are designated at the start of _'things'_ using triple
quotes: `"""..."""`.
[PEP257](https://peps.python.org/pep-0257/) tells us _what_ docstrings should say,
whilst specific conventions tell us _how_ they should say it.
Various formatting options exist: numpy, Google, reST, etc.
We will follow numpydoc as it is readable and widely used in scientific code.
Full guidance for [numpydoc is available](https://numpydoc.readthedocs.io/en/latest/format.html).

Where comments describe how things _work_, docstrings describe how to _use_ them.

All docstrings should communicate at least the following:

- A description of what the thing is.
- A description of any inputs (`Parameters`).
- A description of any outputs (`Returns`).

```python
"""
Short one-line description.

Parameters
----------
name : type
    description of parameter

Returns
-------
name : type
    description of return value
"""
```

Additional features that may be included:

- Extended summary
- Warnings/Errors raised
- Usage examples
- Key references

The following is an example of how a function would be documented using numpy
conventions:
```python
def calculate_gyroradius(mass, v_perp, charge, B, gamma=None):
    """
    Calculates the gyroradius of a charged particle in a magnetic field

    Parameters
    ----------
    mass : float
        The mass of the particle [kg]
    v_perp : float
        velocity perpendicular to magnetic field [m/s]
    charge : float
        particle charge [coulombs]
    B : float
        Magnetic field strength [teslas]
    gamma : float, optional
        Lorentz factor for relativistic case. default=None for non-relativistic case.

    Returns
    -------
    r_g : float
        Gyroradius of particle [m]

    Notes
    -----
    .. [1]  Walt, M, "Introduction to Geomagnetically Trapped Radiation,"
       Cambridge Atmospheric and Space Science Series, equation (2.4), 2005.
    """

    r_g = mass * v_perp / (abs(charge) * B)

    if gamma:
        r_g = r_g * gamma

    return r_g
```


## ruff pydocstyle

At the end of exercise 3 we enabled some additional rules in our ruff setup, including
the pydocstyle ruleset (`"D"`) that is used for checking documentation.

This will enforce the rules of PEP257 and check that docstrings contain the information
they need.

As an example run `ruff check` on the `gyroradius.py` file in this directory:
```bash
ruff check gyroradius.py
```

which should give something like:
```console
exercises/06_docstrings_and_comments/gyroradius.py:3:5: D417 Missing argument description in the docstring for `calculate_gyroradius`: `B`
exercises/06_docstrings_and_comments/gyroradius.py:4:5: D202 [*] No blank lines allowed after function docstring (found 1)
exercises/06_docstrings_and_comments/gyroradius.py:4:5: D400 First line should end with a period
exercises/06_docstrings_and_comments/gyroradius.py:4:5: D401 First line of docstring should be in imperative mood: "Calculates the gyroradius of a charged particle in a magnetic field"
Found 4 errors.
```
indicating where we are in violation of PEP257.

Note that the additional `"D417"` rule is able to tell us when a parameter is missing
from the docstring.

See if you can resolve these warnings.


## Exercise 6

This exercise contains the code after addressing some of the issues raised by ruff in
exercise 3 and naming in exercise 5.

First open the code and examine the use of comments:

1. Is there any dead code in here?
  - Does it make sense to delete it.
  - If not how else might we be able to handle it.
2. Are comments used in a sensible fashion?
  - Are there any redundant comments that ought to be removed.
  - Is there anything that is currently unclear and would benefit from a comment?

Now work through the file adding docstrings where they are missing.
If you are unsure about variable types or meanings at any point you can sneak a look
ahead to the code in exercise 7.

You can refer to the [numpydoc documentation](https://numpydoc.readthedocs.io/en/latest/format.html)
for examples of any types/structures you are unsure about.

Run ruff with pydocstyle on the code for guidance and to check your docstrings.

```bash
ruff check precipitation_climatology.py
```


## Other languages

The examples discussed here so far have been for Python docstrings.
Other languages follow similar principles, though the 'syntax' may be slightly
different.

Here are a few examples for other languages:

Fortran - [FORD](https://forddocs.readthedocs.io/en/stable/) or [doxygen](https://www.doxygen.nl/index.html):
```fortran
subroutine add(a, b, sum)
    !! Add two integers.

    integer, intent(in) :: a     !! First number, a
    integer, intent(in) :: b     !! Second number, b
    integer, intent(out) :: sum  !! Sum of a and b

    sum = a + b
end subroutine add
```

Julia - [triple quoted docstrings](https://docs.julialang.org/en/v1/)
```julia
"""
    add(a,b)

Add two numbers `a` and `b`.

# Arguments
- `a::Number`: The first number.
- `b::Number`: The second number.

# Returns
- `Number`: The sum of `a` and `b`.
"""
function add(a::Number, b::Number)::Number
    return a + b
end
```

C/C++ - [doxygen](https://www.doxygen.nl/index.html):
```c
/**
 * Add two integers.
 * @param a, First integer.
 * @param b, Second integer.
 * @return Sum of a and b.
 */
int add(int a, int b) {
    return a + b;
}
```

R - [roxygen2](https://roxygen2.r-lib.org/):
```r
#' Add two numbers.
#'
#' @param a First number.
#' @param b Second number.
#' @return Sum of `a` and `b`.
add <- function(a, b) {
    return(a + b)
}
```

Rust - [rustdoc](https://doc.rust-lang.org/rustdoc/):
```rust
/// Adds two integers `a` and `b`.
///
/// Returns an `i32` that is the sum of the inputs.
///
/// # Examples
///
/// ```
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
fn add(a: i32, b: i32) -> i32 {
    a + b
}
