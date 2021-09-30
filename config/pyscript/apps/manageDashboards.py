"""Services to create and remove dashboards when users are created or deleted"""
import json 
import re
import os 
import yaml

# ---------Services-----------
@service
def create_new_dashboard(userID = None): 
    """Service to create a new homekit dashboard for a user, when the user is created"""

    task.sleep(10) #Wait for informations to written to the auth files. Nota : This is not a good solution, but it works for now. Is there a way to known the file has been written to?
    
    #Get the user permission and username from the .storage/auth file
    authFile = pyscript.app_config['file_auth']
    jsonMap = readJsonStorage(authFile)
    userType = get_user_permission(jsonMap, userID)
    if userType == None: #If an user is created but the username already exists the event is fired. However, no user is written to the auth file
        log.warning('User not found on database. Likely duplicate username or the wait times need to be greater')
        return #end function 
    userName = get_user_username(jsonMap, userID)

    #Create a new dashboard for the user in the hki_configuration.yaml file 
    hkiRawFileName = pyscript.app_config['hki_main_config_file'] 
    hkiRaw = readFile(hkiRawFileName, fileType = 'yaml')
    dashboardInfo = re.search('# //Lovelade Dashboards\n((.*\n)*)# //End of lovelace dashboards', hkiRaw).group(1)
    newDashboard = dashboardInfo + '\n' + get_dashboard_info(userName, userType) 
    hkiRaw = hkiRaw.replace(dashboardInfo, newDashboard) 
    writeToFile(hkiRawFileName, hkiRaw, fileType = 'yaml') 

    #Add group entities related to the new dashboard to the device_counter file
    device_counter_file = pyscript.app_config['device_counter_file']
    device_counter_raw = readFile(device_counter_file, fileType = 'yaml')
    device_counter_raw += '\n' + add_device_counters(userName)
    writeToFile(device_counter_file, device_counter_raw, fileType= 'yaml') 

    #Add sensors related to the new dashboard
    sensorFileName = pyscript.app_config['user_sensors_file'] 
    sensorData = readYamlFile(sensorFileName)
    sensorData = add_sensors(sensorData, userName)
    writeToYaml(sensorFileName, sensorData)

    #Add user to the dashboard_users option file
    dashboardUsersFile = pyscript.app_config['dashboard_users_file']
    dashboardUsersMap = readYamlFile(dashboardUsersFile) 
    dashboardUsersMap['options'].append(userName)
    writeToYaml(dashboardUsersFile, dashboardUsersMap)

    #clone homekit-infused, base, header-base, view config and general config files
    hkiInfusedRaw = readFile(pyscript.app_config['hki_infused_template'], fileType = 'yaml')
    hkiInfusedRaw = hkiInfusedRaw.replace('base.yaml', 'base_{}.yaml'.format(get_valid_username(userName,'_'))) 
    writeToFile(pyscript.app_config['hki_infused_template'].replace('/homekit-infused', '/homekit-infused-{}'.format(get_valid_username(userName, '-'))), hkiInfusedRaw, fileType= 'yaml')

    baseTemplate = readFile(pyscript.app_config['base_template'], fileType = 'yaml')
    baseTemplate = baseTemplate.replace('_global.view_config', '_global.view_config_{}'.format(get_valid_username(userName, '_')))
    baseTemplate = baseTemplate.replace('_global.general_config', '_global.general_config_{}'.format(get_valid_username(userName, '_'))) 
    baseTemplate = baseTemplate.replace('header-base-template', 'header-base-template-{}'.format(get_valid_username(userName, '-'))) 
    baseTemplate = baseTemplate.replace('- current_user: ""', '- current_user: -{}'.format(get_valid_username(userName, '-')))
    writeToFile(pyscript.app_config['base_template'].replace('/base', '/base_{}'.format(get_valid_username(userName, '_'))), baseTemplate, fileType= 'yaml')

    headerBaseTemplate = readFile(pyscript.app_config['header_base_template'], fileType = 'yaml')
    headerBaseTemplate = headerBaseTemplate.replace('_global.general_config', '_global.general_config_{}'.format(get_valid_username(userName, '_')))
    writeToFile(pyscript.app_config['header_base_template'].replace('/header-base-template', "/header-base-template-{}".format(get_valid_username(userName, '-'))), headerBaseTemplate, fileType= 'yaml') 

    newViewConfig = get_template_view_config(get_valid_username(userName, '_'), userType) 
    writeToFile(pyscript.app_config['view_config_template'].replace('/view_config', '/view_config_{}'.format(get_valid_username(userName, '_'))) , newViewConfig, fileType= 'yaml')

    generalConfigTemplate = readFile(pyscript.app_config['general_config_template'], fileType = 'yaml') 
    generalConfigTemplate = generalConfigTemplate.replace('all_light_entities', 'all_light_entities_{}'.format(get_valid_username(userName, '_'))) #For now only need to replace this. In the future do this with regex? 
    generalConfigTemplate = generalConfigTemplate.replace('sensor.current_lights_on', 'sensor.current_lights_on_{}'.format(get_valid_username(userName, '_'))) #For now only need to replace this. In the future do this with regex?  
    generalConfigTemplate = generalConfigTemplate.replace('general_config', 'general_config_{}'.format(get_valid_username(userName, '_')))
    writeToFile(pyscript.app_config['general_config_template'].replace('/general_config', '/general_config_{}'.format(get_valid_username(userName, '_'))) , generalConfigTemplate, fileType= 'yaml')

    #Call service to restart home assistant 
    #homeassistant.restart() 


