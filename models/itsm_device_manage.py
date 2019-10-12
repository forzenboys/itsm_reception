import odoo
from odoo import models,fields,api
import qrcode
import base64
import os
from pystrich.code128 import Code128Encoder
import time
import random

class ItsmDeviceManage(models.Model):
    _name = 'itsm.device.manage'
    _description = '资产管理'

    name = fields.Char('配置项名称',required=True)
    number = fields.Char('配置项编号')
    category = fields.Many2one(comodel_name="itsm.device.category", ondelete="cascade", string="配置项分类")
    category_name = fields.Char(related="category.name", string="分类名")
    state = fields.Selection([('broken','报废'),
                              ('put','入库'),
                              ('repair','维修'),
                              ('use','使用')],
                             '状态',default='put')
    robot_name = fields.Char('机器名')
    ip = fields.Char('ip地址',required=True)
    use = fields.Char('用途')
    depart_id = fields.Many2one('itsm.department','所属单位')
    manager_id = fields.Many2one('res.users','管理员')
    provider_id = fields.Many2one('itsm.device.provider','供应商')
    area = fields.Many2one('itsm.area','区域')
    location = fields.Many2one('itsm.position','位置/宿舍')
    info = fields.Char('备注')
    img = fields.Binary('设备外形图')
    qr_img = fields.Binary('设备二维码')
    number_property = fields.Integer('资产编号')
    number_contract = fields.Integer('合同编号')
    brand_type = fields.Char('品牌型号')
    serve_sale = fields.Char('售后服务商')
    save_site = fields.Char('存放地点')
    comming_day = fields.Date('投运日期')
    user = fields.Char('使用人')
    user_depart = fields.Many2one('itsm.department','使用部门')
    repair_start = fields.Date('维保开始时间')
    repair_end = fields.Date('维保结束时间')
    repair_contract = fields.Char('维保合同')
    fujian = fields.Many2many('ir.attachment',string=u'附件')

    config_brand = fields.Char('品牌')
    config_type = fields.Char('型号')
    config_number = fields.Char('产品号/序列号')
    config_owner = fields.Many2one('itsm.department','资产归属')
    config_contract = fields.Char('采购合同编号')
    config_repaire = fields.Many2one('res.users','维护人')
    config_depart = fields.Many2one('itsm.department','使用单位')
    config_user = fields.Many2one('res.users','使用者')
    config_time_buy = fields.Date('采购时间')
    config_broken = fields.Date('报废时间')
    cpu_brand = fields.Char('CPU品牌')
    cpu_type = fields.Char('CPU型号')
    cpu_hz = fields.Char('CPU主频')
    cpu_number = fields.Integer('CPU个数')
    memory_size = fields.Char('内存大小')
    disk_size = fields.Char('硬盘大小')
    area_type = fields.Char('分区类型')
    ip_address = fields.Char('IP地址')
    mac = fields.Char('MAC地址')
    belongs = fields.Char('所属域')
    room = fields.Char('机房')
    chest = fields.Char('机柜')
    port_number = fields.Integer('端口数量')
    port_number_use = fields.Integer('剩余端口数量')
    vlan_belong = fields.Char('所属VLAN网段')
    memory = fields.Char('内存')
    trench_number = fields.Integer('槽位数量')
    ios = fields.Char('IOS版本')
    capacity = fields.Char('裸容量')
    capacity_count = fields.Char('总容量')
    capacity_used = fields.Char('已用容量')
    capacity_use = fields.Char('可用容量')
    backup = fields.Char('备份策略表')
    ip_group = fields.Char('隶属IP地址段')
    soft_path = fields.Char('最终软件库路径')
    soft_version = fields.Char('软件版本')
    server = fields.Char('服务名')

    @api.model
    def create(self, vals):
        # 创建配置项产品自动生成设备二维码
        # 定义二维码所包含的信息

        # data = {'name': vals['name'],
        #         'ip': vals['ip']}
        # 调用函数生成二维码图片，返回图片路径
        vals['number'] = self.create_number()
        # img_path = self.create_barcode(vals['number'])
        foo = Code128Encoder(vals['number']).get_imagedata()
        img_qr = base64.b64encode(foo)
        vals['qr_img'] = img_qr
        result = super().create(vals)
        return result

    # @api.multi
    # def write(self, vals):
    #     data = {}
    #     if "ip" in vals:
    #         data['ip'] = vals['ip']
    #     if "name" in vals:
    #         data['name'] = vals['name']
    #     if len(data)>0:
    #         img_path = self.create_qrcode(data)
    #         print(img_path)
    #         img_qr = base64.b64encode(open(img_path, 'rb').read())
    #         vals['qr_img'] = img_qr
    #     result = super().write(vals)
    #     return result

    # @api.constrains('name','ip')
    # def update_name(self):
    #     for device in self:
    #         data = {
    #             "name": device.name,
    #             "ip": device.ip,
    #             "url" : "localhost:8069/itsm_device/devicecheck/" + str(device.id)
    #         }
    #         # data = "http://localhost:8069/itsm_device/devicecheck/" + str(device.id)
    #         img_path = self.create_qrcode(data)
    #         img_qr = base64.b64encode(open(img_path, 'rb').read())
    #         vals = {
    #             'qr_img' : img_qr
    #         }
    #         super().write(vals)
    def count_number(self):
        return self.env['itsm.device.manage'].search_count([])

    def create_number(self):
        timestr = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        count = str(self.count_number())
        return timestr+count

    def create_barcode(self,id):
        foo = Code128Encoder(id)
        print(foo.get_imagedata())
        img_path = "E:\Odoo 12.0\server\my-modules\itsm_device\static\image"+ id +'.png'
        if os.path.exists(img_path):
            os.remove(img_path)
            foo.save(img_path)
        # 保存图片，返回图片路径
        else:
            foo.save(img_path)
        return img_path

    def create_qrcode(self,code):
        # 二维码相关设置
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # 生成二维码
        qr.add_data(code)
        qr.make(fit=True)
        image = qr.make_image()
        img_path = "E:\Odoo 12.0\server\my-modules\itsm_device\static\image"+ code['name'] +'.png'
        if os.path.exists(img_path):
            os.remove(img_path)
            image.save(img_path)
        # 保存图片，返回图片路径
        else:
            image.save(img_path)
        return img_path

class ItsmDeviceCategory(models.Model):
    _name = 'itsm.device.category'
    _description = '配置项分类'

    name = fields.Char('分类名称')
    parent_id = fields.Many2one(
        'itsm.device.category',
        '上级分类',
        ondelete='restrict')
    # Optional but good to have:
    child_ids = fields.One2many(
        'itsm.device.category',
        'parent_id',
        '下级分类')

    @api.model
    def getCategoryList(self):
       category = self.search([])
       result = []
       for record in category:
           result.append({
               "id": record.id,
               "parent_id": record.parent_id.id,
               "name": record.name
           })
       return result