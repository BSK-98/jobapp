import frappe
import requests
import json

#from accounts.config import Config
from accounts.services.api.config import Config
from accounts.services.api.auth import auth
#from accounts.auth import Auth
#from accounts.api.job_application import ApiCreation
from accounts.services.api.job_application import ApiCreation


# initialize object classes
config = Config()
auth = auth()
job_application = ApiCreation()


success = 200
failed = 205
conflict = 409
failed_message = "Request failed"


@frappe.whitelist(allow_guest=True)
def login(username, password):
        data_content = {"usr": username, "pwd": password}
        try:
            response = requests.post(
                f'{frappe.conf.get("admin_url")}/api/method/login',
                data=json.dumps(data_content),
                headers=config_headers('', False)
            )
            if response.status_code == 200:
                return set_response(success, {'status': 200, 'token': response.headers.__getitem__('Set-Cookie')})
        except:
            return set_response(failed, "Could not login")



def config_headers(cookie='', has_cookie=True):
    if has_cookie:
        return {'Accept': 'application/json', 'Content-Type': 'application/json', 'Cookie': cookie}
    else:
        return {'Accept': 'application/json', 'Content-Type': 'application/json'}

def set_response(code, data):
    frappe.response.http_status_code = code
    return data