@service 
def remove_dashboard(userID = None):
    """Remove a dashboard and dashboard information when a user is deleted"""
    ident = '  '
    
    authFile = pyscript.app_config['file_auth']
    jsonMap = readJsonStorage(authFile)
    userName = get_user_username(jsonMap, userID) 

    hki_infused_file = pyscript.app_config['hki_infused_template']
    base_file = pyscript.app_config['base_template']
    header_base_file = pyscript.app_config['header_base_template']
    view_config_file = pyscript.app_config['view_config_template']
    general_config_file = pyscript.app_config['general_config_template']

    if not hki_infused_file.endswith('.yaml'):
        hki_infused_file += '.yaml'
    if not base_file.endswith('.yaml'):
        base_file += '.yaml'
    if not view_config_file.endswith('.yaml'):
        view_config_file += '.yaml'
    if not general_config_file.endswith('.yaml'): 
        general_config_file += '.yaml'
    if not header_base_file.endswith('.yaml'):
        header_base_file += '.yaml'
    
    #Make a failsafe in case the user deletes a dashboard before it is created
    while os.path.isfile(general_config_file) == False: 
        task.sleep(2)

    ##Remove yaml files

    os.remove(hki_infused_file.replace('.yaml', "-{}.yaml".format(get_valid_username(userName, '-'))))
    os.remove(base_file.replace('.yaml', '_{}.yaml'.format(get_valid_username(userName, '_'))))
    os.remove(view_config_file.replace('.yaml', '_{}.yaml'.format(get_valid_username(userName, '_'))))
    os.remove(general_config_file.replace('.yaml', '_{}.yaml'.format(get_valid_username(userName, '_')))) 
    os.remove(header_base_file.replace('.yaml', '-{}.yaml'.format(get_valid_username(userName, '-'))))

    #Remove dashboard info from the hki_configuration.yaml file 
    hkiRawFileName = pyscript.app_config['hki_main_config_file']
    hkiRaw = readFile(hkiRawFileName, fileType = 'yaml')
    dashboardsInfo = re.search('# //Lovelade Dashboards\n((.*\n)*)# //End of lovelace dashboards', hkiRaw).group(1)
    dashboardsInfoMap = yaml.load(dashboardsInfo)
    del dashboardsInfoMap['lovelace']['dashboards']["homekit-infused-{}".format(get_valid_username(userName, '-'))]
    yamlString = mapToYamlString(dashboardsInfoMap)
    hkiRaw = hkiRaw.replace(dashboardsInfo, yamlString)
    writeToFile(hkiRawFileName, hkiRaw, fileType = 'yaml') 

    #Remove Information related to the dashboard from the respective files 
    #sensors 
    sensorFileName = pyscript.app_config['user_sensors_file']
    usersSensorData = readYamlFile(sensorFileName)
    userSensorData = remove_user_entites(usersSensorData, userName)
    if userSensorData != {}: 
        writeToYaml(sensorFileName, userSensorData)
    else: 
        writeToFile(sensorFileName, '', fileType= 'yaml')
    
    #Device counter 
    deviceFileName = pyscript.app_config['device_counter_file']
    deviceMap = readYamlFile(deviceFileName)
    deviceMap = remove_user_entites(deviceMap, userName)
    writeToYaml(deviceFileName, deviceMap) 

    #User 
    dashboardUsersFile = pyscript.app_config['dashboard_users_file']
    dashboardUsersMap = readYamlFile(dashboardUsersFile) 
    dashboardUsersMap['options'].remove(userName) 
    writeToYaml(dashboardUsersFile, dashboardUsersMap)

# -----------------------Helper functions ---------------------------#

def get_valid_username(userName, replacement) -> str:
    """Returns a valid username depending on the situation"""
    return re.sub('_|\s|-', replacement, userName)
    

def get_user_permission(jsonMap, userID) -> str: 
    """Get user type"""
    for person_data in jsonMap["data"]["users"]:
        if person_data["id"] == userID:  
            group = person_data["group_ids"][0]
            if group == 'system-admin': 
                return 'admin'
            else: 
                return 'user'
    return None

def get_user_username(jsonMap, userID) -> str: 
    """Get user type"""
    for person_data in jsonMap["data"]["credentials"]:
        if person_data["user_id"] == userID: 
            return person_data["data"]["username"]

