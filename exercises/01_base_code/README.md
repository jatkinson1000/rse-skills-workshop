# Exercise 1 - Setup and virtual environments

## First impressions

Take a look at the files in this folder and open the code in your preferred text editor

Note the requirements at the top of the script.

## Virtual environment

Set up a virtual environment and activate it.\
Note: _It may be useful to do this a couple of directories higher under `/` or
`/exercises/`._

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

You can now install the required dependencies using pip:

```bash
pip install numpy matplotlib ...
```

## Run the code

Once the dependencies are installed run the code:

```
python3 precipitation_climatology.py
```

Does everything work as you expected or are there some unexpected dependencies required
e.g. `netcdf4`? We will come back to this issue later in the course.

Once you have run the code take a moment to inspect the outputs.\
Does it do what you were expecting it to?

## Finishing

You can now move on to exercise two in the adjacent folder.\
Keep your virtual environment active as you will be re-using it!
