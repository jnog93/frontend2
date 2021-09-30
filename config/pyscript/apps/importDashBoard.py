import json
import os
import re

import yaml

################ Services #################

@service
def updateDashboardsAvaiable():
    """Updates the list of dashboards I can import to home kit
    This service is called each time a new dashboard is created and when homeassistant in initialized (there is a folder watcher in the .storage file)
    Instead of updating the list with the file, I prefer to scan the entire folder and get the list of dashboard""" 
    
    # Get the list of dashboard in storage mode (I need to take control of my dashboard in the dashboard tab first for the file to appear in .storage)
    storageFolder = pyscript.app_config['storage_folder']
    dashboardsAvaiable = [f for f in os.listdir(storageFolder) if os.path.isfile(os.path.join(storageFolder, f)) and (f.startswith('lovelace.lovelace') or f == 'lovelace')]
    dashBoardList = []

    """Make a list of the dashboards I can import
    The actualy name that shows in the front end is also altered"""
    for board in dashboardsAvaiable: 
        if board == 'lovelace': 
            dashBoardList.append('Overview')  #Let call the default dashboard Overview since there is no information in the file name or in other files (as far as I known)
        else: 
            board = board.replace('lovelace.lovelace_','')
            dashBoardList.append(board) 

    #Sort the list of dashboards (Overview always appears first in the list, due to capilalization)    
    dashBoardList.sort()


    dashboardConfig = readYaml(pyscript.app_config['homekit_dashboard_list_file'])
    dashboardConfig['options'] = dashBoardList
    writeToYaml(dashboardConfig, pyscript.app_config['homekit_dashboard_list_file'])
        

@service
def import_lovelace_dashBoard(dashboard_to_import = None, user = None): 
     #typecast to string is a good practice here
    dashboard_to_import = str(state.get(dashboard_to_import))
    user = str(state.get(user))  
    if dashboard_to_import == 'Overview': 
        dashboardStorageFile = '.storage/lovelace'
    else: 
        dashboardStorageFile = f'.storage/lovelace.lovelace_{dashboard_to_import}' #Sets the file to the lovelace file
    if user == 'owner': 
        viewConfigFile = pyscript.app_config['homekit_dashboard_view_file']
        HKIdashBoardGenerator = generateHKIdashbord(dashboardStorageFile, viewConfigFile) 
    else: 
        viewConfigFile = pyscript.app_config['homekit_dashboard_view_file'] + f"_{user.replace(' ', '_')}"
        HKIdashBoardGenerator = generateHKIdashbord(dashboardStorageFile, viewConfigFile, user) 
    HKIdashBoardGenerator.main() # Run the main function
    homeassistant.restart()



########### Dashboard Class ###############

class entity: 
    """Class that represents entity information"""
    def __init__(self, entities_id = None, title = None, aditionalInformation = None) -> None:
        self.entities_id = entities_id  #This will always be a single entity id
        self.title = title
        self.additionalInformation = [aditionalInformation] #additional information is a list of dictionaries

    def updateTitle(self, newTitle):
        """Updates the title of the entity"""
        if self.title == None: 
            self.title = newTitle

    def updateAdditionalInformation(self, newAdditionalInformation):
        """Update additional information list"""
        self.additionalInformation.append(newAdditionalInformation)
        

