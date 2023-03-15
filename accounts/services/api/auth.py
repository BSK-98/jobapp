import frappe
import frappe.sessions

from accounts.accounting_app.services.api.config import config
config = Config()


class Auth:
    def get_csrf_token(self):
        config.self_login()['token']
        return frappe.generate_hash()
        return frappe.local.session.data