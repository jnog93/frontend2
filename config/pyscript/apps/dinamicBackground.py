import sys
import re 
import yaml
import os 

######Services############

@service
def change_background_image(imagename = None):
    """Modifies the yaml file and updates the imagename for all users"""
    for file in os.listdir(pyscript.app_config['homekit_infused_folder']): 
        if 'homekit-infused' in file: #updates wallpaper for all homekit-infused-{personName} files
            completePath = os.path.join(pyscript.app_config['homekit_infused_folder'], file)
            fileData = readFile(completePath)
            backgroundFileName = re.search("background: (.*)\n", fileData).group(1)
            if imagename == 'Theme wallpaper':  #Set the theme variable to be equal to the theme wallpaper 
                fileData = fileData.replace(f'background: {backgroundFileName}', f'background: var(--background-image)')
            else: 
                fileData = fileData.replace(f'background: {backgroundFileName}', f'background: \'center / cover no-repeat url("/local/images/wallpapers/{imagename}") fixed\'')
            writeToFile(fileData, completePath) 


@service
def update_wallpaper_options(entity_id = None):
    """Updates the list of wallpaper options. Supports png and jpg"""
    wallPaperList = []
    for file in os.listdir(pyscript.app_config['wallpaper_folder']):
        wallPaperList.append(file)
    wallPaperList.append('Theme wallpaper') #Add this option to be able to set the wallpaper defined in the theme
    wallPaperList.sort()
    yaml_map = readYaml(pyscript.app_config['wallpaper_selector_config_file']) #Reads the yaml file with the current options 
    yaml_map['options'] = wallPaperList #Updates the options list
    writeToYaml(yaml_map, pyscript.app_config['wallpaper_selector_config_file']) #finally write to the file


########Pyscript executor functions to deal with I/O 

@pyscript_executor
def readFile(fileName): 
    """Reads and returns a String"""

    #Add yaml to the end of the file 
    if not fileName.endswith('.yaml'):
        fileName += '.yaml'

    #open the file and return the a string    
    with open(fileName, 'r') as fh: 
        return fh.read() 


@pyscript_executor
def writeToFile(fileData, fileName): 
    """Writes to a file"""
    #Add yaml to the end of the file 
    if not fileName.endswith('.yaml'):
        fileName += '.yaml'

    with open(fileName, 'w') as ofh: 
        ofh.write(fileData)


@pyscript_executor
def readYaml(fileName): 
    """Reads a yaml file and returns a dictionary"""
    
    if not fileName.endswith('.yaml'): 
        fileName += '.yaml' 
    
    with open(fileName, "r") as fh: 
        try: 
            yaml_map = yaml.load(fh)
        except yaml.YAMLError as exc:
            yaml_map = exc
    
    return yaml_map


@pyscript_executor
def writeToYaml(yaml_map, output_file_name): 
    """Writes a dictionary to yaml file """
    
    if not output_file_name.endswith('.yaml'): 
        output_file_name += '.yaml' 
    
    with open(output_file_name, "w") as ofh: 
        yaml.dump(yaml_map, ofh)