class generateHKIdashbord:  
    """Class used to convert a lovelace dashboard in the .storage/ files into a yaml file"""
    def __init__(self, lovelace_file, viewConfigFile, user = 'default') -> None:
        self.locelaceFile = lovelace_file
        self.viewConfigFile = viewConfigFile
        self.user = user
        self.json = readJsonStorage(self.locelaceFile)
        self.groupYaml = {}
        self.entities_supported = pyscript.app_config['entities_to_import']
        self.cards_to_import  = pyscript.app_config['cards_to_import']
        
    def get_entities(self) -> None:  
        """"Parse entities from json information"""
        viewData = self.json['data']['config']['views']
        self.data = {}
        for dashboardTab in viewData:
            #Process each dashboard
            dashboardTitle = dashboardTab['title']
            self.data[dashboardTitle] = {}

            """Gets all the entities in the dashboard
            as a dictionary of entities objects. 
            Internally verifies if the entity and button type is supported """
            self.entities = self.get_entities_in_dashboard(dashboardTab)  
            self.data[dashboardTitle]['entities'] = self.entities

    def get_entities_in_dashboard(self, dashboardTab) -> dict:
            """Get a dictionary of entities objects"""
            self.entities = {} #self entities is a dictionary of entities objects which is resered for each dashboard
            for card in dashboardTab['cards']: 
                if card['type'] not in self.cards_to_import:
                    log.warning(f'{card["type"]} card not (currently) supported')
                else:
                    #Parses button, light and entity card information
                    if card['type'] == "button" or card['type'] == "light" or card['type']  == 'entity': #Nota -> If there is a 'light' entity, do I want it to be interactive in the dashboard?
                        entity_id, title, additionalInformation = self.parse_button_card(card)
                        if entity_id not in self.entities: 
                            self.entities[entity_id] = entity(entity_id, title, additionalInformation)
                        else: 
                            self.entities[entity_id].updateAdditionalInformation(additionalInformation) #Updates the card type of the entity
                            if title != None: 
                                self.entities[entity_id].updateTitle(title) #Updates the title of the entity if there is none. This means the name in the leftest card is keept
                    
                    #Parses entities card information
                    elif card['type'] == 'entities': 
                        json_in_string = json.dumps(card) 
                        if "input_boolean.learning_mode_remote" in json_in_string: #Workaround to check if a card is a remote
                            entity_list = self.parse_remote_card(json.dumps(json_in_string)) 
                        else:  
                            entity_list = self.parse_entites_card(card)
                        #Interate through the list and add the entities to the entities map
                        for entity_info in entity_list:
                            if entity_info[0] not in self.entities:
                                self.entities[entity_info[0]] = entity(entity_info[0], entity_info[1], entity_info[2])
                            else: 
                                self.entities[entity_info[0]].updateAdditionalInformation(entity_info[2]) #Updates the card type of the entity
                                if entity_info[1] != None:
                                    self.entities[entity_info[0]].updateTitle(entity_info[1]) #Updates the title of the entity if there is none
                    
                    #Parse sensor card information
                    elif card['type'] == 'sensor': 
                        entity_id, title, additionalInformation = self.parse_sensor_card(card)
                        if entity_id not in self.entities:
                            self.entities[entity_id] = entity(entity_id, title, additionalInformation)
                        else: 
                            if title == None: 
                                self.entities[entity_id].updateTitle(title)    #Updates the title of the entity if there is none
                            if additionalInformation != None:
                                self.entities[entity_id].updateAdditionalInformation(additionalInformation)
                    
                    #Parse weather forecast card information
                    elif card['type'] == 'weather-forecast':
                        entity_id, title, additionalInformation = self.parse_weather_forecast_card(card)
                        if entity_id not in self.entities: 
                            self.entities[entity_id] = entity(entity_id, title, additionalInformation)
                        else: 
                            if title == None: 
                                self.entities[entity_id].updateTitle(title)    #Updates the title of the entity if there is none
                            if additionalInformation != None:
                                self.entities[entity_id].updateAdditionalInformation(additionalInformation)
                    
                    #Parse camera information 
                    elif 'camera_image' in card.keys():
                        entity_id, title, additionalInformation = self.parse_camera_card(card)
                        if entity_id not in self.entities: 
                            self.entities[entity_id] = entity(entity_id, title, additionalInformation)
                        else: 
                            if title == None: 
                                self.entities[entity_id].updateTitle(title)    #Updates the title of the entity if there is none
                            
                            #For now, I only want to get information about the first card for each camera entity
                            
                            # if additionalInformation != None:
                            #    self.entities[entity_id].updateAdditionalInformation(additionalInformation)

            return self.entities

    def truncate_name(self, name):
        """Some names will be to large for the dashboard. Truncante these names"""
        if len(name) > 19: 
            return name[:19]
        return name  

    def get_remote_type(self, json_string): 
        """Get remote type based on the number of occurented of custom:button-card. For now this approach works"""
        button_card_count = json_string.count('custom:button-card')
        if button_card_count == 9: 
            return 'ac'
        elif button_card_count == 24: 
            return 'tv'

    def parse_remote_card(self, json_string: str) -> list(tuple): 
        """Parse the remote cards added through the raceland IU dashboard. 
        Unlike other parsers, regular expression on a json.dumps in used instead of using dictionary"""
        entity = re.search('input_boolean.learning_mode_remote_\d*', json_string).group(0) 
        mac_address = re.search("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}", json_string).group(0)
        remote_type = self.get_remote_type(json_string) 
        title = f"Comando {remote_type}"
        additional_information = {'mac': mac_address, 'type': remote_type} 
        return [(entity, title, additional_information)] #We output a list of a tuple to ensure compatibility with the rest of entites cards 

    def parse_camera_card(self, card) -> list: 
        """Parses the camera card information (picture-entity or picture-glance card with a camera)"""
        if self.checkSupported(card['camera_image']):
            entity = card['camera_image']
        else: 
            entity = None
        if 'title' in card: 
            title = self.truncate_name(card['title']) 
        else: 
            title = None
        if 'camera_view' not in card.keys(): 
            camera_view = 'auto' 
        else: 
            camera_view = 'live'
        additionalInformation = {'camera_view' : camera_view}
        return (entity, title, additionalInformation)


    def parse_button_card(self, card) -> tuple:
        """Parses Buttons, lights, and entity"""
        if self.checkSupported(card['entity']): #Check if entity is supported
            entity = card['entity']
        else: 
            entity = None
        if 'name' in card: #This is an optional field
            title = self.truncate_name(card['name']) 
        else: 
            title = None
        additionalInformation = {'title': title, 'type': card['type']}
        return (entity, title, additionalInformation)


    def parse_entites_card(self, card) -> list: #returns a list of list with entity, title and additional information
        """Parses entities card information"""
        entities = []
        nameCounter = 1
        for entity_id in card['entities']:
            if type(entity_id) == dict: 
                entity_id = entity_id['entity'] 
            if self.checkSupported(entity_id):
                if 'title' in card: 
                    title = self.truncate_name(f'{card["title"]} {nameCounter}')
                    nameCounter += 1
                else: 
                    title = None
                additional_information = {title: 'title', 'type': card['type']}
                entities.append([entity_id, title, additional_information])
        return entities
    
    def parse_sensor_card(self, card) -> tuple:
        """Parses sensor cards"""
        if self.checkSupported(card['entity']): #Check if entity is supported 
            entity = card['entity']
        else:
            entity =  None
        
        if 'name' in card: #This is an optional field
            title = self.truncate_name(card['name']) 
        else: 
            title = None
        
        #Get additional information 
        additionalInformation = {} 
        for key, value in card.items():
            if key != 'entity':
                additionalInformation[key] = value

        return (entity, title, additionalInformation)
    
    
    def parse_weather_forecast_card(self, card) -> tuple:
        """Parse weather forecast card information"""
        if self.checkSupported(card['entity']): #Check if entity is supported
            entity = card['entity']
        else: 
            entity = None
        if 'name' in card: #This is an optional field
            title = self.truncate_name(card['name']) 
        else: 
            title = None
        additionalInformation = {} 
        for key, value in card.items():
            if key != 'entity' or key != 'name':
                additionalInformation[key] = value
        return (entity, title, additionalInformation)

    def checkSupported(self, entity_id) -> bool: 
        """Checks if the entity is supported"""
        entity_type = entity_id.split('.')[0]
        if entity_type not in self.entities_supported: 
            log.warning(f'{entity_type} entities are not supported by this service')
            return False
        return True


    def update_view_config(self): 
        """Write entity information to ViewConfig File"""
        viewConfigYaml = readYaml(self.viewConfigFile)
        #Remove any information from the view config file related to dashboards
        viewConfigKey = list(viewConfigYaml.keys())[0] #This file only has one key
        for view in list(viewConfigYaml[viewConfigKey]): #Converting to list to be able to remove elements from the dictionary (forcing python to make a copy of the dictionary keys) 
            if view.startswith('room'): #check if is a room that should be writen to the config file
                del viewConfigYaml[viewConfigKey][view] #remove the view
        
        """Loop through each dashboard and add the entities to the view config file
        I could avoid this loop, but I think it's better to keep the code more readable"""
        roomKeyCounter = 1
        self.lightGroup = [] #Keeps track of all the lights in the dashboard
        for dashboardName in self.data.keys():
            #Fill the information of the room
            information = {} 
            information['icon'] = self.getIcon(dashboardName)
            information['title'] = dashboardName
            information['show_in_favorites'] = 'true'
            information['devices'] =  []
            information['graphs'] = [] 
            information['weather'] = []
            information['cameras'] = [] 
            information['remote_control'] = []

            #create lists for each device category
            swichLightInfo = {'title': f'Luzes {dashboardName}', 'entities' : []} #For now switches and lights are in the same category
            sensorInfo = {'title': f'Sensores {dashboardName}', 'entities' : []}  #Deals with all the sensors that are not graphs (entity or sensor with graph == 'None') 
            graphInfo = {'title': f'Gráficos {dashboardName}', 'columns': 2, 'entities' : []}   #For graphs (sensors with graphs != 'None')
            cameraInfo = {'title': f'Câmaras {dashboardName}', 'entities' : []}  #For cameras
            remote_info = []
            #Loop through the entities in a dashboard
            for entity in self.data[dashboardName]['entities'].values(): #self.data[dashboardName]['entities'] is a dictionary of entities objects 
                entity_id = entity.entities_id
                log.info(entity_id)
                entity_states = hass.states.get(entity_id).as_dict() #Get the states of the entity
                entityAdditionalInformation = entity.additionalInformation
                categoryName = None
                #Set the entity title in the dashboard (Sensor titles are dealt in a separate function) 
                entity_title = self.get_entity_title(entity.title, entity_states) 
               
                #Get information about lights and switches
                if entity_id.startswith('light') or entity_id.startswith('switch'):
                    entity_information = self.addSwitchLightEntity(entity_id, entity_title, entity_states, dashboardName)  #Get the entity information
                    categoryName = 'lights'
                
                if categoryName == 'lights':
                    swichLightInfo['entities'].append(entity_information)
                    if entity_information['entity'] not in self.lightGroup:
                        self.lightGroup.append(entity_information['entity'])

                #Get information about sensors (the same sensor entity can have several cards and I want to show them all in the dashboard) 
                if entity_id.startswith('sensor'): 
                    if entityAdditionalInformation != []:
                        for cardInformation in entityAdditionalInformation: 
                            #Deals with simple sensors (sensor with no graph)
                            if cardInformation['type'] == 'entity' or 'graph' not in cardInformation: 
                                entity_information = self.addSensor(entity_id, cardInformation, entity_states, dashboardName)
                                categoryName = 'simple_sensor'
                            elif cardInformation['type'] == 'sensor' and 'graph' in cardInformation: 
                                entity_information = self.addSensorGraph(entity_id, cardInformation, entity_states, dashboardName)
                                categoryName = 'sensor_graph'
                            
                            #Add the information to the respective list 
                            if categoryName == 'simple_sensor':
                                sensorInfo['entities'].append(entity_information)
                            if categoryName == 'sensor_graph': 
                                graphInfo['entities'].append(entity_information)

                    if entityAdditionalInformation == []: #If the sensor is only in an entity card
                        entity_information = self.addSensor(entity_id, {'name': entity_title}, entity_states, dashboardName)
                        categoryName = 'simple_sensor'
                        if categoryName == 'simple_sensor':
                            sensorInfo['entities'].append(entity_information)

                if entity_id.startswith('weather'): 
                    weatherInfo = {'title': f"Previsão do tempo {entity_id.split('.')[1]}", 'entity': entity_id}
                    if 'show_forecast' in entityAdditionalInformation: 
                        weatherInfo['show_forecast'] = str(entityAdditionalInformation['show_forecast']) 
                    information['weather'].append(weatherInfo)
                        
                if entity_id.startswith('camera'):
                    cameraInfo['entities'].append(self.add_cameras(entity_id, entity_title, entityAdditionalInformation))
                
                if entity_id.startswith('input_boolean'):
                    entityAdditionalInformation = entityAdditionalInformation[0]
                    remote_info.append({'title': entity_title, 'input_boolean': entity_id, 'type': entityAdditionalInformation['type'], 'mac': entityAdditionalInformation['mac']})
                
            if (swichLightInfo['entities'] != []):
                information['devices'].append(swichLightInfo)
            if (sensorInfo['entities'] != []):
                information['devices'].append(sensorInfo)
            if (graphInfo['entities'] != []):
                information['graphs'].append(graphInfo)
            if information['weather'] == []:
                del information['weather'] #If there is no weather information, remove it from the list. If we keep it it will render an wrro in the dashboard
            if cameraInfo['entities'] != []:
                n_collums = self.get_camera_collum_number(cameraInfo['entities'])
                cameraInfo['columns'] = n_collums
                information['cameras'].append(cameraInfo)
            if remote_info != []: 
                information['remote_control'] = remote_info 

            #Add the information to the view config map
            viewConfigYaml[viewConfigKey][f'room_{roomKeyCounter}'] = information
            roomKeyCounter += 1
        
        #Finally, write the information to the yaml file
        writeToYaml(viewConfigYaml, self.viewConfigFile)

    def get_entity_title(self, title, entity_states)-> str: 
        """Get the entity title to use in the card. 
        1 - takes the title parsed (in the dashboard card) 
        2 - takes the devices friendly name if there is no parse title
        3 - returns none if there is not friendly name"""
        if title != None:      
            return title
        elif 'friendly_name' in entity_states['attributes'].keys():
            return entity_states['attributes']['friendly_name']
        return None

    def get_camera_collum_number(self, cameraInfoList) -> int:
        """Get the number of collums that will be used to render the camera cards, based on the number of cameras in the dashboard"""
        if len(cameraInfoList) >= 2: 
            return 2 
        return 1 

    def addSwitchLightEntity(self, entity_id, entity_title, states, dashboardName) -> dict: 
        """Add an entity of swich or light"""
        entity_information = {}
        entity_information['entity'] = entity_id
        if entity_title == None: 
            entity_title = f'Luz {dashboardName}'
        entity_information['name'] = entity_title
        if 'supported_color_modes' in states['attributes'].keys(): 
            if 'hs' in states['attributes']['supported_color_modes']:
                entity_information['type'] = 'rgb'
            if 'brightness' in states['attributes']['supported_color_modes']: 
                entity_information['type'] = 'brightness'
        return entity_information

    def addSensor(self, entity_id, cardInformation, entity_states, dashboardName) -> dict:
        """Add an sensor entity without graph"""
        entity_information = {} 
        entity_information['entity'] = entity_id
        entity_information['type'] = 'sensor'
        if 'name' in cardInformation:
            entity_information['name'] = cardInformation['name']
        elif 'friendly_name' in entity_states['attributes'].keys():
            entity_information['name'] = entity_states['attributes']['friendly_name']
        else:
            entity_information['name'] = f'Sensor {dashboardName}'
        return entity_information
    
    def addSensorGraph(self, entity_id, cardInformation, entity_states, dashboardName): 
        """Add a graph sensor"""
        entity_information = {}
        entity_information['entity'] = entity_id
        if 'name' in cardInformation:
            entity_information['name'] = cardInformation['name']
        elif 'friendly_name' in entity_states['attributes'].keys():
            entity_information['name'] = entity_states['attributes']['friendly_name']
        else:
            entity_information['name'] = f'Sensor {dashboardName}'
        entity_information['type'] = 'line'
        if 'hours_to_show' in cardInformation: 
            entity_information['hours_to_show'] = cardInformation['hours_to_show']
        else: 
            entity_information['hours_to_show'] = 24 #Default value
        return entity_information


    def add_cameras(self, entity_id, entity_title, entityAdditionalInformation):
        """Add information about cameras to the view config file"""
        camera_view = entityAdditionalInformation[0]['camera_view']
        entity_information = {
            'entity': entity_id,
            'camera_view': camera_view,
            'name': entity_title
        }
        return entity_information

    def getIcon(self, dashBoardName): 
        """Get icon depending on the name of the room"""
        return 'mdi:door' #For now use this as a fallback
    
    def setGroups(self):
        """Set entities in the groups, in order o keep track of the correct entities in the header""" 
        deviceCounterFile = pyscript.app_config['devive_counter_file']
        deviceCounterMap = readYaml(deviceCounterFile) 
        #Set key suffix (in order to write to the correct key in the yaml file) 
        if self.user != 'default': 
            keySuffix = f'_{self.user}' 
        else: 
            keySuffix = ''
        #Add the entities to the repective groups
        if self.lightGroup != []: 
            deviceCounterMap[f'all_light_entities{keySuffix}']['entities'] = self.lightGroup
        
        writeToYaml(deviceCounterMap, deviceCounterFile)

    def main(self): 
        """Main function"""
        self.get_entities()
        self.update_view_config()
        self.setGroups() 

###Pyscript I/O functions (@pyscrip executor decorators is required because input and output is supported by pyscript)
@pyscript_executor
def readYaml(fileName) -> dict: 
    """Reads a yaml file and returns a dictionary"""
    
    if not fileName.endswith('.yaml'): 
        fileName += '.yaml' 
    
    if not fileName.startswith('/'): 
        fileName += '/' + fileName
    
    with open(fileName) as fh: 
        try: 
            yaml_map = yaml.safe_load(fh)
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


@pyscript_executor
def readJsonStorage(dashboard_storage_file): 
    """Reads a json file and returns a dictionary"""
    
    with open(dashboard_storage_file) as fh: 
        try: 
            json_map = json.load(fh)
        except json.JSONDecodeError as exc:
            json_map = exc
    
    return json_map
