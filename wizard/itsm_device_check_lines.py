from odoo import models,fields,api

class ItsmDeviceCheckLines(models.Model):
    _name = 'itsm.device.check.lines'
    _description = 'itsm device check info'

    device = fields.Many2one('itsm.device.manage',string='巡检设备')
    device_check = fields.Many2one('itsm.device.check',string='巡检单')
    device_state = fields.Selection([('readycheck','待巡检'),
                                     ('nomal','正常使用'),
                                     ('repaire','维修'),
                                     ('broken','报废')],string='设备状况',default='readycheck')

    def on_barcode_scanned(self, barcode):
        device = self.env['itsm.device.manage'].search([('barcode', '=', barcode)])
        if device:
            self._add_device(device)

    def _add_device(self,device):
        for record in self:
            device_id = []
            for item in device:
                device_id.append(item.id)
            data = {
                "device" : device_id
            }
            record.write(data)


# class ScanDevice(models.TransientModel):
#     _name = 'itsm.device.scan'
#     _description = '扫码向导'
#
#     barcode_scan = fields.Char(string='条码扫描')
#
#     def onchange_barcode_scan(self):
#         for recode in self:
#             check_id = self.env.context.get('check_id')
#             if recode.barcode_scan:
#                 devices = self.env['itsm.device.manage'].search([('number', '=', recode.barcode_scan)])
#                 if devices:
#                     vals = {
#                         'device_check': check_id,
#                         'device':devices.id
#                     }
#                     result = self.env['itsm.device.check.lines'].create(vals)
#                     return result
#                     # ids = [devices.id,]
#                     # vals = {
#                     #     'device_info':devices.id
#                     # }
#             #     result = super().create(vals)
#             #     return result
