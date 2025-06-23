# Exercise 4 - Code Structure

This exercise is intended to practice spotting where code can be structured, how
this improves readability and reusability, and how that in turn enables using
code as building block to enable advanced functionality.

## Functions and further code structuring

Introduce function to
- avoid code duplication (bad style, and you will forget to update all the copies at one point when you make changes!),
- improve readability (a clearly named function replaces a chunk of code),
- and use them as building blocks (create a generic interface with several exchangeable options)

Break code into modules and files instead of having everything in one file. This improves readability and manageability (particularly as the code base grows), makes it easier to extend and test the code, as well as to provide interfaces for coupling with other codes.  

See also [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) and [single responsibility principle](https://en.wikipedia.org/wiki/Single-responsibility_principle).


## Inspect and change the example code

Look at the code in the `plotting.py` file and identify duplicated code blocks as well as other code
snippets that could be moved into separate functions to increase readability and
reusability. Make those changes and experiment with the code -- what can you now
easily do?

## Inspect the changes

Look at the newly structured file and note the changes.

- Is it more readable?
- How does the new structure enables easier reuse of code blocks? What can this
enable you to do?
 - Now look at `plotting_solution.py` . Can you further adapt the code to allow, for example, for customised axis labels?
