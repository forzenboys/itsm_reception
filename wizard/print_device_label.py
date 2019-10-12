from odoo import models,fields,api
from odoo.exceptions import Warning,UserError

class DeviceLabel(models.TransientModel):
    _name = 'itsm.device.label'
    _description = 'device labels'

    selected = fields.Boolean('打印',compute='_compute_selected')
    device_id = fields.Many2one('itsm.device.manage','设备',required=True,ondelete='cascade')
    wizard_id = fields.Many2one('itsm.print.device.label','打印向导')
    qty_initial = fields.Integer('初始数量',default=1)
    qty = fields.Integer('标签数量',default=1)

    @api.depends('qty')
    def _compute_selected(self):
        for record in self:
            if record.qty > 0:
                record.update({'selected' : True})
            else:
                record.update({'selected' : False})

    @api.multi
    def action_plus_qty(self):
        for record in self:
            record.update({'qty' : record.qty+1})

    @api.multi
    def action_minus_qty(self):
        for record in self:
            if record.qty >0:
                record.update({'qty' : record.qty-1})
            else:
                raise UserError('打印的标签数量必需为正数')


class PrintDeviceLabel(models.TransientModel):
    _name = 'itsm.print.device.label'

    @api.model
    def _get_device(self):
        res = []
        if self._context.get('active_model') == 'itsm.device.manage':
            devices = self.env[self._context.get('active_model')].browse(self._context.get('default_devices_ids'))
            for device in devices:
                label = self.env['itsm.device.label'].create({
                    'device_id': device.id,
                })
                res.append(label.id)
        # elif self._context.get('active_model') == 'product.product':
        #     products = self.env[self._context.get('active_model')].browse(self._context.get('default_product_ids'))
        #     for product in products:
        #         label = self.env['product.label'].create({
        #             'product_id': product.id,
        #         })
        #         res.append(label.id)
        return res

    name = fields.Char('Name', default='Print Device Labels')
    label_ids = fields.One2many(
        comodel_name='itsm.device.label',
        inverse_name='wizard_id',
        string='Labels for Device',
        default=_get_device,
    )
    template = fields.Selection(
        selection=[('itsm_reception.report_device_label_A4_57x35', 'Label 57x35mm (A4: 21 pcs on sheet, 3x7)')],
        string='标签模板',
        default='itsm_reception.report_device_label_A4_57x35',
    )
    qty_per_device = fields.Integer(
        string='预打印数量',
        default=1,
    )

    @api.multi
    def action_print(self):
        """ Print labels
        """
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')

        if not labels:
            raise Warning('请选择要打印的设备和数量')
        return self.env.ref(self.template).with_context(discard_logo_check=True).report_action(labels)

    @api.multi
    def action_set_qty(self):
        self.ensure_one()
        self.label_ids.write({'qty': self.qty_per_device})

    @api.multi
    def action_restore_initial_qty(self):
        self.ensure_one()
        for label in self.label_ids:
            if label.qty_initial:
                label.update({'qty': label.qty_initial})
