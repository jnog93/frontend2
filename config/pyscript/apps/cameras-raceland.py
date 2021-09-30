"""Scripts to add cameras entities to homeassistant using the frontend. Does I/O of entities in the yaml file"""

import slugify
import json 
import yaml
import os 
import re
import datetime

from homeassistant.const import MAX_LENGTH_STATE_ENTITY_ID


CAMERA_CONFIG_FILE = pyscript.app_config["camera_yaml_file"]
CAMERAS_TO_BE_RECORDED = pyscript.app_config["cameras_to_be_recorded"] 
SCRIPT_FILE = pyscript.app_config["scrip_yaml_file"]
INPUT_SELECT_CONFIGURED_CAMERAS =  pyscript.app_config["registered_cameras"]
NOTIFICATION_TITLE = 'Câmeras-Raceland'
INPUT_SELECT_FILE = pyscript.app_config["input_select_file"]
NUMBER_OF_PRESETS = pyscript.app_config["number_of_presets"]
RECORDING_FOLDER = pyscript.app_config["recordings_folder"]
DRYRUN = False

### ------ Services ------ ####

@service("raceland_cameras.add_camera_entity") 
def add_camera_entity(inp_text_camera_static, 
    inp_text_camera_stream, 
    inp_text_username, 
    inp_text_password, 
    inp_text_camera_name, 
    inp_sel_authentication, 
    inp_sel_verify_ssl, 
    inp_num_framerate, 
    inp_rtsp_transport,
    inp_bool_record): 
    """Adds camera entity based on the information given in the frontend form."""
    
    #Important: Typecast the state to string
    camera_static = str(state.get(inp_text_camera_static)).strip()
    camera_stream = str(state.get(inp_text_camera_stream)).strip()
    username = str(state.get(inp_text_username)).strip()
    password = str(state.get(inp_text_password)).strip()
    camera_name = str(state.get(inp_text_camera_name)).strip()
    camera_entity_id = slugify.slugify(camera_name, separator = "_") #slugify the camera name to check if the name is legal
    authentication = str(state.get(inp_sel_authentication))
    ssl = str(state.get(inp_sel_verify_ssl))
    framerate = float(state.get(inp_num_framerate))
    rtsp_transport = str(state.get(inp_rtsp_transport))
    camera_bool_record = str(state.get(inp_bool_record))

    #Check if the formulary is valid #Returns true if it valid and false if not. If the form is not valid end the execution of the script
    if not is_form_valid(camera_static, camera_stream, camera_name, camera_entity_id, camera_bool_record):        
        return 

    #Add camera to the yaml file
    yaml_data = read_yaml(CAMERA_CONFIG_FILE)
    if yaml_data == None: 
        yaml_data = []

    camera_to_add = {
        "platform": "generic",
        "still_image_url": camera_static,
        "stream_source": camera_stream,
        "name": camera_name, 
        "verify_ssl": ssl,
        "username": username,
        "password": password,
        "authentication": authentication,
        "framerate": framerate, 
        "rtsp_transport": rtsp_transport
    }
    yaml_data.append(camera_to_add)

    # Update the input select (Note: using pyscript funct state.setattr and state.set attr did not work, as the atrribute would not persist) 
    update_input_select_options(INPUT_SELECT_FILE, INPUT_SELECT_CONFIGURED_CAMERAS, new_option = camera_name, action = "Add")

    #Create scripts to add move camera: 
    script_map = {}
    for preset_i in range(NUMBER_OF_PRESETS):
        script_map[f"move_{camera_entity_id}_to_preset_{preset_i + 1}"] = {
            "mode": "single", 
            "alias": f"Move {camera_name} to preset {preset_i + 1}",
            "sequence": [
                {
                    "service": "raceland_cameras.move_to_preset",
                    "data": {
                        "camera_entity_id": f"camera.{camera_entity_id}", 
                        "preset_number": preset_i + 1
                    }
                }
            ]
        }
        
    script_yaml = read_yaml(SCRIPT_FILE) 
    script_yaml.update(script_map)
    
    #Optionaly, start recording a stream for that camera: 
    cameras_to_be_recorded = read_json_data(CAMERAS_TO_BE_RECORDED)
    if camera_bool_record == "on":
        cameras_to_be_recorded[camera_name] = {"record": "True"}
        time_to_record = (datetime.datetime.now().replace(hour=5, minute=0, second = 0) +  datetime.timedelta(days=1)) - datetime.datetime.now() 
        pattern = r'\d{1,2}:\d{1,2}:\d{1,2}'
        time_to_record_formated = re.search(pattern, str(time_to_record)).group(0)
        rtsp_source = get_url_with_credentials(camera_to_add)
        file_name = os.path.join(RECORDING_FOLDER, str(datetime.datetime.today()).split()[0].replace('-','_') + '_' + camera_entity_id + '.mp4') 
        run_ffmpeg(rtsp_source, file_name, time_to_record_formated)
    else: 
        cameras_to_be_recorded[camera_name] = {"record": "False"}
    
    #write to files 
    write_yaml(yaml_data, CAMERA_CONFIG_FILE)
    write_yaml(script_yaml, SCRIPT_FILE)
    write_json_data(CAMERAS_TO_BE_RECORDED, cameras_to_be_recorded)
    homeassistant.restart() #Adding a camera requires rebooting homeassistant


