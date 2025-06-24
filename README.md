# Research Software Engineering Skills Workshop

![GitLab License](https://img.shields.io/gitlab/license/jatkinson1000%2Frse-skills-workshop)

Materials for a workshop educating academic researchers in research software
engineering (RSE) principles.
The example code used in the exercises is geared towards climate scientists,
but the concepts and material is generally suited for people from various backgrounds.

This course is designed to be delivered as a code-along workshop, but you can also follow
the slides and work through the exercises in your own time.


## Contents

- [Learning Objectives](#learning-objectives)
- [Materials](#materials)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contribution Guidelines](#contribution-guidelines)


## Learning Objectives

The key learning objective for the workshop is to _Introduce key tools and concepts of
research software engineering, and how they can be applied in everyday use to write
higher-quality code_.

More specifically we cover:

- Why software engineering principles matter in research
- (Virtual) environments and dependencies
- Code standards and best practice (through PEP)
  - Code formatters and linting/static-analysis tools
- Documentation
  - Docstrings
  - Advice on commenting
  - The idea of self-documenting code and variable naming
  - Handling magic numbers in code
  - READMEs and other useful files in your repository
  - Software licenses
- General principles for better code
  - Removal of hard-coded content to config files
  - Use of f-strings in Python (optional addition)
  - Improving readability and reusability through better code structure


## Materials

### Slides

The main slide deck for the workshop can be viewed [here](https://jatkinson1000.github.io/rse-skills-workshop).
They are generated from the Quarto materials in the `slides/` directory.
They are broken into separate sections covering the different topics in the workshop.
The modular structure makes the course adaptable, as sections can be included or excluded from the slide deck.

### Exercises

A series of practical exercises accompany the teaching material in the slides.
These are contained in the `exercises/` directory in a series of sub-directories,
each of which has instructions in a README.

The code used as the starting point for each exercise is the 'solution' to the
previous exercise allowing participants to validate/compare their work.

- 01: Base code to examine.
- 02: Apply a formatter to standardise code.
- 03: Linting and static analysis of code.
- 04: Code structure.
- 05: Improve code clarity with naming and removing magic numbers.
- 06: Writing docstrings and best use of comments.
- 07: General techniques for better code.
- 00: The end point of the workshop - an improved version of the code in exercise 01.


## Prerequisites

In terms of knowledge this workshop requires:

- Some general programming knowledge
- Basic familiarity with Python - the course is taught in Python but teaches skills that are transferrable to other languages.
- The ability to clone this repository and work on it locally.

Python and pip:

- A working installation of Python 3.
  This should come as standard on linux and can be installed on mac and Windows.
- A working installation of pip for installing Python packages.
  Often this will come with Python, but some operating systems/distributions disable it.
  If `pip` is not available on the command line you can add it to a virtual environment
  ([see below](#virtual-environment-setup)) using `python -m ensurepip --upgrade`

> [!NOTE]
> For macOS users: Python 3 can be installed through several popular package managers.
> Alternatively, if you are unfamiliar with this, refer to
> [Python's getting-started on mac information](https://docs.python.org/3/using/mac.html)
> for a complete guide to getting set up.

> [!NOTE]
> For Windows users: you may wish to refer to
> [Windows' getting-started with Python information](https://learn.microsoft.com/en-us/windows/python/beginners)
> for a complete guide to getting set up on a Windows system.

Participants will also be expected to have:

- A text editor to open and edit code files.\
   e.g. vim/[neovim](https://neovim.io/), [gedit](https://gedit.en.softonic.com/), [VS code](https://code.visualstudio.com/), [sublimetext](https://www.sublimetext.com/) etc.
- A terminal emulator to run the code.\
  e.g. [GNOME Terminal](https://help.gnome.org/users/gnome-terminal/stable/), [wezterm](https://wezfurlong.org/wezterm/index.html), [Windows Terminal (windows only)](https://learn.microsoft.com/en-us/windows/terminal/), [iTerm (mac only)](https://iterm2.com/) etc.
- The two of these may be combined in a single IDE e.g. PyCharm, VS Code, IntelliJ IDEA etc.


## Setup

### Cloning the materials

Cloning the repository and setting up a virtual environment will be covered in the course,
but in preparation you can complete these steps as follows:

Navigate to the location you want to install this repository on your system and clone
via https by running:
```
git clone https://github.com/jatkinson1000/rse-skills-workshop.git
```
This will create a directory `rse-skills-workshop/` with the contents of this repository.

Please note that if you have a GitHub account and want to preserve any work you do
we suggest you first [fork the repository](https://github.com/Cambridge-ICCS/rse-skills-workshop/fork) 
and then clone your fork.
This will allow you to push your changes and progress from the workshop back up to your
fork for future reference.

If you would prefer to do this from GitHub you can use the [GitHub mirror](https://gitlab.com/jatkinson1000/rse-skills-workshop).

### Virtual environment setup

You can then instantiate a Python virtual environment by running:
```
python3 -m venv rse-venv
```
This will create a directory called `rse-venv` containing software for the virtual environment.
To activate the environment run:
```
source rse-venv/bin/activate
```
You can now work on Python from within this isolated environment, installing packages
as you wish without disturbing your base system environment.

When you have finished working on this project run:
```
deactivate
```
to deactivate the venv and return to the system Python environment.

You can always boot back into the venv as you left it by running the activate command again.


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


## Contribution Guidelines

Contributions and collaborations are welcome from anyone with an
interest in RSE education.

For bugs, feature requests, and clear suggestions for improvement please
[open an issue](https://gitlab.com/jatkinson1000/rse-skills-workshop/-/issues).

If you built something upon this that would be useful to others, or can
address an [open issue](https://gitlab.com/jatkinson1000/rse-skills-workshop/-/issues),
please [fork the repository](https://gitlab.com/jatkinson1000/rse-skills-workshop/-/forks/new)
and open a merge request.
If you wish to contribute a new exercise you think would be useful please follow the
existing format in [exercises/](exercises/), and also try and update the slides in
[slides/](slides/).


### A note on mirrors

This repository exists mainly as a
[GitLab repository](https://gitlab.com/jatkinson1000/rse-skills-workshop)
with a [mirror on GitHub](https://github.com/jatkinson1000/rse-skills-workshop).\
Please try to open issues and contributions on GitLab.


### Code of Conduct

Everyone participating in this project, including as a participant at a workshop,
is expected to treat other people with respect and more generally to follow
the guidelines articulated in the
[Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).
