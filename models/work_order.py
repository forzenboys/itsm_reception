import datetime,time
from odoo import models, fields, api
from odoo.exceptions import UserError
class Itsm_Work_Order(models.Model):
    """
    业务申请工单
    """
    _name = "itsm.work_order"

    name = fields.Char(string="业务类型")
    working_condition = fields.Char(string="工作状态")
    task_coding = fields.Char(string="任务编号")
    server_id = fields.Char('服务单号')
    title = fields.Char(string="标题")
    applicant_name = fields.Many2one("res.users", string="申请人", store=True, required=True)
    receiver = fields.Many2one("res.users", string="接单人", store=True)
    phone = fields.Char(string="联系电话")
    create_time = fields.Datetime(string="创建时间")
    priority = fields.Char(string="优先级")
    applicant_department = fields.Many2one('itsm.department',string="申请部门")
    describe = fields.Text(string="描述")
    response_time_limit = fields.Char(string="响应时限（时）")
    slove_time_limit = fields.Char(string="解决时限（时）")
    acceptance_time = fields.Datetime(string="接单时间")
    response_completion = fields.Char(string="响应(完成)", default="待接单")
    solve = fields.Char(string="解决", default="待解决")

    approval_state = fields.Selection([
        ('draft', '待审批'),
        ('receipt', '接单'),
        ('appoint', '指定接单人'),
        ('frontline', '转一线执行'),
        ('transfer', '转派'),
        ('done', '已完成'),
        ('cancel', '不通过'),
        ('evaluate', '评价')
    ], default='draft', string='操作')
    """
    工单记录所需字段
    """
    first_record = fields.Char(string="记录1", default="null")
    feedback1 = fields.Char(string="评语", default="null")
    two_record = fields.Char(string="记录2", default="null")
    feedback2 = fields.Char(string="评语", default="null")
    three_record = fields.Char(string="记录3", default="null")
    feedback3 = fields.Char(string="评语", default="null")
    four_record = fields.Char(string="记录4", default="null")
    feedback4 = fields.Char(string="评语", default="null")

    def update_time(self, id):
        """
        定时任务进去的方法
        :param id:
        :return:
        """
        print("进入方法")
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M") #获取当前时间
        odoo = self.env["itsm.work_order"].search([("id", "=", id)])
        response_time = odoo.create_time + datetime.timedelta(hours=int(odoo.response_time_limit)) #获取创建工单的时间加上响应时限
        check_time = response_time.strftime("%Y%m%d%H%M")
        disparity_response_time = int(check_time) - int(now_time)
        if disparity_response_time < 0 and odoo.acceptance_time == False: #如果响应时间超过了当前时间，则修改字段为已超时
            odoo.write({"response_completion": "已超时", "working_condition": "已超时"})
        if disparity_response_time == 100 and odoo.acceptance_time == False: #响应时间只剩一小时
            odoo.write({"response_completion": "接单工单时间仅剩1小时"})
        """
        判断完成与否
        """
        if odoo.acceptance_time != False: #判断是否已接单
            acceptance_time_data = odoo.acceptance_time + datetime.timedelta(hours=int(odoo.slove_time_limit))
            acceptance_time = acceptance_time_data.strftime("%Y%m%d%H%M")
            solve_time = int(acceptance_time) - int(now_time)
            if solve_time < 0 and odoo.solve !="解决":
                odoo.write({"solve": "已超时", "working_condition": "已超时"})
            if disparity_response_time == 100 and odoo.solve !="解决":  # 解决时间只剩一小时
                odoo.write({"solve": "完成工单时间仅剩1小时"})

    def time_update_time(self, id):
        """
        每隔一分钟，获取一次当前时间
        :return:
        """
        cron_name = "szpdc" + str(id)
        name = self.env['ir.cron'].search([("name", "=", cron_name)])
        if not name:
            model_id = self.env.ref("itsm_reception.model_itsm_work_order").id
            self.env['ir.cron'].sudo().create({
                'name': cron_name,  # 定时任务名
                'interval_type': 'minutes',  # 定时间隔的单位
                'interval_number': 1,  # 定时间隔
                'numbercall': -1,  # 循环次数（-1代表无限循环）
                'doall': False,  # 服务器重启错过时机，是否补回执行
                'model_id': model_id,  # 任务绑定的Model
                'state': 'code',
                'code': "model.update_time(" + str(id) + ")"
            })
        else:
            raise UserError('已定时')
        print("定时开始")

    @api.model
    def create(self, vals):
        """
        重写create方法，在create方法触发后，执行定时任务
        :return:
        """
        odoo = super(Itsm_Work_Order, self).create(vals)
        self.time_update_time(odoo.id) #将id传到定时任务中
        return odoo

    @api.multi
    def action_receipt(self):
        """审批状态跳转到接单"""
        self.write({'approval_state': 'receipt'})
        self.write({'working_condition': '待完成'})
        """
        创建工单记录
        """
        first_record = self.env.user.name + "-接单了"
        record_data = {
            "first_record": str(first_record),
            "receiver": self.env.user.id,
            "feedback1": "备注:"
        }
        self.write(record_data)
        """将当前时间写进接单时间中"""
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.write({"acceptance_time": now_time})

    @api.multi
    def action_appoint(self):
        """指定接单人按钮"""
        select_user = self.env["itsm.select_user"].search([("itsm_id", "=", self.id)])  # 查找id相同的表单
        if not select_user:  # 如果没有则创建
            self.env["itsm.select_user"].search([]).create({"itsm_id": self.id})
        data_id = self.env["itsm.select_user"].search([("itsm_id", '=', self.id)]).id
        action = {
            "type": "ir.actions.act_window",
            "name": "视图",
            "res_model": "itsm.select_user",
            "view_mode": "form",
            "res_id": data_id,
            "target": "new"
        }
        return action

    @api.multi
    def action_frontline(self):
        """审批状态跳转到二线执行人"""
        self.write({'approval_state': 'frontline'})
        """
        添加记录
        """
        first_record = self.env.user.name + "-提升工单等级"
        record_data = {
            "two_record": str(first_record),
            "feedback2": "备注:"
        }
        self.write(record_data)
    @api.multi
    def action_transfer(self):
        """审批状态降级"""
        self.write({'approval_state': 'transfer'})
        self.write({'working_condition': '降低工单'})
        """
        添加记录
        """
        first_record = self.env.user.name + "-降低工单等级"
        record_data = {
            "three_record": str(first_record),
            "feedback3": "备注:"
        }
        self.write(record_data)

    @api.multi
    def action_done(self):
        """审批状态完成"""
        self.write({'working_condition': '完成工单'})
        data = {
            "itsm_id": self.id,
            "name": self.name,
            "working_condition": self.task_coding,
            "title": self.title,
        }
        self.env["itsm.satisfaction_return"].search([]).create(data)
        self.write({'approval_state': 'done'})
        """
        添加记录
        """
        first_record = self.env.user.name + "-完成单子"
        record_data = {
            "four_record": str(first_record),
            "feedback4": "备注:"
        }
        self.write(record_data)
        """
        获取定时任务id,完成表单后删除定时任务
        """
        cron_name = "szpdc" + str(self.id)
        crons = self.env['ir.cron'].search([("name", "=", cron_name)])
        crons.unlink()

    @api.multi
    def action_cancel(self):
        """审批状态不通过"""
        self.write({'working_condition': '工单未完成'})
        self.write({'approval_state': 'cancel'})
        """
        添加记录
        """
        first_record = self.env.user.name + "-取消单子"
        record_data = {
            "four_record": str(first_record),
            "feedback4": "备注:"
        }
        self.write(record_data)

    @api.multi
    def action_evaluate(self):
        """审批状态结束，评价"""
        data_id = self.env["itsm.satisfaction_return"].search([("itsm_id", '=', self.id)]).id
        print(data_id)
        action = {
            "type": "ir.actions.act_window",
            "name": "视图",
            "res_model": "itsm.satisfaction_return",
            "view_mode": "form",
            "ref": "itsm_scoring_table_form",
            "res_id": data_id,
            "target": "new"
        }
        return action

    def set_username(self):
        """
        升降级后接单
        :return:
        """
        self.write({"receiver": self.env.user.id, 'approval_state': 'receipt', 'working_condition': '待完成'})  # 修改接单人为当前用户