@service("raceland_cameras.delete_camera_entity")
def delete_camera_entity(registered_cameras_entity):  
    """Service to delete camera entity based on the friendly name"""
    friendly_name = state.get(registered_cameras_entity)
    if friendly_name == 'None': 
        return #Stop the execution because there is no camera to delete 
    camera_entity_id = slugify.slugify(friendly_name, separator = "_") 
    yaml_data = read_yaml(CAMERA_CONFIG_FILE)
    for camera in yaml_data.copy():
        if camera['name'] == friendly_name: 
            yaml_data.remove(camera)
            break
    
    #Update the input select that keeps track of the camera
    update_input_select_options(INPUT_SELECT_FILE, INPUT_SELECT_CONFIGURED_CAMERAS, new_option = friendly_name, action = "Remove")
    #Remove all the scripts for that camera
    scripts_yaml = read_yaml(SCRIPT_FILE)
    for script_name in scripts_yaml.copy():
        if script_name.startswith(f"move_{camera_entity_id}"):
            del(scripts_yaml[script_name])

    #Remove the camera from the record file list 
    cameras_to_be_recorded = read_json_data(CAMERAS_TO_BE_RECORDED)
    del(cameras_to_be_recorded[friendly_name])
    
    #write to files save changes
    write_json_data(CAMERAS_TO_BE_RECORDED, cameras_to_be_recorded)
    write_yaml(scripts_yaml, SCRIPT_FILE)
    write_yaml(yaml_data, CAMERA_CONFIG_FILE)
            
    log.info(f"Camera {friendly_name} removed with sucess")         
    homeassistant.restart() #Removing a camera requires rebooting homeassistant


