"""Scripts to add deepstack objects entities to homeassistant using the frontend. Does I/O of entities in the yaml file"""

DEEPSTACK_CONFIG_FILE = pyscript.app_config["deepstack_yaml"]
INPUT_SELECT_CONFIGURED_CAMERAS = pyscript.app_config["registered_cameras"]
INPUT_TEXT_CURRENT_CAMERA_ENTITY_ID = pyscript.app_config["current_camera_entity_id"]
FACE_RECOGNITION_PREVIEW_FOLDER = pyscript.app_config["teach_face_preview_folder"] #This folder is used to save images that will show in the frontend and the preview for the facial recognition software. Also used to train new faces
NOTIFICATION_TITLE = "Raceland Camera AI"


import json
import yaml
import slugify
import os

## ----- Services ---- #####


@service("raceland_cameras.manage_deepstack_entities")
def manage_deepstack_entities(
    camera_entity,
    object_ai_bool, 
    face_ai_bool,
    ip_address_object,
    ip_address_face, 
    detect_person_bool,
    detect_person_bool_confidence,
    detect_animal_bool,
    detect_animal_bool_confidence,
    detect_vehicle_bool,
    detect_vehicle_bool_confidence,
    detect_others_bool,
    detect_others_bool_confidence, 
    detect_only_face_bool):
    """Add/updates deepstack entities. Divides into 2 subfunction, which are also registered as services"""
    #If the camera entity is == to None then return and end the function
    #Important: typecast to states to strings
    camera_entity = slugify.slugify(str(state.get(camera_entity)), separator= "_")
    object_ai_bool = str(state.get(object_ai_bool))
    face_ai_bool = str(state.get(face_ai_bool))
    ip_address_object = str(state.get(ip_address_object)).strip()
    ip_address_face = str(state.get(ip_address_face)).strip()
    detect_person_bool = str(state.get(detect_person_bool))
    detect_person_bool_confidence = str(state.get(detect_person_bool_confidence))
    detect_animal_bool = str(state.get(detect_animal_bool))
    detect_animal_bool_confidence = str(state.get(detect_animal_bool_confidence))
    detect_vehicle_bool = str(state.get(detect_vehicle_bool))
    detect_vehicle_bool_confidence = str(state.get(detect_vehicle_bool_confidence))
    detect_others_bool = str(state.get(detect_others_bool))
    detect_others_bool_confidence = str(state.get(detect_others_bool_confidence))
    detect_only_face_bool = str(state.get(detect_only_face_bool))
 
    #If no camera entity is picked finish the execution wihtout restarting
    if camera_entity == 'none': 
        return

    #Update/add deepstack objects entity
    manage_deepstack_object(camera_entity,
                            object_ai_bool, 
                            ip_address_object,
                            detect_person_bool,
                            detect_person_bool_confidence,
                            detect_animal_bool,
                            detect_animal_bool_confidence,
                            detect_vehicle_bool,
                            detect_vehicle_bool_confidence,
                            detect_others_bool,
                            detect_others_bool_confidence)

    #Add/update deepstack face entity
    manage_deepstack_face_recognition(camera_entity,
                                      face_ai_bool,
                                      ip_address_face,
                                      detect_only_face_bool)

    homeassistant.restart()

@service("raceland_cameras.manage_deepstack_object")
def manage_deepstack_object(
    camera_entity,
    object_ai_bool, 
    ip_address,
    detect_person_bool,
    detect_person_bool_confidence,
    detect_animal_bool,
    detect_animal_bool_confidence,
    detect_vehicle_bool,
    detect_vehicle_bool_confidence,
    detect_others_bool,
    detect_others_bool_confidence):
    """Add/update a deepstack object entity"""

    ##Check if the entity is already registered
    putative_object_name = f"image_processing.deepstack_object_{camera_entity}"
    image_processing_list = get_image_processing_entities_list()
    deepstack_object_entities = [object for object in image_processing_list if object.startswith("image_processing.deepstack_object")]
    if putative_object_name in deepstack_object_entities:
        update_deepstack_object_entity(
            object_ai_bool,
            camera_entity,
            ip_address,
            detect_person_bool,
            detect_person_bool_confidence,
            detect_animal_bool,
            detect_animal_bool_confidence,
            detect_vehicle_bool,
            detect_vehicle_bool_confidence,
            detect_others_bool,
            detect_others_bool_confidence)

    elif object_ai_bool == "on":
        add_deepstack_object_entity(
            camera_entity,
            ip_address,
            detect_person_bool,
            detect_person_bool_confidence,
            detect_animal_bool,
            detect_animal_bool_confidence,
            detect_vehicle_bool,
            detect_vehicle_bool_confidence,
            detect_others_bool,
            detect_others_bool_confidence)
                

