from odoo import models,fields,api
import datetime

class ItsmWorkEvent(models.TransientModel):
    _name = 'itsm.workevent'
    _description = '事件对应工单'

    number = fields.Char('服务单编号')
    name = fields.Char('工单名称')
    time = fields.Datetime('报障时间')
    enginer = fields.Many2one('res.users',string='受理工程师')
    user = fields.Char(string='申请人')
    department = fields.Char(string='报障部门')
    emergency = fields.Selection([("低", "低"), ("中", "中"), ("高", "高"), ("紧急", "紧急")], string="优先级", default="低")
    tel = fields.Char('联系电话')
    eventtype = fields.Many2one('itsm.service_type',string='故障类别')
    description = fields.Html('故障描述')
    device_number = fields.Char('设备资产编号')

    # evaluate = fields.Char('评价')
    note = fields.Char('备注')

    def get_applications_data(self):
        """
        创建事件处理工单：
        model:itsm.event_processing
        """
        for record in self:
            approval_state ='draft'
            if record.enginer:
                working_condition = 'appoint'
            now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            coding = "IM" + now_time
            data = {
                # "title":record.name,
                "working_condition": "处理中",
                "approval_state": approval_state,
                "server_id":record.number,
                "priority": record.emergency,
                "task_coding": coding,
                "title": record.name,
                "user": record.user,
                "applicant_department": record.department,
                "receiver":record.enginer.id,
                "phone": record.tel,
                "create_time": create_time,
                "describe": record.description,
                "service_type": record.eventtype.id,
                "device_number":record.device_number,
                "response_time_limit": "4",
                "slove_time_limit": "4"
            }
            self.env["itsm.event_processing"].search([]).create(data)