class Itsm_Event_Processing(models.Model):
    """
    事件处理工单
    """
    _name = "itsm.event_processing"
    _description = "事件处理工单"
    _order = "create_time desc"

    # _inherit = ['mail.thread']

    name = fields.Char(string="业务类型")
    working_condition = fields.Char(string="工作状态")
    task_coding = fields.Char(string="任务编号")
    server_id = fields.Char('服务单号')
    title = fields.Char(string="标题")
    user = fields.Char(string='申请人')
    # applicant_name = fields.Many2one("res.users", string="申请人", store=True)
    applicant_department = fields.Char(string="报障部门")
    receiver = fields.Many2one("res.users", string="接单人", store=True)
    phone = fields.Char(string="联系电话")
    create_time = fields.Datetime(string="创建时间")
    priority = fields.Char(string="优先级")
    service_type = fields.Many2one('itsm.service_type', string='故障类别')
    enclosure = fields.Binary(string="附件", store=True)
    describe = fields.Html(string="故障描述")
    analyze = fields.Char('故障分析')
    fault_equipment = fields.Many2many("itsm.device.manage", string="故障设备")
    device_number = fields.Char('设备资产编号')
    material_seletion = fields.One2many("itsm.material_seletion", "name", string="物料选择")
    response_time_limit = fields.Char(string="响应时限（时）")
    slove_time_limit = fields.Char(string="解决时限（时）")
    acceptance_time = fields.Datetime(string="接单时间")
    response_completion = fields.Char(string="响应(完成)", default="待接单")


    solve = fields.Char(string="解决", default="待解决")
    approval_state = fields.Selection([
        ('draft', '待审批'),
        ('receipt', '接单'),
        ('appoint', '指定接单人'),
        ('frontline', '转一线执行'),
        ('transfer', '转派'),
        ('done', '已完成'),
        ('cancel', '不通过'),
        ('evaluate', '评价')
    ], default='draft', string='操作')
    """
    工单记录所需字段
    """
    first_record = fields.Char(string="记录1", default="null")
    feedback1 = fields.Char(string="评语", default="null")
    two_record = fields.Char(string="记录2", default="null")
    feedback2 = fields.Char(string="评语", default="null")
    three_record = fields.Char(string="记录3", default="null")
    feedback3 = fields.Char(string="评语", default="null")
    four_record = fields.Char(string="记录4", default="null")
    feedback4 = fields.Char(string="评语", default="null")

    # cost_progress = fields.Integer(string="进度", compute="_compute_progress")
    # @api.depends('create_time','slove_time_limit')
    # def _compute_progress(self):
    #     for record in self:
    #         print(record.slove_time_limit)
    #         now_time = datetime.datetime.now()
    #         cost_time = (now_time-record.create_time).seconds
    #         solve_time = int(record.slove_time_limit)*3600
    #         print(round(cost_time/solve_time,2))


    def update_time(self, id):
        """
        定时任务进去的方法
        :param id:
        :return:
        """
        print("进入方法")
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M") #获取当前时间
        odoo = self.env["itsm.event_processing"].search([("id", "=", id)])
        response_time = odoo.create_time + datetime.timedelta(hours=int(odoo.response_time_limit)) #获取创建工单的时间加上响应时限
        check_time = response_time.strftime("%Y%m%d%H%M")
        disparity_response_time = int(check_time) - int(now_time)
        if disparity_response_time < 0 and odoo.acceptance_time == False: #如果响应时间超过了当前时间，则修改字段为已超时
            odoo.write({"response_completion": "已超时", "working_condition": "已超时"})
            print("已超时")
        if disparity_response_time == 100 and odoo.acceptance_time == False: #响应时间只剩一小时
            odoo.write({"response_completion": "接单工单时间仅剩1小时"})
            print("时间不多")
        """
        判断完成与否
        """
        print(disparity_response_time)
        if odoo.acceptance_time != False: #判断是否已接单
            print("已接单")
            acceptance_time_data = odoo.acceptance_time + datetime.timedelta(hours=int(odoo.slove_time_limit))
            acceptance_time = acceptance_time_data.strftime("%Y%m%d%H%M")
            solve_time = int(acceptance_time) - int(now_time)
            if solve_time > 0 and odoo.solve !="解决":
                odoo.write({"solve": "已超时", "working_condition": "已超时"})
            if disparity_response_time == 100 and odoo.solve !="解决":  # 解决时间只剩一小时
                odoo.write({"solve": "完成工单时间仅剩1小时"})
            print(solve_time)

    def time_update_time(self, id):
        """
        每隔一分钟，获取一次当前时间
        :return:
        """
        print(id)
        cron_name = "szpdc.event_processing" + str(id)
        name = self.env['ir.cron'].search([("name", "=", cron_name)])
        if not name:
            model_id = self.env.ref("itsm_reception.model_itsm_event_processing").id
            self.env['ir.cron'].sudo().create({
                'name': cron_name,  # 定时任务名
                'interval_type': 'minutes',  # 定时间隔的单位
                'interval_number': 1,  # 定时间隔
                'numbercall': -1,  # 循环次数（-1代表无限循环）
                'doall': False,  # 服务器重启错过时机，是否补回执行
                'model_id': model_id,  # 任务绑定的Model
                'state': 'code',
                'code': "model.update_time(" + str(id) + ")"
            })
        else:
            raise UserError('已定时')
        print("定时开始")

    @api.model
    def create(self, vals):
        """
        重写create方法，在create方法触发后，执行定时任务
        :return:
        """
        odoo = super(Itsm_Event_Processing, self).create(vals)
        self.time_update_time(odoo.id) #将id传到定时任务中
        return odoo

    @api.multi
    def action_receipt(self):
        """审批状态跳转到接单"""
        self.write({'working_condition': '待完成'})
        self.write({'approval_state': 'receipt'}) #修改审批状态
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #获取当前时间
        material_approval = self.env["itsm.material_approval"].search([]) #获取物料审批表单值
        for record in self.material_seletion:
            material_data = {
                "job_number": self.task_coding, #工单号
                "application_time": now_time, #申请时间
                "applicant": self.applicant_name.name, #申请人姓名
                "name": record.material_name.name, #物料名称
                "quantity_of_applications": record.number, #申请数量
                "material_coding": record.code, #物料编码
                "residual_quantity": record.max_number #最大数量，通过查找一样物料编码的物料数量相加而成
            }
            print(record.material_name.name, record.max_number)
            material_approval.create(material_data)  # 当审批状态为接单时，将物料申请信息返回到物料申请表单中
        """
        创建工单记录
        """
        first_record = self.env.user.name + "-接单了"
        record_data = {
            "first_record": str(first_record),
            "receiver": self.env.user.id,
            "feedback1": "备注:"
        }
        self.write(record_data)
        """将当前时间写进接单时间中"""
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.write({"acceptance_time": now_time})

    @api.multi
    def action_appoint(self):
        """指定接单人按钮"""
        """
        指定接单人，在接单时绑定接单人表单id
        """
        select_user = self.env["itsm.select_user"].search([("itsm_id", "=", self.id)])  # 查找id相同的表单
        if not select_user:  # 如果没有则创建
            self.env["itsm.select_user"].search([]).create({"itsm_id": self.id})
        data_id = self.env["itsm.select_user"].search([("itsm_id", '=', self.id)]).id
        action = {
            "type": "ir.actions.act_window",
            "name": "视图",
            "res_model": "itsm.select_user",
            "view_mode": "form",
            "res_id": data_id,
            "target": "new"
        }
        return action

    @api.multi
    def action_frontline(self):
        """审批状态跳转到二线执行人"""
        self.write({'approval_state': 'frontline'})
        """
        添加记录
        """
        first_record = self.env.user.name + "-提升工单等级"
        record_data = {
            "two_record": str(first_record),
            "feedback2": "备注:"
        }
        self.write(record_data)

    @api.multi
    def action_transfer(self):
        """工单等级下降"""
        self.write({'approval_state': 'transfer'})
        """
        添加记录
        """
        first_record = self.env.user.name + "-降低工单等级"
        record_data = {
            "three_record": str(first_record),
            "feedback3": "备注:"
        }
        self.write(record_data)

    @api.multi
    def action_done(self):
        """审批状态完成"""
        self.write({'working_condition': '已完成'})
        data = {
            "itsm_id": self.id,
            "name": self.name,
            "working_condition": self.task_coding,
            "title": self.title,
        }
        self.env["itsm.satisfaction_return"].search([]).create(data)
        self.write({'approval_state': 'done'})
        """
        添加记录
        """
        first_record = self.env.user.name + "-完成单子"
        record_data = {
            "four_record": str(first_record),
            "feedback4": "备注:"
        }
        self.write(record_data)
        """
        获取定时任务id,完成表单后删除定时任务
        """
        cron_name = "szpdc.event_processing" + str(self.id)
        crons = self.env['ir.cron'].search([("name", "=", cron_name)])
        crons.unlink()
    @api.multi
    def action_cancel(self):
        """审批状态不通过"""
        self.write({'working_condition': '未完成'})
        self.write({'approval_state': 'cancel'})
        """
        添加记录
        """
        first_record = self.env.user.name + "-取消单子"
        record_data = {
            "four_record": str(first_record),
            "feedback4": "备注:"
        }
        self.write(record_data)

    @api.multi
    def action_evaluate(self):
        """审批状态结束，评价"""
        data_id = self.env["itsm.satisfaction_return"].search([("itsm_id", '=', self.id)]).id
        action = {
            "type": "ir.actions.act_window",
            "name": "视图",
            "res_model": "itsm.satisfaction_return",
            "view_mode": "form",
            "ref": "itsm_scoring_table_form",
            "res_id": data_id, #跳转至指定id的表单中
            "target": "new"
        }
        return action

    @api.multi
    def action_material_seletion(self):
        """跳转至物料选择窗口"""
        data_id = self.env["itsm.material_seletion"].search([("name", '=', self.id)]).id
        action = {
            "type": "ir.actions.act_window",
            "name": "视图",
            "res_model": "itsm.material_seletion",
            "view_mode": "form",
            "ref": "itsm_material_seletion_form",
            "res_id": data_id,  # 跳转至指定id的表单中
            "target": "new"
        }
        return action

    def set_username(self):
        """
        升降级后接单
        :return:
        """
        self.write({"receiver": self.env.user.id, 'approval_state': 'receipt','working_condition': '待完成'}) #修改接单人为当前用户

