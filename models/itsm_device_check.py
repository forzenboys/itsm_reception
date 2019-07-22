from odoo import models,fields,api
import requests, json, time
from odoo.exceptions import UserError

class ItsmDeviceCheck(models.Model):
    _name = 'itsm.device.check'
    _inherit = 'barcodes.barcode_events_mixin'
    _description = '资产盘点'

    name = fields.Char('盘点单名称',required=True)
    executor = fields.Many2one('res.users','执行人',required=True)
    creater = fields.Many2one('res.users','创建人')
    start_day = fields.Date('开始时间',required=True)
    end_day = fields.Date('结束时间',required=True)
    device_owner = fields.Many2one('itsm.department','资产所属')
    depart_use = fields.Many2one('itsm.department','使用部门')
    category = fields.Many2one('itsm.device.category','分类')
    location = fields.Many2one('itsm.position','位置')
    state = fields.Selection([('todo','未完成'),
                              ('done','已完成')],
                             '完成状态',default='todo')
    device = fields.Many2many('itsm.device.manage', string='巡检设备')
    device_info = fields.One2many('itsm.device.check.lines','device_check',string='巡检状况')
    scan_count = fields.Integer(compute='_compute_device')

    def _compute_device(self):
        for record in self:
            record.scan_count = self.env['itsm.device.check.lines'].search_count([('device_check','=',record.id)])

    def on_barcode_scanned(self,barcode):
        for recode in self:
            device_ids = recode.device.ids
            if barcode:
                devices = self.env['itsm.device.manage'].search([('number', '=',barcode)])
                if not devices:
                    raise UserError('无法识别设备，请检查设备条码的正确性')
                if self.env['itsm.device.check.lines'].search([('device','=',devices.id),('device_check','=',recode.id)]):
                    raise UserError('设备已录入，请勿重复扫描')

                vals = {
                    'device_check': recode.id,
                    'device':devices.id
                }
                result = self.env['itsm.device.check.lines'].create(vals)
                return result
                    # ids = [devices.id,]
                    # vals = {
                    #     'device_info':devices.id
                    # }
            #     result = super().create(vals)
            #     return result

# 巡检单过滤规则：通过配置项分类，部门等条件生成domain
    @api.model
    def domain_rule(self,vals):
        domain = []
        if vals['category']:
            domain.append(('category', '=', vals['category']))
        if vals['depart_use']:
            domain.append(('depart_id', '=', vals['depart_use']))
        if vals['device_owner']:
            domain.append(('config_owner', '=', vals['device_owner']))
        if vals['location']:
            domain.append(('location', '=', vals['location']))
        return domain

    @api.model
    def create(self,vals):
        domain = self.domain_rule(vals)
        record = self.env['itsm.device.manage'].search(domain)
        id_list = record.ids
        vals['device'] = [(6,0,id_list)]
        # a= super(ItsmDeviceCheck,self).create(vals)
        result = super().create(vals)
        return result

    @api.constrains('category', 'depart_use','device_owner','location')
    def change_device(self):
        for record in self:
            data = {
                "category": record.category.id,
                "depart_use": record.depart_use.id,
                "device_owner":record.device_owner.id,
                "location":record.location.id
            }
            domain = self.domain_rule(data)
            record = self.env['itsm.device.manage'].search(domain)
            id_list = record.ids
            vals={
                'device': [(6, 0, id_list)]
            }
            super().write(vals)






