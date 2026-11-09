import base64
from IPython.display import Image, display
import json

with open('DSBOOK/sessions/plot_colors_nf.json', 'r') as pc:
    color_dict = json.load(pc)

theme_flowchart = color_dict['theme_flowchart']

def chart(graph, kind="flowchart"):
    graph_theme = theme_flowchart + graph
    graphbytes = graph_theme.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    display(Image(url="https://mermaid.ink/img/" + base64_string))
