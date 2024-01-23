## Slides

This directory contains the slides for the workshop.

The slides are written in Markdown and presented in the reveal.js format being
generated using [Quarto](https://quarto.org/).


#### Generating slides

To build them install Quarto and then run, from this directory:
```bash
quarto render python.qmd
```
to generate `python.html` which can be viewed in any browser.


#### Editing slides

To edit the slides please see the contents of `python.qmd` which is a Quarto Markdown
file.

Images are placed in `/images/` and BibTeX references are in `references.bib`.
