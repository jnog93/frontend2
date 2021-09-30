"""The Broadlink-Raceland app built with pyscript"""

import json
import requests
import os 
import yaml 
import re 
import broadlink as blk

BROADLINK_CONFIG_FOLDER = pyscript.app_config['broadlink_config_file']
STORAGE_FILE = pyscript.app_config['storage_file']
STORAGE_FOLDER = pyscript.app_config['storage_folder']
INPUT_SELECT_YAML_FILE = pyscript.app_config['input_select_yaml_file'] 
INPUT_BOOL_YAML_FILE = pyscript.app_config['input_bool_yaml_file'] 
INPUT_SELECT_DASHBOARD = pyscript.app_config['input_select_dashboard'] 
INPUT_SELECT_DIVISION = pyscript.app_config['input_select_division'] 
INPUT_SELECT_REMOTE = pyscript.app_config['input_select_remote']
REMOTE_TEMPLATE_FOLDER = pyscript.app_config['remote_template_folder']
REMOTE_COUNTER_NAME = pyscript.app_config['remote_counter_name']
BASE_BOOL_NAME = pyscript.app_config['base_bool_name']


## ------------- Services ------------- ### 

@service('broadlink_raceland.send_request') 
def send_broadlink_api_request(command_name, mac_adress): 
    """Controls what happens when clicking on the remote
    If there is no command registered on a certain button, learn the command, or if the learning mode is on, a command is learned. Else send the command
    The command name must be unique"""
    input_bool_state = state.get(f"input_boolean.{BASE_BOOL_NAME}_{command_name.split('_')[-1]}")

    broadlink_data  = read_json_data(os.path.join(BROADLINK_CONFIG_FOLDER, mac_adress.replace(':', '') + ".json"))
    ip_address = broadlink_data["ip"] 

    command_info = None
    for command in broadlink_data["commands"]:
        if command["name"] == command_name: 
            command_info = command
            break

    if input_bool_state == "on":
        #If a command with the same name is already learned, delete it. These task run asynchronously
        if command_info != None:  
            task.create(delete_command, command_id = command_info["id"], ip_address = ip_address)
        task.create(learn_command, command_name = command_name, ip_address = ip_address) 
    
    elif input_bool_state == "off":
        #If there is no command in the button, learn it 
        if command_info == None: 
            task.create(learn_command, command_name = command_name, ip_address = ip_address)
        else: 
            task.create(send_command, command_id = command_info["id"], ip_address = ip_address) 


@service('broadlink_raceland.rename')
def rename(broadlink, new_name):
    """Renames a broadlink device (friendly name). Two broadlink can not have the same name"""
    #Get object state
    broadlink_state = str(state.get(broadlink)) #type casting into a string to prevent errors down the line
    new_name_state = str(state.get(new_name)).strip() 

    broadlink_data = read_json_data(os.path.join(BROADLINK_CONFIG_FOLDER, STORAGE_FILE)) 
    for broadlink_configured in broadlink_data.items():
        if broadlink_configured[1]['friendly_name'] == new_name_state: 
            notify.persistent_notification(message = "A broadlink with this name already exists", title = "Broadlink")
            return False
        if broadlink_configured[1]['friendly_name'] == broadlink_state: 
            mac_address = broadlink_configured[0]

    broadlink_data[mac_address]['friendly_name'] = new_name_state
    update_input_select(broadlink_data, INPUT_SELECT_YAML_FILE, INPUT_SELECT_REMOTE)
    write_json_data(os.path.join(BROADLINK_CONFIG_FOLDER, STORAGE_FILE), broadlink_data)

    input_select.reload() #Reload the input_select to update the friendly name




@service("broadlink_raceland.update_broadink_on_toogle") 
def update_broadlink_on_toggle(mac_adress, input_bool): 
    """Update broadlink devices on toogle. First checks if the IP adress was updated by sending a broadlink.hello() and comparing the IP adress 
    to the corresponding json file file"""

    #Before running this service check the state of the input_boolean. If the state is off then do not run the service
    state = state.get(input_bool) 
    if state == "off":
        log.debug("The device is off - The service will not try to update") 
        return 

    ##Get recorded information in the json file
    json_data = read_json_data(os.path.join(BROADLINK_CONFIG_FOLDER, mac_adress.replace(':', '') + ".json"))
    ip_address = json_data["ip"]
    try: 
        device = blk.hello(ip_address, timeout = 1)# Is this timeout enough? Since its in the local network it should be fine
    except blk.exceptions.NetworkTimeoutError: 
        message = f"Could not reach the IP address {ip_address}. Running discovery ..." 
        notify.persistent_notification(message = message, title = "Broadlink")
        broadlink_raceland.update_broadlink_remotes()  #Update broadlink devices if there was a network error 
    
    else: 
        discovered_device_mac = format_mac(device.mac) #Note: pyscript does not support iterators
        if discovered_device_mac != mac_adress: #On the off chance the IP adress update makes one device have the IP address of another device (broadlink)
            message = f"Ip address was updated {ip_address}. Running discovery ..."
            notify.persistent_notification(message = message, title = "Broadlink")
            broadlink_raceland.update_broadlink_remotes()  #Update broadlink devices if there was a network error 
    
