---
title: 'Research Software Engineering Skills'
tags:
  - Software Engineering
  - Python
  - Research Software
authors:
  - name: Jack Atkinson
    orcid: 0000-0001-5001-4812
    affiliation: "1"
    corresponding: true
  - name: Amy Pike
    affiliation: "1"
    orcid: 0009-0007-7278-4122
  - name: Marion Weinzierl
    affiliation: "1"
    orcid: 0000-0002-2302-5476
affiliations:
 - name: Institute of Computing for Climate Science, University of Cambridge, UK
   index: 1
date: 29 July 2024
bibliography: paper.bib

---

# Summary

Research across many domains increasingly relies on software for simulation,
data processing, analysis, visualisation, and more.
This software is often written by individuals without a formal training in software engineering
leading to inefficiencies, bugs, and poor reproducibility/reuseability.

The course described in this paper is designed to raise awareness software
engineering principles and how they can be applied to research code.
It illustrates, through a series of practical exercises, why these are important and
introduced basic techniques to produce FAIR-er code [@barker2022introducing].
We hope that introducing a software engineering mindset, with simple tools and techniques
to facilitate this will have long-term impact with participants continuing to explore
ideas in their future work beyond this course.



# Statement of need

Software forms a significant part of research today, with much of it being written and developed
by academic researchers. Many of these individuals are self-taught or have minimal training,
which will often focus on 'coding' rather than software development.
As a result there is often a lack of awareness of software development principles
amongst academic developers leading to software that is hard to use and maintain,
presenting a barrier to research.

In our experience working with academic developers many of the bad practices and
antipatterns are a result of them:

- learning on the job from old code and emulating habits they observe
- never having been made aware of the available tools and techniques
- not keeping up to date with language/package developments
- not investing time into writing good code, often due to placing priorities elsewhere.

The intent of developing this short course, _RSE Skills (in Python)_, is to educate
individuals in some basic software engineering principles that they can carry forward
in their work.
It is designed to introduce key tools and techniques to facilitate the writing of
better code, but also to raise awareness of research software engineering and provide pointers
to allow researchers to continue exploring and learning beyond this material.



# Learning objectives

The key learning objective for the workshop is to _Introduce key tools and concepts of
research software engineering, and how they can be applied in everyday use to write
higher-quality code_.

More specifically we cover:

* Why software engineering principles matter
* (Virtual) environments and dependencies
* Code standards and best practice (through PEP)
  * Code formatters and linting/static-analysis tools
* Documentation
  * Docstrings
  * Advice on commenting
  * The idea of self-documenting code and variable naming
  * READMEs and other useful files in your repository
  * Software licenses
* General principles for better code
  * Magic Numbers
  * Removal of hard-coded content to config files
  * use of f-strings in Python.



# Teaching materials

All of the teaching materials for this course are available online in a GitHub repository.


## Slides

