# Selecting a company color scheme

Every color scheme we defined in the course of this project is available in neuefische and spiced colors. This includes the...

* slide background and heading colors defined in the [rise.css](../DSBOOK/sessions/rise.css) file
* Jupyter Book colors defined in the [custom.css](../DSBOOK/_static/custom.css) file
* RAT question colors defined in the [RATs](../DSBOOK/RATs/) folder
* plot colors used in the notebooks defined in the [sessions](../DSBOOK/sessions/) folder

   
## Setting a color scheme   

After forking the repository for a new bootcamp, make sure to edit/rename the following files:

1. **Slide colors:** \
Edit the [rise.css](../DSBOOK/sessions/rise.css) file. Per default it uses the neuefische color scheme. If you want to change it to spiced remove the neuefische part at the beginning of the file and uncomment the part where the spiced colors are defined (starting with `:root{...}`).
2. **Jupyter Book colors:** \
Edit the [custom.css](../DSBOOK/_static/custom.css) file. Similar to the slides styling it uses the neuefische colors as default. If you want to change it to spiced remove the neuefische part and uncomment the part where the spiced colors are defined (starting with `:root{...}`).
3. **RAT colors:** \
The RAT colors are defined in two json files in the [RATs](../DSBOOK/RATs/) folder. Assuming you want to use the spiced color scheme, delete the file called `colors_nf.json` and rename the spiced file to `RAT_colors.json`.
4. **Plot colors:** \
The plot colors are defined in two json files in the [sessions](../DSBOOK/sessions/) folder. Assuming you want to use the spiced color scheme, delete the neuefische file called `plot_colors_nf.json` and rename the file for spiced to `plot_colors.json`.
5. **Job Interview colors:** \
The Job colors are defined in two json files in the [Job_Interview](../DSBOOK/Job_Interview/) folder. Assuming you want to use the spiced color scheme, delete the file called `colors_nf.json` and rename the spiced file to `Job_colors.json`.


## Changing the logo of the Jupyter Book

In order to change the icon of the jupyter book which is displayed in the top left corner, you need to change the `logo` path in the [_config.yml](../DSBOOK/_config.yml) file. Per default it uses the neuefische logo, if you want to change it to the spiced logo replace the path with `images/spiced_logo_purple.png`.