@service("raceland_cameras.update_camera_information")
def update_camera_information(
    inp_text_camera_static,
    inp_text_camera_stream, 
    inp_text_username, 
    inp_text_password,
    inp_text_camera_name, 
    inp_selected_camera, 
    inp_sel_authentication, 
    inp_sel_verify_ssl, 
    inp_num_framerate, 
    inp_rtsp_transport, 
    inp_bool_record): 
    """Service to handle updating camera info"""
    yaml_data = read_yaml(CAMERA_CONFIG_FILE)
    selected_camera_name = str(state.get(inp_selected_camera)) 
    camera_name_set = set()
    
    #Get the correct index in the file to update
    for i in range(len(yaml_data.copy())):
        camera_name_set.add(yaml_data[i]['name'])
        if yaml_data[i]['name'] == selected_camera_name: 
            index_to_update = i
    
    #Note: If I replace the name of the helpers I can do this programatically in 3-4 lines
    if str(state.get(inp_text_camera_static)) != "": 
        yaml_data[index_to_update]['still_image_url'] = str(state.get(inp_text_camera_static)) 
    if str(state.get(inp_text_camera_stream)) != "":
        yaml_data[index_to_update]['stream_source'] = str(state.get(inp_text_camera_stream)) 
    if  str(state.get(inp_text_username)) != "": 
        yaml_data[index_to_update]['username'] = str(state.get(inp_text_username)) 
    if str(state.get(inp_text_password)) != "":
        yaml_data[index_to_update]['password'] = str(state.get(inp_text_password)) 
    if str(state.get(inp_text_camera_name)) != "":
        new_camera_name = str(state.get(inp_text_camera_name))
        if new_camera_name in camera_name_set: 
            log.error(f"Duplicate names are not allowed")  
            notify_frontend(NOTIFICATION_TITLE, "Erro: Já existe uma câmera com esse nome registado", type =  "persistent_notification")
            return
        update_input_select_options(INPUT_SELECT_FILE, INPUT_SELECT_CONFIGURED_CAMERAS, new_camera_name, action = "Update", old_option= yaml_data[index_to_update]['name']) 
        yaml_data[index_to_update]['name'] = new_camera_name 
    if state.get('input_boolean.camera_update_advanced_options') == 'on': #Unless the input_boolean is turned to on these options will not update
        ##Since these are input select I do not need to check if they are empty
        yaml_data[index_to_update]['authentication'] = str(state.get(inp_sel_authentication)).lower()
        yaml_data[index_to_update]['verify_ssl'] = str(state.get(inp_sel_verify_ssl))
        yaml_data[index_to_update]['framerate'] = float(state.get(inp_num_framerate))
        yaml_data[index_to_update]['rtsp_transport'] = str(state.get(inp_rtsp_transport)) 

    #update the record file
    cameras_to_be_recorded = read_json_data(CAMERAS_TO_BE_RECORDED)
    _input_bool_record = str(state.get(inp_bool_record))
    if _input_bool_record == 'on': 
        input_bool_record = "True"
    if _input_bool_record == 'off':
        input_bool_record = "False" 

    if str(state.get(inp_text_camera_name)) != "":
        new_camera_name = str(state.get(inp_text_camera_name))
        del(cameras_to_be_recorded[selected_camera_name])
        cameras_to_be_recorded[new_camera_name] = {"record": input_bool_record}
    else: 
        cameras_to_be_recorded[selected_camera_name] = {"record": input_bool_record}
    
    #update the scripts file
    scripts_yaml = read_yaml(SCRIPT_FILE)
    if str(state.get(inp_text_camera_name)) != "":
        old_camera_entity_id = slugify.slugify(selected_camera_name, separator = "_")
        new_camera_entity_id = slugify.slugify(str(state.get(inp_text_camera_name)), separator = "_")
        for script_name in scripts_yaml.copy():
            if script_name.startswith(f"move_{old_camera_entity_id}"):
                new_script_name = script_name.replace(old_camera_entity_id, new_camera_entity_id)
                log.info(new_script_name) 
                scripts_yaml[new_script_name] = scripts_yaml[script_name]
                del(scripts_yaml[script_name])
    
    #write everything to files
    write_yaml(yaml_data, CAMERA_CONFIG_FILE)
    write_yaml(scripts_yaml, SCRIPT_FILE)
    write_json_data(CAMERAS_TO_BE_RECORDED, cameras_to_be_recorded)
    homeassistant.restart() #Updating a camera requires rebooting homeassistant


@service("raceland_cameras.move_to_preset") 
def move_to_preset(camera_entity_id, preset_number):
    """yaml
name: Move Camera to preset
description: Service to move the camera to a preset. Can be used in a script and then integrated with a picture-glance card in lovelace
fields:
  camera_entity_id:
     description: Camera entity to send the command
     name: Camera Entity Id 
     example: camera.camera_name
     required: true
     selector:
        entity: 
          domain: camera
  preset_number:
     description: Id of the preset to move the camera
     example: 1
     required: true
     selector:
       number:
        min: 1
        max: 100
        mode: box
    """
    
    log.info(camera_entity_id) 
    log.info(preset_number)
    #Note: The docstring above is equivalent to a service.yaml. Although its not needed leave it 
    #Runs the command: curl -X PUT --user admin:raceland2015 --user-agent "admin" --digest http://192.168.1.69/ISAPI/PTZCtrl/channels/1/presets/2/goto

    #Get information about the camera
    ##refactor using the camera entity id as an entry point 
    camera_name = state.getattr(camera_entity_id)['friendly_name'] 
    camera = get_camera_information(camera_name) 
    if camera: 
        user = camera['username']
        password = camera['password']
        ip_address = get_ip_address(camera)

    #Run the command to move to the preset
    log.info(f"Running the command: curl -X PUT --user {user}:{password} --user-agent '{user}' --digest http://{ip_address}/ISAPI/PTZCtrl/channels/1/presets/{preset_number}/goto") 
    os.system(f"curl -X PUT --user {user}:{password} --user-agent '{user}' --digest http://{ip_address}/ISAPI/PTZCtrl/channels/1/presets/{preset_number}/goto")

            


### ------ Automations ------ #### 

