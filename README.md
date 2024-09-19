# Research Software Engineering Skills Workshop

![GitLab License](https://img.shields.io/gitlab/license/jatkinson1000%2Fpower-up-python)

Materials for a workshop educating academic researchers in research software
engineering (RSE) principles.
The example code used in the exercises is geared towards climate scientists,
but the concepts and material is generally suited for people from various backgrounds.

This course is designed to be delivered as a code-along workshop, but you can also follow
the slides and work through the exercises in your own time.


### A note on mirrors

This repository exists mainly as a
[GitLab repository](https://gitlab.com/jatkinson1000/rse-skills-workshop)
with a [mirror on GitHub](https://github.com/jatkinson1000/rse-skills-workshop).\
Please try to open issues and contributions on GitLab.


## Learning Objectives

The key learning objective for the workshop is to _Introduce key tools and concepts of
research software engineering, and how they can be applied in everyday use to write
higher-quality code_.

More specifically we cover:

- Why software engineering principles matter
- (Virtual) environments and dependencies
- Code standards and best practice (through PEP)
  - Code formatters and linting/static-analysis tools
- Documentation
  - Docstrings
  - Advice on commenting
  - The idea of self-documenting code and variable naming
- General principles for better code
  - Magic Numbers
  - Removal of hard-coded content to config files
  - use of f-strings in Python.


## Prerequisites

In terms of knowledge this workshop requires:

- Some general programming knowledge
- Basic familiarity with Python - the course is taught in python but teaches skills that are transferrable to other languages.
- The ability to clone this repository and work on it locally.

Participants will be expected to have:

- A text editor to open and edit code files.\
   e.g. vim/[neovim](https://neovim.io/), [gedit](https://gedit.en.softonic.com/), [VS code](https://code.visualstudio.com/), [sublimetext](https://www.sublimetext.com/) etc.
- A terminal emulator to run the code.\
  e.g. [GNOME Terminal](https://help.gnome.org/users/gnome-terminal/stable/), [wezterm](https://wezfurlong.org/wezterm/index.html), [Windows Terminal (windows only)](https://learn.microsoft.com/en-us/windows/terminal/), [iTerm (mac only)](https://iterm2.com/) etc.
- The two of these may be combined in a single IDE e.g. PyCharm, VS Code, IntelliJ IDEA etc.

Note for Windows users: _We have linked suitable applications for windows in the above lists.
However, you may wish to refer to [Windows' getting-started with python information](https://learn.microsoft.com/en-us/windows/python/beginners)
for a complete guide to getting set up on a Windows system._


## Setup

Cloning the repository and setting up a virtual environment will be covered in the course,
but in preparation you can complete these steps as follows:

Navigate to the location you want to install this repository on your system and clone
via https by running:
```
git clone https://gitlab.com/jatkinson1000/rse-skills-workshop.git
```
This will create a directory `rse-skills-workshop/` with the contents of this repository.

Please note that if you have a GitLab account and want to preserve any work you do
we suggest you first [fork the repository](https://github.com/Cambridge-ICCS/practical-ml-with-pytorch/fork) 
and then clone your fork.
This will allow you to push your changes and progress from the workshop back up to your
fork for future reference.
If you would prefer to do this from GitHub you can use the [GitHub mirror](https://github.com/jatkinson1000/rse-skills-workshop).

You can then instantiate a python virtual environment by running:
```
python3 -m venv myvenv
```
This will create a directory called `myvenv` containing software for the virtual environment.
To activate the environment run:
```
source myvenv/bin/activate
```
You can now work on python from within this isolated environment, installing packages
as you wish without disturbing your base system environment.

When you have finished working on this project run:
```
deactivate
```
to deactivate the venv and return to the system python environment.

You can always boot back into the venv as you left it by running the activate command again.


## Exercises

A series of practical exercises accompany the teaching material in the slides.
These are contained in the `exercises/` directory in a series of sub-directories,
each of which has instructions in a README.

The code used as the starting point for each exercise is a 'solution' to the
previous exercise allowing participants to validate/compare their work.

- 01: Base code to examine.
- 02: Apply a formatter to standardise code.
- 03: Improve code clarity with naming and source changes.
- 04: Linting and static analysis of code.
- 05: Writing docstrings and best use of comments.
- 06: General techniques for better code (magic numbers, string formatting).
- 00: The end point of the workshop - an improved version of the code in exercise 01.


## License

Copyright &copy; Jack Atkinson

Unless otherwise noted the programs and other software provided in this repository are
made available under an [OSI](https://opensource.org/)-approved
[GPL-3.0-only](https://opensource.org/license/gpl-3-0/) license.

Unless otherwise noted the teaching materials provided in this repository are
made available under a Creative Commons [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
license for which the full legal text is [available online](https://creativecommons.org/licenses/by/4.0/legalcode).


## Acknowledgments

The code used in this teaching is adapted from a script in\
Irving, (2019). Python for Atmosphere and Ocean Scientists.
Journal of Open Source Education, 2(11), 37,
[doi.org/10.21105/jose.00037](https://doi.org/10.21105/jose.00037)


## Contributions

Contributions and collaborations are welcome from anyone with an
interest in RSE education.

For bugs, feature requests, and clear suggestions for improvement please
[open an issue](https://gitlab.com/jatkinson1000/power-up-python/-/issues).

If you built something upon this that would be useful to others, or can
address an [open issue](https://gitlab.com/jatkinson1000/power-up-python/-/issues),
please [fork the repository](https://gitlab.com/jatkinson1000/power-up-python/-/forks/new)
and open a merge request.
If you wish to contribute a new exercise you think would be useful please follow the
existing format in [exercises/](exercises/), and also try and update the slides in
[slides/](slides/).


### Code of Conduct

Everyone participating in this project, including as a participant at a workshop,
is expected to treat other people with respect and more generally to follow
the guidelines articulated in the
[Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).
