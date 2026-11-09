import nbformat as nbf
import click

@click.command()
@click.option('--lead', help="Name of the lead coach. [necessary]")
@click.option('--manager', help="Name of the bootcamp manager. [necessary]")
@click.option('--coach', default=None, help="Name of third coach [optional]")
@click.option('--course_id', help="Add course id (e.g. cgn-ds-23-1) [necessary]")
@click.option('--orientation_nb', default='../DSBOOK/sessions/01_Orientation.ipynb', help="Path to orientation notebook. [optional]")
@click.option('--team_nb', default='../DSBOOK/sessions/00_Team_Slides.ipynb', help="Path to team notebook. [optional]")

def create_slides(lead, manager, coach, course_id, orientation_nb, team_nb):

    # Open orientation and team notebook
    ntbk_team = nbf.read(team_nb, nbf.NO_CONVERT)
    ntbk = nbf.read(orientation_nb, nbf.NO_CONVERT)


    # Extract team info
    for cell in ntbk_team.cells:
        cell_tag = cell.get('metadata', {}).get('tags', [])
        if len(cell_tag) == 0:
            continue
        elif cell_tag[0] == lead:
            lead_info = cell.get('source')
        elif cell_tag[0] == manager:
            manager_info = cell.get('source')
        elif cell_tag[0] == coach:
            coach_info = cell.get('source')
        else:
            continue

       
    # Insert team info in orientation slides
    for i, cell in enumerate(ntbk.cells):
        cell_tag = cell.get('metadata', {}).get('tags', [])
        if len(cell_tag) == 0:
            continue
        elif cell_tag[0] == "welcome":
            cell['source'] = f"""<div class="slide-title"> 
        
# Welcome to the Data Science Bootcamp {course_id}!
           
</div> """
        elif cell_tag[0] == "lead":
            cell['source'] = lead_info
        elif cell_tag[0] == "manager":
            cell['source'] = manager_info
        elif cell_tag[0] == "coach":
            if coach != None:
                cell['source'] = coach_info    
            else:
                ntbk.cells.pop(i)

    # Write output to 
    nbf.write(ntbk, f"../DSBOOK/sessions/01_Orientation_{course_id}.ipynb")


if __name__ == '__main__':
    print("Let's create the orientation slides.")
    create_slides()