class Material_Seletion(models.Model):
    """故障工单中的物料选择"""
    _name = "itsm.material_seletion"

    name = fields.Many2one("itsm.event_processing", string="物料选择表id")
    material_name = fields.Many2one("itsm.material_management", string="物料选择")
    max_number = fields.Char(string="可选数量", compute="material_seletion")
    code = fields.Char(related="material_name.code")
    number = fields.Char(string="申请数量")

    @api.one
    @api.depends("material_name")
    def material_seletion(self):
        """
        获取最大数量
        :return:
        """
        odoo = self.env["itsm.material_management"].search([("code", "=", self.code)])
        number1 = 0
        for record in odoo:
            number1 = number1 + int(record.total_quantity)
        self.max_number = str(number1)

    @api.onchange("number")
    def get_number_data(self):
        if int(self.number) > int(self.max_number):
            raise UserError("申请数量不可大于仓库物料数量")

class select_user(models.Model):
    """
    指定接单人
    """
    _name = "itsm.select_user"

    itsm_id = fields.Char(string="事件id")
    name = fields.Many2one("res.users", string="接单人")

    def write_receiver(self):
        """
        修改接单人字段值
        :return:
        """
        odoo = self.env["itsm.event_processing"].search([("id", "=", self.itsm_id)])
        if odoo:
            odoo.write({"receiver": self.name.id, 'approval_state': 'appoint'})