@service('broadlink_raceland.update_broadlink_remotes') 
def update_broadlink_remotes(): 
    """Updates the avaiable broadlink devices"""
    log.info("Updating avaiable broadlink devices")
    r = task.executor(requests.post, url = "http://localhost:10981/discover", data = {})
    devices = json.loads(r.text)
    data = get_registered_devices(os.path.join(BROADLINK_CONFIG_FOLDER, STORAGE_FILE))  
    updated_data = update_list(devices, data) 
    update_input_select(updated_data, INPUT_SELECT_YAML_FILE, INPUT_SELECT_REMOTE) 
    write_json_data(os.path.join(BROADLINK_CONFIG_FOLDER, STORAGE_FILE), updated_data)

    input_select.reload() #This is called here instead of the script to make sure this service terminates before reloading


@service('broadlink_raceland.populate_view_input_select')
def populate_view_input_select(dashboard_name): 
    """Populates the INPUT_SELECT_DIVISION with the corresponding dashboard view names"""
    log.debug("Populating view for dashboard %s", dashboard_name)

    #Get the dashboard view names
    if dashboard_name == 'Overview':
        dashboard_file_name = os.path.join(STORAGE_FOLDER, 'lovelace')
    else: 
        dashboard_file_name = os.path.join(STORAGE_FOLDER, f'lovelace.lovelace_{dashboard_name}')
    
    json_data = read_json_data(dashboard_file_name)
    view_list = [] 
    for view in json_data['data']['config']['views']:
        view_list.append(view.get('title', "Unnamed View")) #Note: From what I understadnd Unnamed View is the default view name and is hardcodded in the frontend Typescript code

    # Update the input select (Note using pyscript function state.setattr and state.set attr did not work)
    input_selects_yaml = read_yaml(INPUT_SELECT_YAML_FILE)
    input_selects_yaml[INPUT_SELECT_DIVISION]['options'] = view_list
    write_yaml(input_selects_yaml, INPUT_SELECT_YAML_FILE)


@service('broadlink_raceland.update_dashboards')
def update_dashboards():
    """Updates the list of dashboards I can pick to add a remote. Similar to the homekit script
    This service is called each time a new dashboard is created and deleted and when homeassistant in initialized (there is a folder watcher in the .storage file)
    Instead of updating the list with the file, I prefer to scan the entire folder and get the list of dashboard""" 
    
    # Get the list of dashboard in storage mode (I need to take control of my dashboard in the dashboard tab first for the file to appear in .storage)
    dashboards_avaiable = [f for f in os.listdir(STORAGE_FOLDER) if os.path.isfile(os.path.join(STORAGE_FOLDER, f)) and (f.startswith('lovelace.lovelace') or f == 'lovelace')]
    dashboard_list = []

    """Make a list of the dashboards I can import
    The actualy name that shows in the frontend is also altered"""
    for board in dashboards_avaiable: 
        if board == 'lovelace': 
            dashboard_list.append('Overview')  #Let call the default dashboard Overview since there is no information in the file name or in other files (as far as I known)
        else: 
            board = board.replace('lovelace.lovelace_','')
            dashboard_list.append(board) 

    #Sort the list of dashboards    
    dashboard_list.sort()

    #Update the input select
    input_selects_yaml = read_yaml(INPUT_SELECT_YAML_FILE)
    input_selects_yaml[INPUT_SELECT_DASHBOARD]['options'] = dashboard_list
    write_yaml(input_selects_yaml, INPUT_SELECT_YAML_FILE)


@service("broadlink_raceland.add_remote") 
def add_remote_to_dashboard(broadlink, dashboard, division, remote_type): 
    """Add remote to dashboard. Causes Homeassistant to restart""" 
    broadlink_state = state.get(broadlink)
    dashboard_state = state.get(dashboard)
    division_state = state.get(division)
    remote_state = state.get(remote_type)
    
    #Increase the counter state by 1 and fetch new value
    counter.increment(entity_id = REMOTE_COUNTER_NAME)
    remote_counter = state.get(REMOTE_COUNTER_NAME) 

    #Get Mac adress 
    mac_address = get_mac_adress(broadlink_state)

    #Read remote yaml data
    remote_file_name = get_remote_name(remote_state) 
    yaml_data = read_yaml(os.path.join(REMOTE_TEMPLATE_FOLDER, remote_file_name))
    yaml_data = get_remote_from_template(yaml_data, str(remote_counter), mac_address) 

    #Read dashboard json 
    if dashboard_state != 'Overview':
        lovelace_file = os.path.join(STORAGE_FOLDER, f"lovelace.lovelace_{dashboard_state}")
    else: 
        lovelace_file = os.path.join(STORAGE_FOLDER, f"lovelace")
    
    dashboard_data = read_json_data(lovelace_file)
    
    ##Add remote to dashboard in the correct view
    index = 0
    for view in dashboard_data['data']['config']['views']: 
        if view['title'] == division_state: 
            view_cards = view.get('cards', []) 
            break
        index += 1
    
    view_cards.append(yaml_data) 
    dashboard_data['data']['config']['views'][index]['cards'] = view_cards
    write_json_data(lovelace_file, dashboard_data)

    #Create the input boolean to go with this remote
    create_input_boolean(INPUT_BOOL_YAML_FILE, BASE_BOOL_NAME, str(remote_counter))
    homeassistant.restart()


