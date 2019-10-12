from odoo import models,fields,api

class ItsmDeviceProvider(models.Model):
    _name = 'itsm.device.provider'
    _description = '供应商管理'

    name = fields.Char('公司名称')
    image = fields.Binary('公司头像')
    is_provider = fields.Boolean('供应商',default=True)
    is_sever = fields.Boolean('服务商')
    nickname = fields.Char('公司简称')
    fax = fields.Char('传真')
    tel = fields.Char('总机')
    email = fields.Char('邮箱')
    address = fields.Char('公司地址')
    web = fields.Char('网址')
    info = fields.Char('公司简介')