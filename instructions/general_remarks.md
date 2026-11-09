# Jupyter notebook options for our lectures  
 What you need to know if you want to expand/modify slide notebooks

### Which purposes do the notebooks serve?
- providing slides during the lecture (including speaker notes)
- providing the basis for book creation for the students

### Which relevant cell types are there?
- Code
- Markdown

### Which relevant view are there?
 (accessible via View/Cell Toolbar)
- Slideshow  
- Hide code
- Tags


### What can be controlled by the different views?
- Slideshow (relevant for **slide show and markdown** cells only)
  - Slide (begin of a new slide)
  - Fragment (allows to enter a sub slide during the lecture)
  - Skip (if this markdown cell should not be shown)
  - Notes (to show this markdown cell in the speaker notes only)
  - `-` (to continue the previous cell) (?)
- Hide code (relevant for **slide show and code cells** only)
  - Hide promt
  - Hide code
  - Hide output
- Tags (relevant for **book output** only)
  - `remove-cell`(removes the entire cell from the book)
  - `remove-input` (removes input of a code cell from the book)
  - use the `Add tag` button to create those tags manually

### In a nutshell
In general, all cells will be used for the slide show and the book.  
If a slide should be skipped
- during the slide show:
  - select *Slideshow* view / Skip to skip a complete markdown cell
  - select *Hide code* view / select the options to skip (parts of) a code cell
- in the book:
  - select *Tags* view and add the *remove-cell* tag to remove the entire cell from the book
  - select *Tags* view and add the *remove-input* tag to remove the input from the book

### Further things to know
- Speaker notes view can be started by hitting `t`. Sometimes this works only after starting the slide show.
- There is unfortunately no shortcut to switch between the views during editing.
- If jupyter swallows, run the complete notebook or even restart it again. (Still does not help everytime)


### What about html in some markdown cells?
- Correctly set html tags are relevant for the slide show only.
- Incorrectly set html tags can destroy the book.
- If you are familar with css: Have a look at `rice.css` for class definitions.
 Some important ones:
  - `<div class="text_70">` use the left 70% of the space
  - `<div class="images_30">` use the right 30% of the space
