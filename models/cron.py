# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class Cron(models.Model):
    _name = "itsm.cron"

    name = fields.Char(required=True, string="计划名称")
    cron_id = fields.Many2one(comodel_name="ir.cron", string="关联任务")
    # use = fields.Boolean(string="是否启用")
    interval = fields.Selection(
        selection=[("days", "每天"), ("weeks", "每周"), ("months", "每月"), ("years", "每年"), ("once", "一次性"),
                   ("others", "自定义")], string="执行间隔")
    days = fields.Integer(string="天")
    hours = fields.Integer(string="小时")
    worker = fields.Many2one(comodel_name="res.users", string="处理人")
    device_ids = fields.Many2many(comodel_name="itsm.device.manage", string="巡检对象")
    start_at = fields.Datetime(string="起始时间")
    remark = fields.Text(string="任务内容及要求")

    @api.model
    def create(self, vals):
        """
        重写create方法，使得创建表单时创建定时任务
        """
        cron_vals = self.get_cron_vals(vals)

        itsm_cron = super(Cron, self).create(vals)
        cron_vals["code"] = "model.send_mission(%S)" % itsm_cron.id
        cron = self.env["ir.cron"].create(cron_vals)
        itsm_cron.write({
            "cron_id": cron.id
        })

    @api.multi
    def write(self, vals):
        raise UserError("暂不支持修改定时任务")

    @api.multi
    def unlink(self):
        for this in self:
            print(this.cron_id.id)
            this.cron_id.unlink()
        return super(Cron, self).unlink()

    def send_mission(self, id):
        """
        派发巡检任务
        :param id: 定时任务ID
        """
        mission_detail = self.browse(id)
        self.env["itsm.work_order"].create({
            "name": "定时巡检任务",
            "title": mission_detail.name,
            "receiver": mission_detail.worker.id,
            "fault_equipment": [(6, 0, mission_detail.device_ids.ids)],
            "describe": mission_detail.remark
        })

    def get_cron_vals(self, vals):
        model_id = self.env.ref("itsm.model_itsm_cron").id

        cron_vals = {
            "name": vals.get("name"),
            "nextcall": vals.get("start_at"),
            "doall": True,
            "model_id": model_id,
            "state": "code"
        }

        if vals.get("interval") != "once" and vals.get("interval") != "others":
            interval_type = vals.get("interval")
            cron_vals["interval_type"] = interval_type
            cron_vals["interval_numbe"] = 1
            cron_vals["numbercall"] = -1

        elif vals["interval"] == "once":
            cron_vals["interval_type"] = "days"
            cron_vals["interval_numbe"] = 1
            cron_vals["numbercall"] = 0

        elif vals["interval"] == "others":
            hours = vals.get("days") * 24 + vals.get("hours")
            cron_vals["interval_type"] = "hours"
            cron_vals["interval_numbe"] = hours
            cron_vals["numbercall"] = 0

        return cron_vals
