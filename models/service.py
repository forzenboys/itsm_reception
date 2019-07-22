# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ServiceType(models.Model):
    _name = "itsm.service_type"

    name = fields.Char(index=True, required=True, string="分类名称")
    parent_id = fields.Many2one(comodel_name="itsm.service_type", index=True, string="上级分类")
    child_ids = fields.One2many(comodel_name="itsm.service_type", inverse_name="parent_id", string="下级分类")


class ServiceCatalogue(models.Model):
    _name = "itsm.service_catalogue"

    name = fields.Char(required=True, string="服务目录")
    introduction = fields.Text(string="服务简介")
    description = fields.Html(string="详细说明")
    type_id = fields.Selection([('业务申请', '业务申请'), ('故障报修', '故障报修')], default="业务申请", required=True, string="所属分类")
    level = fields.Selection(selection=[("低", "低"), ("中", "中"), ("高", "高"), ("紧急", "紧急")], string="优先级", default="中")
    response_time_limit = fields.Integer(required=True, string="响应时限（时）")
    slove_time_limit = fields.Integer(required=True, string="解决时限（时）")

    @api.model
    def create(self, vals):
        """
        创建业务申请、故障报修工单
        :param vals:
        :return:
        """
        odoo = super(ServiceCatalogue, self).create(vals)
        name = str(vals["name"])
        id = str(odoo.id)
        emergency = str(vals["level"])
        response_time_limit = str(vals["response_time_limit"])
        slove_time_limit = str(vals["slove_time_limit"])
        if str(vals["type_id"]) == "业务申请":
            self.env['itsm.reception_business_applications'].create_business_applications(name, id, emergency, response_time_limit, slove_time_limit)
        else:
            self.env['itsm.reception_trouble_repair'].create_trouble_repair(name, id, emergency, response_time_limit, slove_time_limit)
        return odoo

    @api.multi
    def write(self, values):
        """
        修改业务申请、故障报修工单
        """
        data = super(ServiceCatalogue, self).write(values)
        for record in self:
            if record.type_id == "业务申请":
                self.env['itsm.reception_business_applications'].update_business_applications(record.name, record.id, record.level, record.response_time_limit, record.slove_time_limit)
            else:
                self.env['itsm.reception_trouble_repair'].update_trouble_repair(record.name, record.id, record.level, record.response_time_limit, record.slove_time_limit)
            print(record.type_id)
        return data

    @api.multi
    def unlink(self):
        """
        删除业务申请、故障报修工单
        """
        data = super(ServiceCatalogue, self).unlink()
        for record in self:
            self.env['itsm.reception_business_applications']. unlink_business_applications(record.id)
            self.env['itsm.reception_trouble_repair'].unlink_trouble_repair(record.id)
            print("删除成功")
        return data

class SLA(models.Model):
    _name = "itsm.sla"

    name = fields.Char(index=True, required=True, string="SLA名称")
    description = fields.Text(string="描述")
    level = fields.Selection(selection=[("LOW", "低"), ("MIDDLE", "中"), ("HIGHT", "高")], string="优先级")
    service_id = fields.Many2one(comodel_name="itsm.service_catalogue", string="关联服务")
    response_time_limit = fields.Integer(string="响应时限（时）")
    slove_time_limit = fields.Integer(string="解决时限（时）")


class EvaluationTag(models.Model):
    _name = "itsm.evaluation_tag"

    name = fields.Char(index=True, required=True, string="标签名称")
