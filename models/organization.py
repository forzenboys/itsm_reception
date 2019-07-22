# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Area(models.Model):
    _name = "itsm.area"

    name = fields.Char(index=True, required=True, string="区域名称")


class Department(models.Model):
    _name = "itsm.department"

    display_name = fields.Char(related="name_path")
    name = fields.Char(index=True, required=True, string="部门名称")
    parent_id = fields.Many2one(index=True, comodel_name="itsm.department", string="上级部门")
    name_path = fields.Char(index=True, compute="_compute_name_path", string="部门路径")
    member_ids = fields.One2many(comodel_name="res.users", inverse_name="department_id", readonly=True, string="部门成员")
    child_ids = fields.One2many(comodel_name="itsm.department", inverse_name="parent_id", string="下级部门")

    @api.one
    @api.depends("name", "parent_id", "parent_id.name")
    def _compute_name_path(self):
        """
        生成部门路径
        """
        if self.parent_id:
            self.name_path = "{} / {}".format(self.parent_id.name_path, self.name)
        else:
            self.name_path = self.name

    @api.model
    def get_department_tree_data(self, id):
        departments = self.search([])
        result = []
        for department in departments:
            result.append({
                "id": department.id,
                "parentId": department.parent_id.id,
                "name": department.name
            })
        return result


class ResUsers(models.Model):
    _inherit = "res.users"

    name = fields.Char(index=True, string="姓名")
    login = fields.Char(index=True, string="账号")
    email = fields.Char(index=True, string="邮箱")
    area_id = fields.Many2one(comodel_name="itsm.area", index=True, required=True, string="区域")
    level = fields.Selection(selection=[("LV3", "LV3"), ("LV2", "LV2"), ("LV1", "LV1"), ("VIP", "VIP")], default="LV3",
                             index=True, required=True, string="等级")
    department_id = fields.Many2one(comodel_name="itsm.department", index=True, required=True, string="部门")
    working_group_ids = fields.Many2many(comodel_name="itsm.working_group", relation="itsm_working_group_members",
                                         string="工作组")
    room_number = fields.Char(index=True, string="房号")
    position_id = fields.Many2one(comodel_name="itsm.position", index=True, string="位置")
    job = fields.Char(index=True, string="职务")
    test = fields.Datetime(string="评分")

    @api.multi
    def reset_password(self):
        """
        重置密码
        :return:
        """
        for this in self:
            this.write({
                "password": "123456"
            })

class Role(models.Model):
    _name = "itsm.role"

    name = fields.Char(index=True, required=True, string="角色名称")
    # TODO 角色继承
    # TODO 工作台视图
    member_ids = fields.Many2many(comodel_name="res.users", relation="itsm_role_members", string="成员")
    # TODO 权限组
    # TODO 面板


class Position(models.Model):
    _name = "itsm.position"

    name = fields.Char(index=True, required=True, string="位置名称")
    parent_id = fields.Many2one(index=True, comodel_name="itsm.department", string="上级位置")

class WorkingGroup(models.Model):
    _name = "itsm.working_group"

    name = fields.Char(index=True, required=True, string="工作组名称")
    member_ids = fields.Many2many(comodel_name="res.users", relation="itsm_working_group_members", string="工作组成员")
