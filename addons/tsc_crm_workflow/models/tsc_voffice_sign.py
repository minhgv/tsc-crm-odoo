import json
import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class TscVofficeSign(models.Model):
    _name = 'tsc.voffice.sign'
    _description = _('VOffice Signing Record')
    _order = 'id desc'

    contract_id = fields.Many2one('tsc.contract', string=_('Contract'), ondelete='cascade')
    voffice_config_id = fields.Many2one('tsc.voffice.config', string=_('VOffice Config'), required=True)
    doc_id = fields.Char(string=_('VOffice Doc ID'), readonly=True)
    trans_code = fields.Char(string=_('Trans Code'), readonly=True)
    status = fields.Selection([
        ('draft', _('Draft')),
        ('uploaded', _('Uploaded')),
        ('sent', _('Sent for Signing')),
        ('signing', _('Signing in Progress')),
        ('signed', _('All Signed')),
        ('published', _('Published')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    ], default='draft', required=True)
    upload_response = fields.Text(string=_('Upload Response'))
    sign_response = fields.Text(string=_('Sign Response'))
    detail_response = fields.Text(string=_('Detail Response'))
    signed_file_path = fields.Char(string=_('Signed File Path'))
    signed_file_data = fields.Binary(string=_('Signed File'))
    notes = fields.Text()
    error_message = fields.Text(string=_('Error'))

    def action_upload_and_send(self):
        for rec in self:
            if not rec.contract_id:
                raise ValueError(_('No contract linked'))
            rec._upload_document()
            if rec.status == 'uploaded':
                rec._send_and_sign()

    def _upload_document(self):
        self.ensure_one()
        contract = self.contract_id
        config = self.voffice_config_id

        payload = {
            'docDetail': {
                'typeId': config.default_type_id or 0,
                'sTypeId': 0,
                'priorityId': 0,
                'officePublishedId': 0,
                'areaId': config.default_area_id or 0,
                'code': contract.name or '',
                'title': f"Contract {contract.name}",
                'description': contract.notes or f"Contract for {contract.partner_id.name or ''}",
                'autoPromulgateText': '',
                'isActive': True,
                'placeOfReceipt': config.default_place or 'Vientiane',
            },
            'signers': [],
            'mainFiles': [],
            'additionalFiles': [],
        }

        if contract.signed_file:
            import base64
            file_content = base64.b64decode(contract.signed_file)
            upload_result = config.upload_file(file_content, f"{contract.name}.pdf")
            if upload_result:
                payload['mainFiles'] = [{
                    'name': f"{contract.name}.pdf",
                    'fileLocation': upload_result.get('fileLocation', ''),
                }]
                self.upload_response = json.dumps(upload_result)

        try:
            result = config.upload_document_to_sign(payload)
            self.write({
                'doc_id': result.get('docId', ''),
                'trans_code': result.get('transCode', ''),
                'status': 'uploaded',
                'upload_response': json.dumps(result),
            })
            contract.sudo().write({'voffice_doc_id': result.get('docId', '')})
            _logger.info("VOffice document uploaded: %s", result.get('docId'))
        except Exception as e:
            self.write({
                'status': 'draft',
                'error_message': str(e),
            })
            _logger.exception("VOffice upload failed")
            raise

    def _send_and_sign(self):
        self.ensure_one()
        config = self.voffice_config_id
        try:
            result = config.send_and_sign(self.doc_id, self.trans_code)
            self.write({
                'status': 'sent',
                'sign_response': json.dumps(result),
            })
            self.contract_id.sudo().message_post(
                body=_('Document sent to VOffice for signing. Doc ID: %s') % self.doc_id,
            )
            _logger.info("VOffice send_and_sign: %s", self.doc_id)
        except Exception as e:
            self.write({
                'error_message': str(e),
            })
            _logger.exception("VOffice send_and_sign failed")
            raise

    def action_check_status(self):
        for rec in self:
            if not rec.doc_id:
                continue
            rec._check_status()

    def _check_status(self):
        self.ensure_one()
        config = self.voffice_config_id
        try:
            detail = config.get_document_detail(self.doc_id)
            self.detail_response = json.dumps(detail)
            state = detail.get('state')

            state_map = {
                1: 'signing',
                2: 'rejected',
                3: 'signing',
                4: 'published',
                5: 'signing',
                6: 'cancelled',
            }
            new_status = state_map.get(state, self.status)
            self.status = new_status

            if state == 4:
                self._handle_published(detail)
            elif state in (2, 6):
                self._handle_rejected(detail)

        except Exception as e:
            self.error_message = str(e)
            _logger.exception("VOffice check_status failed")

    def _handle_published(self, detail):
        self.ensure_one()
        contract = self.contract_id
        contract.sudo().action_sign()

        main_files = detail.get('fileMainSign', [])
        if main_files:
            self.signed_file_path = main_files[0].get('filePath', '')
            try:
                config = self.voffice_config_id
                file_data = config.get_signed_file(
                    self.doc_id,
                    main_files[0].get('filePath', ''),
                    main_files[0].get('storage', ''),
                )
                import base64
                self.signed_file_data = base64.b64encode(file_data)
                contract.signed_file = base64.b64encode(file_data)
            except Exception:
                _logger.exception("Failed to download signed file")

        contract.sudo().message_post(
            body=_('Contract signed and published via VOffice.'),
        )

    def _handle_rejected(self, detail):
        self.ensure_one()
        reason = ''
        list_stamper = detail.get('listStamper', [])
        for stamper in list_stamper:
            if stamper.get('rejectReason'):
                reason = stamper['rejectReason']
                break
        if not reason:
            reason = self.notes or ''

        self.write({'error_message': reason})
        self.contract_id.sudo().message_post(
            body=_('VOffice signing was rejected. Reason: %s') % reason,
        )