@state_trigger(INPUT_SELECT_CONFIGURED_CAMERAS)
def update_input_text_entities(): 
    """Update entities in the frontend when selecting a camera in the update cameras information tab"""
    #Get information about the current camera
    camera_friendly_name = state.get(INPUT_SELECT_CONFIGURED_CAMERAS)
    if camera_friendly_name == 'None': #When there no cameras selected, set some input_text to null
        state.set('input_text.camera_config_still_image', value  = "")
        state.set('input_text.camera_config_username', value  = "")
        state.set('input_text.camera_config_password', value  = "")
        return 
    
    recording_bool = read_json_data(CAMERAS_TO_BE_RECORDED)[camera_friendly_name]['record']
    if recording_bool == "True":
        recording_bool_state = "on"
    elif recording_bool == "False": 
        recording_bool_state = "off"
    camera = get_camera_information(camera_friendly_name) 
    if camera: 
        #Update the input text entities with the current information 
        #Note: If I update the entities names I can do this programatically in 3-4 lines
        state.set('input_text.camera_config_still_image', value  = camera['still_image_url'])
        state.set('input_text.camera_config_rtsp', value  = camera['stream_source'])
        state.set('input_text.camera_config_username', value  = camera['username'])
        state.set('input_text.camera_config_password', value  = "•••••••")
        state.set('input_text.camera_config_camera_name', value  = camera['name'])
        state.set('input_text.camera_config_authenication', value  = camera['authentication'].capitalize())
        state.set('input_text.camera_config_verify_ssl', value  = 'State: ' + str(camera['verify_ssl'])) 
        state.set('input_text.camera_config_rtsp_transport', value  = camera['rtsp_transport'])
        state.set('input_text.camera_config_framerate', value  = str(int(camera['framerate'])) + " fps") 

        #Update the input select update options. #These entites are updated so the user does not accidently overwrite anything
        state.set('input_text.camera_update_still_image', value  = '')
        state.set('input_text.camera_update_rtsp', value  = '')
        state.set('input_text.camera_update_username', value  = '')
        state.set('input_text.camera_update_password', value  = '')
        state.set('input_text.camera_update_camera_name', value  = '')
        state.set('input_select.camera_update_authentication', value  = camera['authentication'].capitalize())
        state.set('input_select.camera_update_verify_ssl', value  = camera['verify_ssl']) 
        state.set('input_select.camera_update_rtsp_transport', value  = camera['rtsp_transport'])
        state.set('input_number.camera_update_framerate', value  = camera['framerate']) 
        state.set('input_boolean.camera_update_record_video', value = recording_bool_state) 

@time_trigger("once(5:00:00)")
def record_camera() -> None:  
    """Automation that gets triggered at 5am every day to record camera feed. 
    Only records feed from the cameras in dictionary cameras_to_record. Also delete feed of the cameras from the previous 2 days"""
    camera_yaml = read_yaml(CAMERA_CONFIG_FILE)
    cameras_to_record  = read_json_data(CAMERAS_TO_BE_RECORDED)
    time = "24:00:00"    
    for camera_friendly_name in cameras_to_record:
        if cameras_to_record[camera_friendly_name]['record'] == 'True': 
            camera = get_camera_information(camera_friendly_name, camera_yaml)
            rtsp_source = get_url_with_credentials(camera)
            file_name = os.path.join(RECORDING_FOLDER, str(datetime.datetime.today()).split()[0].replace('-','_') + '_' + slugify.slugify(camera_friendly_name, separator = "_") + '.mp4') 
            run_ffmpeg(rtsp_source, file_name, time)
    
    #Delete file from the current day - 2 
    delete_date = str(datetime.datetime.today() - datetime.timedelta(days = 2)).split()[0].replace('-','_')
    for filename in os.listdir(RECORDING_FOLDER):
        if filename.startswith(delete_date):
            os.remove(os.path.join(RECORDING_FOLDER, filename))

#### ---- Helper functions ---- ####

def notify_frontend(domain, message, type = "persistent_notification") -> None:
    """Handles notifications
    Supported types: 
    Persistant notifications"""
    if type == "persistent_notification":
        notify.persistent_notification(message = message, title = domain)
    return 