@service("raceland_cameras.manage_deepstack_face_recognition")
def manage_deepstack_face_recognition(
    camera_entity,
    face_ai_bool,
    ip_address_face,
    detect_only_face_bool): 
    """Add/update a deepstack face entity"""

    putative_object_name = f"image_processing.deepstack_face_{camera_entity}"  
    image_processing_list = get_image_processing_entities_list()
    deepstack_face_recognition_entities = [object for object in image_processing_list if object.startswith("image_processing.deepstack_face")]
    if putative_object_name in deepstack_face_recognition_entities:
        update_deepstack_face_entity(camera_entity, face_ai_bool, ip_address_face, detect_only_face_bool)
    
    elif face_ai_bool == "on": 
        add_deepstack_face_entity(camera_entity, ip_address_face, detect_only_face_bool)


@service("raceland_cameras.take_screenshot")
def screenshot_wrapper(): 
    """Take a screenshot with the currently seelcted camera and save it under FACE_RECOGNITION_PREVIEW_FOLDER. Saves the image either as camera_name_screenshot or 
    camera_name_screenshot_2. This is a workaround since subscribing the image will not update the frontend preview"""
    camera_entity = slugify.slugify(str(state.get(INPUT_SELECT_CONFIGURED_CAMERAS)), separator = '_')
    list_of_files = os.listdir(FACE_RECOGNITION_PREVIEW_FOLDER)
    if f"{camera_entity}_screenshot.png" in list_of_files: 
        camera.snapshot(entity_id = f"camera.{camera_entity}", filename = f"{FACE_RECOGNITION_PREVIEW_FOLDER}{camera_entity}_screenshot_2.png", blocking=True)
        os.remove(f"{FACE_RECOGNITION_PREVIEW_FOLDER}{camera_entity}_screenshot.png")
    else: 
        camera.snapshot(entity_id = f"camera.{camera_entity}", filename = f"{FACE_RECOGNITION_PREVIEW_FOLDER}{camera_entity}_screenshot.png", blocking=True)
        if f"{camera_entity}_screenshot_2.png" in list_of_files: 
            os.remove(f"{FACE_RECOGNITION_PREVIEW_FOLDER}{camera_entity}_screenshot_2.png")

    update_teach_face_preview_picture() #call this function to update the preview image path

@service("raceland_cameras.teach_face")
def teach_face(image_path, person_name): 
    """Wrapper around the teach face service. Sets the image to the image path and the name to person name."""

    #Typecast to string 
    image_path = str(state.get(image_path)).replace("/local", "/config/www")
    person_name = str(state.get(person_name)).strip()

    #Check if the image path is valid 
    if not os.path.isfile(image_path):
        log.error(f"The image path {image_path} is not valid")
    if person_name == '':
        log.error(f"The person name {person_name} is not valid. Provide a person-name")
    
    deepstack_face.teach_face(name = person_name, file_path = image_path)
    


### --- Helper functions --- ###


def add_deepstack_object_entity(
    camera_entity,
    ip_address,
    detect_person_bool,
    detect_person_bool_confidence,
    detect_animal_bool,
    detect_animal_bool_confidence,
    detect_vehicle_bool,
    detect_vehicle_bool_confidence,
    detect_others_bool,
    detect_others_bool_confidence) : 
    """Add a deepstack object entity"""

    target_list = get_object_target_list(detect_person_bool, detect_person_bool_confidence, detect_animal_bool, detect_animal_bool_confidence, 
                    detect_vehicle_bool, detect_vehicle_bool_confidence, detect_others_bool, detect_others_bool_confidence)

    deepstack_camera = {
        'platform': 'deepstack_object', 
        'ip_address': get_ip_address(ip_address),
        'roi_x_max': 1,
        'roi_y_max': 1,
        'port': 80,
        'save_file_folder': '/config/www/camera_screenshots',
        'save_file_format': 'png',
        'save_timestamped_file': True,
        'always_save_latest_file': True,
        'source': [{'entity_id': f"camera.{camera_entity}"}],
        'targets': target_list
    }

    #Save the entity to the deepstack yaml file
    deepstack_yaml = read_yaml(DEEPSTACK_CONFIG_FILE)
    deepstack_yaml.append(deepstack_camera)
    write_yaml(deepstack_yaml, DEEPSTACK_CONFIG_FILE)



