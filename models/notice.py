# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NoticeSubject(models.Model):
    _name = "itsm.notice.subject"

    name = fields.Char(index=True, required=True, string="栏目名称")


class Notice(models.Model):
    _name = "itsm.notice"

    name = fields.Char(index=True, required=True, string="标题")
    publish = fields.Boolean(string="是否发布")
    subject_id = fields.Many2one(comodel_name="itsm.notice.subject", string="栏目")
    content = fields.Html(string="正文")
    attachment = fields.Binary(string="附件")
