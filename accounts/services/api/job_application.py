import frappe

from accounts.services.api.config import Config
from accounts.services.api.constants import doctypes
from accounts.services.doctype.job_application import JobApplication

config = Config()
cookie = config.self_login()['token']

class ApiCreation:
    def new_job_application(self, data):
        data_content = {
            "name": data.name,
            "email": data.email,
            "contact": data.contact,
            "nrc": data.nrc,
            "nationality":data.nationality,
            "qualifications":data.qualifications,
            # 'status': 1,
        }
        res = config.post_data(cookie, data_content, JobApplication)
        return config.set_response(config.success, res)