All of the key material is contained in a slide deck for the course available online
and linked from the repository README.
The slides are written in [Quarto](https://quarto.org/) markdown [@Allaire_Quarto_2022]
and rendered as [reveal.js](https://revealjs.com/) html.
Source and instructions on how to render are included in the repository should
others wish to tailor them to their specifications.

The slides are broken into separate files by section covering:

- Introduction to research software engineering, why it matters, and some examples,
- The use of virtual environments and specifying project dependencies,
- Code formatting for consistent readable layout,
- Naming principles for readable, re-useable code,
- Linting and static analysis of code,
- Writing docstrings and comments, and
- Other general principles including magic numbers, avoiding hardcoded values, etc.

This makes it easy to remove sections to tailor the course, or for additional topics to be added in future.

## Exercises

The slides are interspersed with a series of exercises, each one applying techniques
that have just been taught.

We set up a scenario where users have been provided a working, but poorly written piece
of code that they are now expected to re-use in their work.
As they progress through the exercises they apply their new skills to transform this
into a much more readable and understandable piece of code.

The script we use is based on some of the code and data available in @Irving2019.
This was chosen as it features typical applications we expect users to encounter
(reading from a dataset, processing, and plotting).
The course was originally designed to be taught to geoscientists, and then at a climate
science summer school, and we wanted participants to be focussed on the changes to the
code rather than worrying about the application or semantics.

Exercises roughly match the slide sections above:

- 01: Baseline code to examine, install dependencies, and run.\
  Users can familiarise themselves with what the code does, see why listing dependencies
  with a quick setup is useful, and make early observations about how the code is
  difficult to understand/use.
- 02: Apply a formatter to standardise code.\
  We use the black python formatter [@LangaBlack]
- 03: Improve code clarity with naming and source changes.
- 04: Linting and static analysis of code.
- 05: Writing docstrings and best use of comments.
- 06: General techniques for better code (magic numbers, string formatting).
- 00: The end point of the workshop - an improved version of the code in exercise 01.

Each exercises builds upon the results of the previous one, allowing participants to
apply what they are learning in a continuous fashion to a code.
However, each exercise has a dedicated subdirectory meaning that success in a previous
exercise is not a pre-requisite for continuing to the next one.
Two additional benefits to this approach are that the starting point for a subsequent
exercise can be viewed as the solution to the current one, allowing participants to
compare their work to an 'ideal' solution, and that exercises can easily be removed to
tailor the course to different emphasis or time constraints.



# Content Delivery

The course has been designed to be flexible in terms of delivery, allowing
it to be adapted to and reused in various setups.

The slides are interspersed with the exercises, rather than separate from the presentation material, as the exercises are an integral component of the course.

The main aspect we wish to emphasise in delivery is teaching in a _"code-along"_ fashion.
This helps with engagement, participation, and understanding [@barba2022teaching] and
is essential, we feel, to having a long-lasting benefit [@rubin2013effectiveness].
This approach slows those leading the course towards the rate at which the participants
are working, and illustrates through errors (whether intentional or not!) that even
experienced coders are human and make mistakes.
Such errors can illustrate common pitfalls and provide an opportunity to include
the teaching of debugging approaches.
More generally this approach helps emphasise RSE principles, as participants can
see the live application of these ideas in practise.

We also believe that there is sufficient guidance in the slides and repository
documentation to follow the course alone, and we include a link to a recording of
the workshop.
This is, however, no substitute to in-person delivery where participants can ask
questions, and successive workshops are continually improving.



# Teaching experience

One aspect of the material we have found useful is the ability to tailor the course to
the workshop/audience.
By breaking the slides into separate files by section and having standalone exercises
for each section it is easy to add or remove material as desired.

As discussed in the introduction, the course is written in Python for the broadest appeal,
but is intended to educate researchers more generally on software engineering principles.
We found it useful during delivery to reference tools and techniques applicable for
other languages and systems as we went along.
For example, where we introduce environment and dependency management in Python using
virtual environments, we also mention spack as an analagous approach for those using HPC
environments.
We also discuss other language specific tools for formatting and linting/static analysis
such as `clang-format` for C++.
We feel that this is important to help participants see past the python specifics and
understand the broader ideas and how they can be deployed in their own projects.

TODO IDE and vimdiff

The content can be easily changed to be domain specific in another area, simply by choosing a different example for the exercises.

We have also adapted a modular design for the course material -- using Markdown with Quarto, to allow easy inclusion and exlusion of individual sections included in the main document. A similar modular design would be possible, for example, with Latex. This means that the content can be adapt

Finally, we encourage participants to feed experiences back into the project, either via
a GitHub issue or pull request.
This allows us to continually learn from delivery and improve the material for future
participants, especially if making instructions clearer or providing solutions
to previously unencountered problems.



# Acknowledgments

We thank anyone who has made a contribution to these materials, however small,
assisted in code review for us, or helped as demonstrators on the course.

The [Institute of Computing for Climate Science](https://iccs.cam.ac.uk/)
received support through [Schmidt Sciences](https://www.schmidtsciences.org/).



# References