def update_deepstack_object_entity(
    object_ai_bool,
    camera_entity,
    ip_address,
    detect_person_bool,
    detect_person_bool_confidence,
    detect_animal_bool,
    detect_animal_bool_confidence,
    detect_vehicle_bool,
    detect_vehicle_bool_confidence,
    detect_others_bool,
    detect_others_bool_confidence): 
    """Update a deepstack a object entity"""
    
    deepstack_map = read_yaml(DEEPSTACK_CONFIG_FILE)
    for i in range(len(deepstack_map)):
        if f"camera.{camera_entity}" == deepstack_map[i]['source'][0]['entity_id'] and deepstack_map[i]["platform"] == "deepstack_object": 
            break #After getting the index stop the execution
    
    #If the input_bool is turned off then remove the object from the list
    if object_ai_bool == "off":
        deepstack_map.pop(i)
    
    #Else update the entity
    else:
        new_target_list = get_object_target_list(
            detect_person_bool, 
            detect_person_bool_confidence, 
            detect_animal_bool, 
            detect_animal_bool_confidence, 
            detect_vehicle_bool, 
            detect_vehicle_bool_confidence, 
            detect_others_bool, 
            detect_others_bool_confidence)
        
        deepstack_map[i]['targets'] = new_target_list
        deepstack_map[i]['ip_address'] = get_ip_address(ip_address)

    #Save the file            
    write_yaml(deepstack_map, DEEPSTACK_CONFIG_FILE)


def add_deepstack_face_entity(camera_entity, ip_address_face, detect_only_face_bool): 
    """Add a deepstack face entity"""
    face_entity = {
        'platform': 'deepstack_face',
        'ip_address': get_ip_address(ip_address_face),
        'port': 80, 
        'save_file_folder': '/config/www/facial_recognition',
        #'save_faces_folder': '/config/www/facial_recognition/', 
        'save_timestamped_file': True,
        'save_faces': False,
        'detect_only': input_bool_to_bool(detect_only_face_bool),
        'source': [{'entity_id': f"camera.{camera_entity}"}]
    }

    #Save the entity to the deepstack yaml file
    deepstack_yaml = read_yaml(DEEPSTACK_CONFIG_FILE)
    deepstack_yaml.append(face_entity)
    write_yaml(deepstack_yaml, DEEPSTACK_CONFIG_FILE)


def update_deepstack_face_entity(camera_entity, face_ai_bool, ip_address, detect_only_face_bool):
    """Update a deepstack a object entity"""
    
    deepstack_yaml = read_yaml(DEEPSTACK_CONFIG_FILE)
    for i in range(len(deepstack_yaml)):
        if f"camera.{camera_entity}" == deepstack_yaml[i]['source'][0]['entity_id'] and deepstack_yaml[i]["platform"] == "deepstack_face": 
            break #After getting the index stop the execution

    #If the input_bool is turned off then remove the object from the list
    if face_ai_bool == "off":
        deepstack_yaml.pop(i)
    
    #Else update the entity
    else:
        deepstack_yaml[i]['detect_only'] = input_bool_to_bool(detect_only_face_bool)
        deepstack_yaml[i]['ip_address'] = get_ip_address(ip_address)

    #Save the file            
    write_yaml(deepstack_yaml, DEEPSTACK_CONFIG_FILE)


def input_bool_to_bool(input_bool_state:str) -> bool:
    """Convert the input string to bool"""
    return True if input_bool_state == "on" else False

def get_ip_address(ip_address:str) -> str: 
    """Get ip_address. Return localhost as a default"""
    return 'localhost' if ip_address == '' else ip_address


def get_image_processing_entities_list():
    """Return a list of the image processing entities. If there are no entities return and empty_list with 'placeholder'.
    This workaround is required to do list comprehension on empty lists with pyscript"""
    return ['placeholder'] if state.names(domain="image_processing") == [] else state.names(domain="image_processing")


def get_object_target_list(
    detect_person_bool, detect_person_bool_confidence, detect_animal_bool, detect_animal_bool_confidence, 
    detect_vehicle_bool, detect_vehicle_bool_confidence, detect_others_bool, detect_others_bool_confidence) -> list: 
    """Get the target list for a deepstack object"""

    target_list = []
    if detect_person_bool == "on":
        target_list.append({"target": "person", "confidence": detect_person_bool_confidence})
    if detect_animal_bool == "on":
        target_list.append({"target": "animal", "confidence": detect_animal_bool_confidence})
    if detect_vehicle_bool == "on":
        target_list.append({"target": "vehicle", "confidence": detect_vehicle_bool_confidence})
    if detect_others_bool == "on":
        target_list.append({"target": "others", "confidence": detect_others_bool_confidence})
    
    return target_list


