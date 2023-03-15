import frappe
import requests
import json


class Config:

    # static variables
    success = 200
    failed = 205
    conflict = 409
    failed_message = "Request failed"

    def all_fields(self):
        return 'fields=["*"]'

    # configure url

    def url(self, params=''):
        return f'{frappe.conf.get("admin_url")}/api/resource/{params}'

    def login(self, username, password):
        data_content = {"usr": username, "pwd": password}
        try:
            response = requests.post(
                f'{frappe.conf.get("admin_url")}/api/method/login',
                data=json.dumps(data_content),
                headers=self.config_headers('', False)
            )
            if response.status_code == 200:
                return self.set_response(self.success, {'status': 200, 'token': response.headers.__getitem__('Set-Cookie')})
        except:
            return self.set_response(self.failed, "Could not login")

    def self_login(self):
        usr = frappe.conf.get('admin_user')
        pwd = frappe.conf.get('admin_password')
        return self.login(usr, pwd)

    # configure headers

    def config_headers(self, cookie='', has_cookie=True):
        if has_cookie:
            return {'Accept': 'application/json', 'Content-Type': 'application/json', 'Cookie': cookie}
        else:
            return {'Accept': 'application/json', 'Content-Type': 'application/json'}

    # function to set response
    def set_response(self, code, data):
        frappe.response.http_status_code = code
        return data

    # to get data
    def get_data(self, cookie, doctype, filters=''):
        if filters != '':
            full_filters = f'/?{filters}'
        else:
            full_filters = ''
        try:
            req = requests.get(
                self.url(f"{doctype}{full_filters}"),
                headers=self.config_headers(cookie)
            )
            return req.json()
        except:
            return False

    # to get data
    def get_single_doctype_data(self, cookie, doctype):
        try:
            req = requests.get(
                self.url(f"{doctype}/{doctype}"),
                headers=self.config_headers(cookie)
            )
            return req.json()
        except:
            return False

    def get_doc(self, cookie, doctype, doc, filters=''):
        if filters != '':
            full_filters = f'/?{filters}'
        else:
            full_filters = ''
        req = requests.get(
            self.url(f"{doctype}/{doc}{full_filters}"),
            headers=self.config_headers(cookie)
        )
        return req.json()

    # post new data data to the doctype

    def post_data(self, cookie, data, doctype):
        return requests.post(self.url(doctype), data=json.dumps(
            data), headers=self.config_headers(cookie)).json()

    def update_data(self, cookie, data, doctype, document):
        res = requests.put(f"{self.url(doctype)}/{document}",
                           data=json.dumps(data), headers=self.config_headers(cookie)).json()
        return res

    def get_child_table_data(self, doctype, child, fields=[], filters=''):
        field_list = []
        for field in fields:
            field_list.append(f"`tab{child}`.{field}")
        return self.get_data(self.self_login()['token'], doctype, f'fields={json.dumps(field_list)}{filters}')
