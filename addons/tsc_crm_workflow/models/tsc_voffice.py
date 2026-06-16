import json
import logging
import requests
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class TscVofficeConfig(models.Model):
    _name = 'tsc.voffice.config'
    _description = _('VOffice Configuration')

    name = fields.Char(required=True, default='Default')
    api_url = fields.Char(
        string=_('API URL'),
        default='https://crm.laoid.net/apis',
        required=True,
    )
    api_user = fields.Char(string=_('Username'), required=True)
    api_password = fields.Char(string=_('Password'), required=True, groups='base.group_system')
    active = fields.Boolean(default=True)
    default_type_id = fields.Integer(string=_('Default Type ID'), default=0)
    default_area_id = fields.Integer(string=_('Default Area ID'), default=0)
    default_place = fields.Char(string=_('Default Place'), default='Vientiane')

    def _get_headers(self):
        self.ensure_one()
        return {
            'user': self.api_user,
            'password': self.api_password,
        }

    def test_connection(self):
        self.ensure_one()
        try:
            resp = requests.get(
                f"{self.api_url}/getListDocumentType",
                headers=self._get_headers(),
                timeout=30,
                verify=False,
            )
            if resp.status_code == 200:
                return {'type': 'ir.actions.client', 'tag': 'display_notification',
                        'params': {'title': _('Success'), 'message': _('Connection successful'), 'type': 'success'}}
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': _('Error'), 'message': _('Connection failed: %s') % resp.status_code, 'type': 'danger'}}
        except Exception as e:
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': _('Error'), 'message': str(e), 'type': 'danger'}}

    def get_document_types(self):
        self.ensure_one()
        resp = requests.get(
            f"{self.api_url}/getListDocumentType",
            headers=self._get_headers(),
            timeout=30,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()

    def search_employee(self, keyword):
        self.ensure_one()
        resp = requests.get(
            f"{self.api_url}/getEmployeeInfo/{keyword}",
            headers=self._get_headers(),
            timeout=30,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()

    def get_user_sign_roles(self, org_id=None):
        self.ensure_one()
        payload = {}
        if org_id:
            payload['orgId'] = org_id
        resp = requests.post(
            f"{self.api_url}/getListUserSignWithRole",
            headers=self._get_headers(),
            json=payload,
            timeout=30,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()

    def get_signature_image(self, employee_id, employee_code):
        self.ensure_one()
        resp = requests.get(
            f"{self.api_url}/getImageSign/{employee_id}/{employee_code}",
            headers=self._get_headers(),
            timeout=30,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()

    def upload_file(self, file_content, filename):
        self.ensure_one()
        resp = requests.post(
            f"{self.api_url}/files/upload",
            headers=self._get_headers(),
            files={'file': (filename, file_content)},
            timeout=60,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()

    def upload_document_to_sign(self, payload):
        self.ensure_one()
        resp = requests.post(
            f"{self.api_url}/uploadDocumentToSign",
            headers={**self._get_headers(), 'Content-Type': 'application/json'},
            json=payload,
            timeout=60,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()

    def send_and_sign(self, doc_id, trans_code):
        self.ensure_one()
        resp = requests.get(
            f"{self.api_url}/sendAndSign/{doc_id}/{trans_code}",
            headers=self._get_headers(),
            timeout=30,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()

    def get_document_detail(self, doc_id):
        self.ensure_one()
        resp = requests.get(
            f"{self.api_url}/getDocumentDetail/{doc_id}",
            headers=self._get_headers(),
            timeout=30,
            verify=False,
        )
        resp.raise_for_status()
        return resp.json()

    def get_signed_file(self, doc_id, file_path, storage):
        self.ensure_one()
        resp = requests.get(
            f"{self.api_url}/getFile",
            headers=self._get_headers(),
            params={'documentId': doc_id, 'filePath': file_path, 'storage': storage},
            timeout=60,
            verify=False,
        )
        resp.raise_for_status()
        return resp.content