## ------- Automations ------- ###

@state_trigger(INPUT_SELECT_CONFIGURED_CAMERAS)
def update_input_text_entities():
    """Update the information in the frontend information when selecting a new camera"""
    camera_entity_id = f"camera.{slugify.slugify(str(state.get(INPUT_SELECT_CONFIGURED_CAMERAS)), separator = '_')}"
    deepstack_yaml = read_yaml(DEEPSTACK_CONFIG_FILE)
    bool_objects = False
    bool_target_person = False
    bool_target_animals = False
    bool_target_vehicle = False
    bool_target_others = False
    bool_face = False
    bool_detect_only = False
    
    for deepstack_entity in deepstack_yaml:
        if camera_entity_id == deepstack_entity['source'][0]['entity_id']:
            #updates the deepstack_object 
            if deepstack_entity["platform"] == "deepstack_object":
                bool_objects = True
                state.set('input_boolean.camera_form_ai', value = "on")
                if deepstack_entity["ip_address"] == 'localhost':
                    state.set("input_text.ai_form_object_ip_address", value = "")
                else: 
                    state.set("input_text.ai_form_object_ip_address", value = deepstack_entity["ip_address"])
                for target in deepstack_entity["targets"]:
                    if target["target"] == "person":
                        state.set("input_boolean.ai_form_detect_person", value = "on")
                        state.set("input_number.ai_form_detect_person_confidence", value = target["confidence"])
                        bool_target_person = True
                    elif target["target"] == "animal":
                        state.set("input_boolean.ai_form_detect_animal", value = "on")
                        state.set("input_number.ai_form_detect_animal_confidence", value = target["confidence"])
                        bool_target_animals = True
                    elif target["target"] == "vehicle":
                        state.set("input_boolean.ai_form_detect_vehicle", value = "on")
                        state.set("input_number.ai_form_detect_vehicle_confidence", value = target["confidence"])
                        bool_target_vehicle = True
                    elif target["target"] == "others":
                        state.set("input_boolean.ai_form_detect_others", value = "on")
                        state.set("input_number.ai_form_detect_others_confidence", value = target["confidence"])
                        bool_target_others = True

            #updates the deepstack_face  
            elif deepstack_entity["platform"] == "deepstack_face":
                bool_face = True
                bool_detect_only = True
                state.set('input_boolean.camera_form_facial_recognition', value = "on")
                if deepstack_entity["ip_address"] == 'localhost':
                    state.set("input_text.ai_face_form_ip_address", value = "")
                else: 
                    state.set("input_text.ai_face_form_ip_address", value = deepstack_entity["ip_address"])
                if deepstack_entity["detect_only"] == False:
                    state.set("input_boolean.ai_face_form_detect_only", value = "off")
                else: 
                    state.set("input_boolean.ai_form_detect_only", value = "on") 
                
    #If the option was not found on the list then set the states to off
    #Object options
    if bool_objects == False: 
        state.set('input_boolean.camera_form_ai', value = "off")
    if bool_target_person == False:
        state.set('input_boolean.ai_form_detect_person', value = "off")
    if bool_target_animals == False:
        state.set('input_boolean.ai_form_detect_animal', value = "off")
    if bool_target_vehicle == False:
        state.set('input_boolean.ai_form_detect_vehicle', value = "off")
    if bool_target_others == False:
        state.set('input_boolean.ai_form_detect_others', value = "off")

    #Face options
    if bool_face == False:
        state.set('input_boolean.camera_form_facial_recognition', value = "off")
    if bool_detect_only == False: 
        state.set('input_boolean.ai_face_form_detect_only', value = "off")


@state_trigger(INPUT_SELECT_CONFIGURED_CAMERAS)
def update_teach_face_preview_picture(): 
    """Updates the path to the preview picture on the camera. The previewed picture will be used with the teach_face service"""
    base_path = FACE_RECOGNITION_PREVIEW_FOLDER.replace("/config/www", "/local")
    camera_screenshot_image = f"{slugify.slugify(state.get(INPUT_SELECT_CONFIGURED_CAMERAS), separator = '_')}_screenshot"
    if f"{camera_screenshot_image}.png" in os.listdir(FACE_RECOGNITION_PREVIEW_FOLDER): 
        state.set(INPUT_TEXT_CURRENT_CAMERA_ENTITY_ID, value = f"{base_path}{camera_screenshot_image}.png")
    else: 
        state.set(INPUT_TEXT_CURRENT_CAMERA_ENTITY_ID, value = f"{base_path}{camera_screenshot_image}_2.png")


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