def get_template_view_config(personName, userType, ident = '  ') -> str: 
    """Get view config for the new dashboard"""
    newViewConfig = f'view_config_{personName}:\n'
    newViewConfig += f'{ident}home:\n'
    newViewConfig += f'{ident*2}icon: mdi:home\n'
    newViewConfig += f'{ident*2}menu:\n'
    newViewConfig += f'{ident*3}Title: "Divis\xF5es"\n'
    newViewConfig += f'{ident*2}show_in_menu: false\n'
    newViewConfig += f'{ident*2}show_in_navbar: true\n'
    newViewConfig += f'{ident*2}title: Menu Principal\n'
    newViewConfig += f'{ident*2}show_header: true\n'
    if userType == 'admin': 
        newViewConfig += f'{ident*2}hki_menu: null\n'
    return newViewConfig

def get_dashboard_info(userName, userType, ident = '  ') -> str:
    """Generate dashboard info for the hki_configuration"""
    userName = get_valid_username(userName, '-')
    dashboard = ""
    dashboard += f'{ident*2}homekit-infused-{userName}:\n'
    dashboard += f'{ident*3}mode: yaml\n'
    dashboard += f'{ident*3}title: Homekit Infused {userName}\n'
    dashboard += f'{ident*3}icon: mdi:home-assistant\n'
    dashboard += f'{ident*3}show_in_sidebar: true\n'
    dashboard += f'{ident*3}filename: "hki-base/homekit-infused-{userName}.yaml"\n'
    if userType == 'admin': 
        dashboard += f'{ident*3}require_admin: true\n'
    else: 
        dashboard += f'{ident*3}require_admin: false\n'
    return dashboard 



def mapToYamlString(dashboardInfoMap, ident_level = 0,  ident = '  '): 
    """Convert a dictionary into a string representation of a yaml using recursion.
    Works for limited cases"""
    final_string = ''
    for key, value in dashboardInfoMap.items():
        if isinstance(value, dict):  
            final_string += f'{ident*ident_level}{key}:\n'
            final_string += mapToYamlString(value, ident_level+1)
        else: 
            if value == True: 
                value = 'true'
            if 'template' in key:
                final_string += f'{ident*ident_level}{key}: >-\n{value}\n'
            else:  
                final_string += f'{ident*ident_level}{key}: {value}\n'
    return final_string

def add_device_counters(username, ident = '  ') -> str: 
    """Add device Counter for a user in the file"""
    username = get_valid_username(username, '_')
    return f'all_light_entities_{username}: \
    \n{ident}entities:\n'
    
def add_sensors(sensorData, username) -> dict: 
    """Update sensors counters in the user_sensor yaml"""
    ##For now only add the light sensor counter
    username = get_valid_username(username, '_')
    if sensorData == None: 
        sensorData = {} 
    lightSensor = {f'current_lights_on_{username}': {'friendly_name': f'All Lights Currently On in {username} dashboard', 'value_template': f'{{{{ expand("group.all_light_entities_{username}")|selectattr("state","eq","on")|list|count }}}}'}}  
    sensorData.update(lightSensor) 
    return sensorData

def remove_user_entites(userData, userName) -> dict: 
    """Remove entities in the users yaml"""
    userName = get_valid_username(userName, '_')
    newUserData = userData.copy()
    for key in userData.keys(): 
        if userName in key: 
            del newUserData[key]
    return newUserData 


# ----------------------Functions that deal with I/O --------------------------------- 

@pyscript_executor
def readJsonStorage(file) -> dict: 
    """Reads a json file and returns a dictionary"""
    
    with open(file, "r") as fh: 
        try: 
            json_map = json.load(fh)
        except json.JSONDecodeError as exc:
            json_map = exc
    
    return json_map

@pyscript_executor
def readFile(fileName, fileType = None) -> str: 
    """Reads a file"""
    if fileType != None and not fileName.endswith(f'.{fileType}'): 
        fileName += f'.{fileType}'

    with open(fileName, "r") as fh: 
        return fh.read()

@pyscript_executor
def writeToFile(fileName, data, fileType = None): 
    """Write data to a file"""
    if fileType != None and not fileName.endswith(f'.{fileType}'): 
        fileName += f'.{fileType}'
    with open(fileName, "w") as fh: 
        fh.write(data)

@pyscript_executor
def readYamlFile(fileName) -> dict: 
    """Reads data from yaml file """
    if not fileName.endswith('.yaml'): 
        fileName += '.yaml'
    
    with open(fileName, "r") as fh:
        try:
            yaml_map = yaml.safe_load(fh)
        except yaml.YAMLError:
            log.info(f'Error reading the yaml file {fileName}') 
            return None
    return yaml_map

@pyscript_executor
def writeToYaml(fileName, data) -> None: 
    """Write data to a yaml file""" 
    if not fileName.endswith('.yaml'): 
        fileName += '.yaml'
    
    with open(fileName, "w") as fh: 
        yaml.dump(data, fh)
