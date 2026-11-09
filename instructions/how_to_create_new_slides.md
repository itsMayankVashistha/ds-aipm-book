# Creating new slides with the rise extension

More to come...


## Curiosities that need your attention

Since we are using the same jupyter notebook for our slides and the respective site in the jupyter book there are some things we need to take special care of. 

### Title slides

We style the title slides for our presentations by creating a cell with the following content:

```css
<div class="slide-title">

# Linear Regression (or whatever)

</div>
```
Unfortunately, using those html tags breaks the layout of the rendered jupyter book. Therefore, we need to remove this cell from the book by adding a `remove-cell` tag to it. In order to still have a proper title for the jupyter book page, another cell with the same title but without the html needs to be added. To not show up in the slide show, this cell should be skipped.

**_NOTE:_** In order to change the background color of the title slide it was necessary to put it in dependence of the slide number. This means even if the .slide_title class is not called, the background color will still be orange/pink. In order to change that you would need a new css file with the notebooks name with the following content:
``` 
.reveal .slides > section:nth-child(1) {
    background-color: white;
}
```


## Charts and Diagrams

For flowcharts, class diagrams, gitgraph diagrams, mindmaps and timelines you can use [mermaid.js](https://mermaid.js.org/). You can use either the [live editor](https://mermaid.live/edit) or set mermaid up in VS Code to create your own chart. To implement your chart in the notebooks you need to import the following function:
```python
from auxiliary_functions import chart
```
Now you can give your code as a string to this function and you will get your chart as a plot output. Don't forget to hide your code.
```python
chart("""
flowchart TD
    A(Training Set) --> B(Model 1 
    fa:fa-cogs) --Test--> F(( 1 )) --> J{Voting} --> K((1))
    A --> C(Model 2
    fa:fa-cogs) --Test Set--> G(( 0 )) --> J
    A --> D(Model 3 
    fa:fa-cogs) --Test Set--> H(( 1 )) --> J
    A --> E(Model 4
    fa:fa-cogs) --Test Set--> I(( 1 )) --> J
    subgraph "Ensemble"
        B
        C
        D
        E
    end
""")
```
The color scheme will be set automatically according to your theme setting in the plot_colors.json file.


## Checklist before you are done

- [ ] Add `remove-cell` tag to...
    * the title slide of the lecture, which is styled with the `class=slide-title`
    * all the speaker notes (Cells with speaker notes always start with `Notes:`)
    * all code cells at the beginning of the notebooks
    * all to break slides 
- [ ] Add `remove-input` tag to every code cell in the lecture (e.g. code cells with function calls producing plots)
- [ ] Check if there is an additional heading for the jupyter book (without html/css)
- [ ] Make sure all the `<div>` opening tags are also closed and there are no redundant closing tags.