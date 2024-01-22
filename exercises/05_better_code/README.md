# Exercise 5 - Better Code

This exercise contains the code now complete with docstrings.


## Magic Numbers

Look through the code and try and identify any magic numbers.\
For any that you find implement what you feel is best approach for dealing with them
in each case?


## f-strings

Look through the code for any string handling (currently using the `.format()` approach)
and update it to an f-string format.\
Is the intent clearer?\
Is the layout of the data written to file easier to understand?


## Configuration settings

The original author of the code has helpfully put a list of the configurable
inputs at the end of the file under `"__main__"`.
We can improve on this, however, by placing them in a configuration file.

Create an appropriate `json` file to be read in as a dictionary and passed to the 
main function.


## Extension exercises

- Make it possible to specify the input filename at runtime using
  ```python
  input("Enter configuration filename: ")
  ```
- Extend the `input()` approach to use
  [argparse](https://docs.python.org/3/library/argparse.html).
