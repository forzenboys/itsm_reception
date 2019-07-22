# -*- coding: utf-8 -*-
from odoo import models, fields


class IrAttachiment(models.Model):
    _inherit = 'ir.attachment'

    source = fields.Char(string='来源')

class one_fujian(models.Model):
    """
    存储附件的model
    """
    _name = "fujian"

    name = fields.Binary("附件")
    filename = fields.Many2one("itsm.reception_trouble_repair", string="名称")
