# Data Science Course Material

This repository is a template repo and contains a collection of all the data science course slides and RATs. 

If you are new to the project you can find helpful information in the [instructions](instructions) folder. You might want to have a look there if you ask yourself...

* [How do I use jupyter slides with the rise extension?](instructions/how_to_use_slides.md)
* [How do I create a new jupyter slide deck?](instructions/how_to_create_new_slides.md)
* [How do I create the orientation slides automatically?](instructions/how_to_create_orientation_slides.md)
* [How do I set the color scheme for spiced respectively neuefische?](instructions/how_to_set_the_color_scheme.md)


This README contains some general information which will help you to setup a new repository for your bootcamp.

- [Data Science Course Material](#data-science-course-material)
  - [How to use this repo](#how-to-use-this-repo)
    - [Step by step instructions](#step-by-step-instructions)
    - [Setup](#setup)
    - [Enable Scrolling](#enable-scrolling)
    - [Having slides top aligned instead of centered](#having-slides-top-aligned-instead-of-centered)
  - [Deploying the book with gh-pages](#deploying-the-book-with-gh-pages)
  - [Creating the Jupyter Book locally](#creating-the-jupyter-book-locally)
  - [TOC Automation](#toc-automation)


## How to use this repo
Create a new repository for each Bootcamp by using the **template** button in the upper right corner. The main branch of this repository contains all the necessary lecture material and rapid assessment tests. By successively updating the [_toc.yml](DSBOOK/_toc.yml) file the lectures and RATs can be added to the jupyter book. 

### Step by step instructions
1. Create new repo by using template button. Name it "`<cohort-name>`-book".
2. Select the company color scheme for the slides and jupyter book ([see here for more detailed instructions](instructions/how_to_set_the_color_scheme.md))
3. Deploy jupyter book with Github pages ([see here](#deploying-the-book-with-gh-pages)) and bookmark link in course Slack channel
4. Setup virtual environment and use Jupyter Notebook to present slides in [sessions](DSBOOK/sessions/) folder.
   1. There is an `aipm_sessions` folder inside the `sessions` folder which contains AIPM lectures
5. Update [_toc.yml](DSBOOK/_toc.yml) file each day by uncommenting the respective lines for lectures and RATs
   1. Updating [_toc.yml](DSBOOK/_toc.yml) file now works automatically with respect to the calendar events of the cohort. See [toc-automation.md](toc-automation.md)
   2. RATs are now provided as quizzes (see [ds-quizzes-flashcards-template](https://github.com/neuefische/ds-quizzes-flashcards-template) repo). So no need to uncomment RATs

### Setup

After creating a new repository for a Bootcamp you can setup the virtual environment.

>Requirements:
>- [uv](https://docs.astral.sh/uv/getting-started/installation/) 
>- jupyter notebook < 7 (version 7 and later will break our extensions!) this is pinned for you in `pyproject.toml`

`uv sync` reads `pyproject.toml` / `uv.lock` and creates the `.venv` with the exact pinned
package versions (uv also downloads a matching Python 3.11 automatically, so no `pyenv` needed):

```bash
uv sync
```

Then enable the `hide-code` notebook extension once (this step can't be part of `uv sync`
because it modifies your local Jupyter config, not the environment):

```bash
uv run jupyter nbextension install --py --user hide_code
uv run jupyter nbextension enable  --py --user hide_code
uv run jupyter serverextension enable --py --user hide_code
```

Start the slides with `uv run jupyter notebook`.


### Enable Scrolling

Scrolling on slides needs to be enabled locally. In order to do so, use the following commands:

```bash
touch ~/.jupyter/nbconfig/livereveal.json # creates new file
echo '{"scroll": true}' > ~/.jupyter/nbconfig/livereveal.json # adds necessary content
```

### Having slides top aligned instead of centered

Slides alignment needs to be configured locally. In order to do so, use the following command:
```bash
touch ~/.jupyter/nbconfig/rise.json # creates new file
echo '{"center": false}' > ~/.jupyter/nbconfig/rise.json # adds necessary content
```


## Deploying the book with gh-pages 

In order to deploy the book with gh-pages, you'll need to go to the settings of the repository. Click on `Pages`. Make sure source is set to `Deploy from branch` and select in the dropdown menu for branch `gh-pages`. It might take a few minutes, till the url to the deployed jupyter book will be shown here. When merging a pull request the github page will be updated automatically. 

![deploy book](images/deploy_book.png)

## Creating the Jupyter Book locally

If you want to see a preview of the jupyter book locally you can create the html file with the following commands:

```bash
rm -rf DSBOOK/_build                        # 1. wipe the old/incremental build
uv run jupyter-book build DSBOOK            # 2. full clean rebuild
cp -r DSBOOK/images DSBOOK/_build/html/     # 3. copy the untracked images into the output
```

If you want to re-build the book locally, Jupyter Book will only build the HTML for pages that have been updated since the last time you built the book. You can use the following to force a full re-build:

```bash
rm -rf DSBOOK/_build                        # 1. wipe the old/incremental build
uv run jupyter-book build --all DSBOOK      # 2. full clean rebuild
cp -r DSBOOK/images DSBOOK/_build/html/     # 3. copy the untracked images into the output
```

After building the book you will get the information on where to find the rendered html in the terminal and can view it by opening the link in a browser.

---
## TOC Automation

Instead of manually uncommenting lines in [_toc.yml](DSBOOK/_toc.yml) each day, a scheduled GitHub Action can reveal each session automatically based on the cohort's Google Calendar. See [toc-automation.md](toc-automation.md) for how it works and the one-time setup.

