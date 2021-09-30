###Service to redirect user to homekit when a mobile device is used for login 

import os
#import time

@event_trigger('state_changed')
def homekit_redirect(**kwargs):
    """Redirects the user to the respective homekit-dashboard"""
    entity_id = kwargs.get('entity_id')
    old_state = kwargs.get('old_state')
    if old_state != None: 
        old_state_attributes = kwargs.get('old_state').as_dict()['attributes']
    else: 
        old_state_attributes = {'currentUser': 'None'} ##If its the first time a device is used for loggin in the user its set to None 
    
    if kwargs.get('new_state') != None:
        new_state_attributes = kwargs.get('new_state').as_dict()['attributes']

    if entity_id.split('.')[0] == 'sensor' and new_state_attributes.get('type') == 'browser_mod' and new_state_attributes.get('width') <= 600 and (old_state_attributes.get('currentUser') != new_state_attributes.get('currentUser') or old_state_attributes.get('visibility') != new_state_attributes.get('visibility') or old_state == None):
        ipAdress = get_machine_ip_adress()
        userName = new_state_attributes['currentUser'].lower().replace(' ', '-')
        deviceID = new_state_attributes['deviceID']
        navigationPath = f"http://{ipAdress}:8123/homekit-infused-{userName}/home"
        log.debug(f"Redirecting user to {navigationPath}")
        browser_mod.navigate(navigation_path = navigationPath, deviceID = deviceID)


def get_machine_ip_adress():
    """Get the machine IP adress"""
    stream = os.popen("hostname -I | awk '{print $1}'") 
    ip_address = stream.read()
    ip_address = ip_address.strip()
    return ip_address

###For Developers, kwards struture of a browser_mod event change
#**kwargs = 
#{'trigger_type': 'event', 'event_type': 'state_changed', 
# 'context': Context(user_id=None, parent_id=None, id='2f60d4484107d3dec5afa660b38e9095'), 'entity_id': 'sensor.browser_4988d1d2_4a34da33', 
# 'old_state': <state sensor.browser_4988d1d2_4a34da33=2; type=browser_mod, last_seen=2021-08-05T15:15:34.736769+01:00, deviceID=4988d1d2-4a34da33, path=/developer-tools/event, 
# visibility=hidden, userAgent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0, currentUser=owner, fullyKiosk=False, width=2144, height=1005, darkMode=True, 
# userData=id=6f284c8af2294017993e9c7dd44eba6a, name=owner, is_owner=True, is_admin=True, credentials=[{'auth_provider_type': 'homeassistant', 'auth_provider_id': None}], 
# mfa_modules=[{'id': 'totp', 'name': 'Authenticator app', 'enabled': False}], config=command=update @ 2021-08-05T15:07:43.984685+01:00>, 
# 'new_state': <state sensor.browser_4988d1d2_4a34da33=2; 
# type=browser_mod, last_seen=2021-08-05T15:15:40.777965+01:00, deviceID=4988d1d2-4a34da33, path=/config/integrations, visibility=hidden, userAgent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) 
# Gecko/20100101 Firefox/90.0, currentUser=owner, fullyKiosk=False, width=2144, height=1005, darkMode=True, userData=id=6f284c8af2294017993e9c7dd44eba6a, name=owner, is_owner=True, is_admin=True, 
# redentials=[{'auth_provider_type': 'homeassistant', 'auth_provider_id': None}], mfa_modules=[{'id': 'totp', 'name': 'Authenticator app', 'enabled': False}], 
# config=command=update @ 2021-08-05T15:07:43.984685+01:00>}