## ----- Helper functions ----- ###


def update_list(devices: list, data: dict): 
    """Compare the discovered devices with the current data and return an updated list"""
    suffix_dictionary = get_unique_id_suffix(data)

    for device in devices:
        if device["mac"] not in data: 
            if suffix_dictionary.get(device['model'], 0) == 0:
                friendly_name = device['model']
            else: 
                model = device['model']
                suffix = suffix_dictionary[device['model']] + 1
                friendly_name = f"{model} {suffix}"
            
            data[device["mac"]] = {
                "friendly_name": friendly_name, 
                "model": device['model']
            }   
    return data

def get_unique_id_suffix(data: dict): 
    """Returns a dictionary with the suffixes of the unique IDs"""
    suffix = {}
    for values in data.values():
        suffix[values['model']] = int(values.get(values['model'], 0)) + 1
    return suffix

def update_input_select(updated_data, yaml_file, entity): 
    """Update the input select entity"""
    yaml_data = read_yaml(yaml_file) 
    options = [device_data["friendly_name"] for device_data in updated_data.values()]
    yaml_data[entity]['options'] = options
    write_yaml(yaml_data, yaml_file)

def get_registered_devices(storage_file: str): 
    """Returns the json data from the storage file. If the file does not exist create it"""
    if not os.path.isfile(storage_file):
        create_file(storage_file)
    
    return read_json_data(storage_file)

def get_remote_name(s): 
    """Transform the remote state in remote file name"""
    s = str(s.lower()).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s) 


def get_mac_adress(broadlink_state: str) -> str:
    """Get the mac adress based the device friendly name"""
    broadlink_data = read_json_data(os.path.join(BROADLINK_CONFIG_FOLDER, STORAGE_FILE)) 
    for key, value in broadlink_data.items(): 
        if value['friendly_name'] == broadlink_state: 
            return key

def get_remote_from_template(yaml_data, remote_counter, mac_address): 
    """Replace entities id's, command name and mac adresses for the corresponding values 
    entity id and command name will be the name in the template + '_remote_counter' 
    mac_adresses will be broadlink device MAC adress"""
    yaml_string = yaml.dump(yaml_data)
    yaml_string = yaml_string.replace("number", str(remote_counter))
    yaml_string = yaml_string.replace(": mac", f": {mac_address}")
    return yaml.safe_load(yaml_string) 

def create_input_boolean(input_bool_file, base_bool_name, remote_counter):
    """Create an input for the remote""" 
    bool_yaml = read_yaml(input_bool_file) 
    bool_yaml[f"{base_bool_name}_{remote_counter}"] =  {
            "icon": "mdi:router-network", 
            "name": f"input_boolean_learning_{remote_counter}"
    }
    write_yaml(bool_yaml, input_bool_file) 

def learn_command(command_name, ip_address):
    """Learn a command""" 
    log.info(f"Learning command: {command_name} in {ip_address}") 
    task.executor(requests.post, url = "http://localhost:10981/learn", json = {"ipAddress": ip_address, "commandName" : command_name}) 
    log.info("Command learned") 
    
def delete_command(command_id, ip_address): 
    """Delete a command from the broadlink"""
    log.info(f"Deleting old command: {command_id} from {ip_address}")
    task.executor(requests.post, url = "http://localhost:10981/delete", json = {"ipAddress": ip_address, "commandId" : command_id})
    log.info("Command forgotten") 

def send_command(command_id, ip_address): 
    """Send command to the broadlink"""
    log.info(f"Sending command: {command_id} to {ip_address}")
    task.executor(requests.post, url = "http://localhost:10981/command", json = {"ipAddress": ip_address, "commandId" : command_id})
    log.info("Command sent")


@pyscript_executor        
def format_mac(mac_adress): 
    """Format mac address"""
    return ":".join(format(x, '02x') for x in mac_adress)


@pyscript_executor
def create_file(storage_file: str):
    """Creates the storage file with an empty dictionary"""
    with open(storage_file, 'w') as f:
        json.dump({}, f)

@pyscript_executor
def read_json_data(storage_file: str): 
    """Returns the json data from the storage file"""
    with open(storage_file, 'r') as f:
        data = json.load(f)
    return data

@pyscript_executor
def write_json_data(storage_file: str, data: dict):
    """Writes the json data to the storage file"""
    with open(storage_file, 'w') as f:
        json.dump(data, f, indent= 4)


@pyscript_executor
def read_yaml(fileName): 
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
def write_yaml(yaml_map, output_file_name): 
    """Writes a dictionary to yaml file """
    
    if not output_file_name.endswith('.yaml'): 
        output_file_name += '.yaml' 
    
    with open(output_file_name, "w") as ofh: 
        yaml.dump(yaml_map, ofh)