def is_form_valid(camera_static : str, camera_stream : str, camera_name : str, camera_entity_id : str, camera_bool_record : str) -> bool: 
    """Check if the input form is valid"""
    registered_cameras = set(state.names(domain = 'camera')) 
    message_list = [] 
    if camera_name == "":  #Camera has to have a friendly name
        message_list.append("Erro: Adicione nome a câmera") 
    if f"camera.{camera_entity_id}" in registered_cameras:
        message_list.append(f"Erro: Entidade já esta registada") 
    if (camera_static == "" and camera_stream == ""): 
        message_list.append("Erro: Adicione pelo menos o URL da câmara estática ou uma stream RTSP") 
    if camera_stream == "" and camera_bool_record == "on":
        message_list.append("Erro: Para conseguir utilizar a opção de gravar especifique o link da stream RTSP")
    if len(camera_name) >= MAX_LENGTH_STATE_ENTITY_ID: 
        message_list.append("Erro: Nome da câmera tem que ter no maximo " + str(MAX_LENGTH_STATE_ENTITY_ID) + " caracteres")
    for err in message_list: 
        log.error(err) 
        notify_frontend(NOTIFICATION_TITLE, err, type =  "persistent_notification")
    
    return False if len(message_list) > 0 else True


def check_duplicate_camera_name(registered_cameras, camera_name) -> bool:
    """Checks if the camera name is already registered in the yaml file"""
    return True if camera_name in registered_cameras else False

def update_input_select_options(input_select_file, input_select_cameras_registered, new_option, action, old_option = None, reload = False) -> None: 
    """Updates the options of the input select
    3 options Add (append an option the list), Remove (remove and option to the list) and update (remove the old option and add a new one) """
    yaml_data = read_yaml(input_select_file)
    if action == 'Add': 
        yaml_data[input_select_cameras_registered.split('.')[1]]['options'].append(new_option) 
    elif action == 'Remove': 
        yaml_data[input_select_cameras_registered.split('.')[1]]['options'].remove(new_option)
    elif action == 'Update':
        yaml_data[input_select_cameras_registered.split('.')[1]]['options'].remove(old_option)
        yaml_data[input_select_cameras_registered.split('.')[1]]['options'].append(new_option) 
    else: 
        log.error("Unknown action: " + action)
    write_yaml(yaml_data, input_select_file)
    if reload:
        input_select.reload()

def get_camera_information(camera_name, yaml_data = None): 
    """Loops through the camera file until it find a matching camera with the same friendly name. returns false if it does find any camera"""
    if yaml_data is None: 
        yaml_data = read_yaml(CAMERA_CONFIG_FILE)
    for camera in yaml_data:
        if camera['name'] == camera_name: 
            return camera
    return False

def get_ip_address(camera): 
    """Get Camera IP address using the still url or stream source"""
    exp = r"(?:\d{1,3}\.)+(?:\d{1,3})"
    return re.findall(exp, camera['still_image_url'])[0] if camera['still_image_url'] != "" else re.findall(exp, camera['stream_source'])[0]

def get_url_with_credentials(camera: dict) -> str: 
    """Returns a url or a rtsp stream source with the credentials"""
    if f"//{camera['username']}:{camera['password']}@" in camera['stream_source']:
        return camera['stream_source']
    else: 
        return f"rtsp://{camera['username']}:{camera['password']}@{camera['stream_source'].replace('rtsp://', '')})"

def run_ffmpeg(rtsp_source, file_name, time, dryrun = DRYRUN) -> None:
    """Runs ffmpeg to record a video"""
    command = f"ffmpeg -i {rtsp_source} -t {time} -codec copy -vcodec copy -f mp4 {file_name}"
    log.info(f"Running command: {command}")
    if dryrun: 
        return
    os.popen(command)
    return


## --- I/O functions --- #

@pyscript_executor
def read_json_data(storage_file: str): 
    """Returns the json data from the storage file"""
    with open(storage_file, "r") as f:
        data = json.load(f)
    return data

@pyscript_executor
def write_json_data(storage_file: str, data: dict):
    """Writes the json data to the storage file"""
    with open(storage_file, "w") as f:
        json.dump(data, f, indent= 4)


@pyscript_executor
def read_yaml(fileName): 
    """Reads a yaml file and returns a dictionary"""
    
    if not fileName.endswith(".yaml"): 
        fileName += ".yaml" 
    
    with open(fileName, "r") as fh: 
        try: 
            yaml_map = yaml.load(fh)
        except yaml.YAMLError as exc:
            yaml_map = exc
    
    return yaml_map


@pyscript_executor
def write_yaml(yaml_map, output_file_name): 
    """Writes a dictionary to yaml file """
    
    if not output_file_name.endswith(".yaml"): 
        output_file_name += ".yaml" 
    
    with open(output_file_name, "w") as ofh: 
        yaml.dump(yaml_map, ofh)