# Exercise 1 - Setup and virtual environments

Software environments are an important concept in development and deployment.
They allow us to:

- Control dependencies
- Avoid system pollution through isolation
- Allow different versions for different projects
- Facilitate reproducibility - set specific versions

For more information see the
[Real Python article](https://realpython.com/python-virtual-environments-a-primer/)
on virtual environments.


## First impressions

Take a look at the files in this folder, opening the code in your preferred text editor.

Note the package imports at the top of the script.


## Virtual environments

Python has inbuilt support for creating isolated virtual environments through
[`venv`](https://docs.python.org/3/library/venv.html).

Set up a virtual environment and activate it:

> [!NOTE]
> It may be useful to place this a couple of directories higher under `/` or
> `/exercises/` as it will be used for all exercises in the workshop.

Unix/macOS:
```bash
python3 -m venv rse-venv
source rse-venv/bin/activate
```
Windows Powershell:
```powershell
python -m venv rse-venv
rse-venv\Scripts\Activate.ps1
```
Windows cmd.exe
```shell
python -m venv rse-venv
rse-venv\Scripts\activate.bat
```

You will see that your command prompt is now preceded by `(rse-venv)` indicating
that you are working in the virtual environment.

To deactivate the environment use the `deactivate` command.
You can always re-enter it later by running the activate script again.

You will see that a directory `rse-venv/` has been created into which pip will install
packages.
To remove the venv (and any installed packages) we delete this directory with
`rm -r rse-venv` on Unix, or `rmdir /s rse-venv` on Windows.


## Installing dependencies

### Manually

You can now install the required dependencies into this environment using pip:

```bash
pip install numpy matplotlib ...
```
Once the dependencies are installed try to run the code:

```bash
python3 precipitation_climatology.py
```

Does everything work as you expected or are there some unexpected dependencies required
e.g. `netcdf4`?

### From a requirements file

Installing dependencies manually one-at-a-time is tedious and a process of
trial-and-error.

Instead the author of the software should provide a list of all the dependencies
required for running their code.
In Python this is often done in a `requirements.txt` file that can be installed in
one go:

```bash
pip install -r requirements.txt
```


## Running the code

You can now run the code from the command line using:

```
python3 precipitation_climatology.py
```

Once you have done this take a moment to inspect the outputs.
Did it do what you were expecting it to based on reading it beforehand?


## Finishing

You can now move on to exercise two in the adjacent folder.
Keep your virtual environment active as you will be re-using it!


## Other languages

There are various other tools available to manage environments and dependencies in
other languages:

- Python and more - conda
- C, C++, Fortran:
  - Module environments
  - Spack
- Rust - cargo
- Julia - Pkg environments
- R - renv


## Further reading

Providing a list of dependencies (e.g. `requirements.txt` file) should be a bare
minimum when distributing software.

As a project grows it is better to look at proper _software packaging_ to make your code
easy for users to install, robust and reproducible, and portable to different systems.
This is beyond the scope of today's workshop, however.

You can read about packaging for Python in the
[Python Packaging User Guide](https://packaging.python.org).
This enables the project to be installed via pip, and can be achieved for simple
projects by the inclusion of a `pyproject.toml` file.

For other languages/projects there are a variety of packaging tools designed to help
streamline the packaging and distribution process.
