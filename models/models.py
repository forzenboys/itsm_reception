# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api

class Itsm_Reception_Business_Applications(models.Model):
    """
    业务申请模型表
    """
    _name = 'itsm.reception_business_applications'

    itsm_id = fields.Char("id")
    name = fields.Char(string="名称")
    applicant_name = fields.Many2one("res.users", string="申请人姓名", store=True, compute="_compute_name")
    applicant_department = fields.Many2one('itsm.department',string='申请部门')
    number = fields.Char('服务单编号')
    phone = fields.Char(string="联系电话")
    execution_time = fields.Datetime(string="执行时间")
    title = fields.Char(string="标题", store=True, compute="_compute_name")
    emergency = fields.Selection([("低", "低"), ("中", "中"), ("高", "高"), ("紧急", "紧急")], string="优先级", default="低")
    enclosure = fields.Binary(string="附件")
    describe = fields.Text(string="描述")
    response_time_limit = fields.Char(string="响应时限（时）")
    slove_time_limit = fields.Char(string="解决时限（时）")

    def create_business_applications(self, name, id, emergency, response_time_limit, slove_time_limit):
        """
        创建业务申请模块
        """
        data = {
            "name": str(name),
            "itsm_id": str(id),
            "emergency": str(emergency),
            "response_time_limit": str(response_time_limit),
            "slove_time_limit": str(slove_time_limit),
        }
        self.create(data)

    def update_business_applications(self, name, id, emergency, response_time_limit, slove_time_limit):
        """
        更新业务申请模块
        """
        itsm_id = str(id)
        this = self.search([("itsm_id", "=", itsm_id)])
        data = {
            "name": str(name),
            "emergency": str(emergency),
            "response_time_limit": str(response_time_limit),
            "slove_time_limit": str(slove_time_limit),
        }
        this.write(data)

    def unlink_business_applications(self,id):
        """
        删除业务申请模块
        """
        itsm_id = str(id)
        this = self.search([("itsm_id", "=", itsm_id)])
        this.unlink()

    @api.depends("phone")
    def _compute_name(self):
        """
        表单自动填写申请人姓名
        """
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TITLE = "{},{}".format(now_time, self.name)
        self.applicant_name = self.env.user.id,
        self.title = TITLE

    def get_applications_data(self):
        """
        数据调用：
        model:工单管理
        :return:
        """
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        coding = "IM" + now_time
        data = {
            "name": self.name,
            "working_condition": "处理中",
            "server_id": self.number,
            "priority": self.emergency,
            "task_coding": coding,
            "title": self.title,
            "applicant_name": self.applicant_name.id,
            "phone": self.phone,
            "create_time": create_time,
            "applicant_department": self.applicant_department.id,
            "describe": self.describe,
            "response_time_limit": self.response_time_limit,
            "slove_time_limit": self.slove_time_limit
        }
        self.env["itsm.work_order"].search([]).create(data)
        print(data)

    def return_view(self):
        """
        定义返回视图按钮
        :return:
        """
        action = {
            "type": "ir.actions.act_window",
            "name": "返回视图",
            "res_model": "itsm.reception_business_applications",
            "view_mode": "kanban,form",
        }
        return action

class Itsm_Reception_Trouble_Repair(models.Model):
    """
    故障申请模型表
    """
    _name = 'itsm.reception_trouble_repair'

    itsm_id = fields.Char("id")
    name = fields.Char(string="名称")
    applicant_name = fields.Many2one("res.users", string="申请人姓名", compute="_compute_name", store=True)
    service_type = fields.Many2one('itsm.service_type', string='故障类别')
    applicant_department = fields.Many2one('itsm.department',string='故障事件部门')
    phone = fields.Char(string="手机号码")
    telephone = fields.Char(string="联系电话")
    device_number = fields.Char(string='设备资产编号')
    position = fields.Char(related="applicant_name.position_id.name", string="位置", store=True)
    room_number = fields.Char(related="applicant_name.room_number", string="房间号", store=True)
    title = fields.Char(string="标题", store=True)
    fault_description = fields.Text(string="故障描述")
    time_of_appointment = fields.Datetime(string="预约上门时间")
    number = fields.Char('服务单编号')
    enclosure = fields.Binary(string="附件")
    response_time_limit = fields.Char(string="响应时限（时）")
    slove_time_limit = fields.Char(string="解决时限（时）")

    def get_applications_data(self):
        """
        事件处理：
        model:itsm.event_processing
        :return:
        """
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        coding = "IM" + now_time
        priority = self.env["itsm.service_catalogue"].search([("id", "=", self.itsm_id)]).level
        data = {
            "name": self.name,
            "working_condition": "处理中",
            "priority": priority,
            "server_id": self.number,
            "task_coding": coding,
            "title": self.title,
            "applicant_name": self.applicant_name.id,
            "applicant_department": self.applicant_department.id,
            "phone": self.phone,
            "create_time": create_time,
            "enclosure": self.enclosure,
            "describe": self.fault_description,
            "response_time_limit": self.response_time_limit,
            "slove_time_limit": self.slove_time_limit,
            "service_type": self.service_type.id
        }
        self.env["itsm.event_processing"].search([]).create(data)
        print(data)

    def create_trouble_repair(self, name, id, emergency, response_time_limit, slove_time_limit,service_type):
        """
        创建故障申请模块
        """
        data = {
            "name": str(name),
            "itsm_id": str(id),
            "emergency": str(emergency),
            "response_time_limit": str(response_time_limit),
            "slove_time_limit": str(slove_time_limit),
            "service_type":service_type
        }
        self.create(data)

    def update_trouble_repair(self, name, id, emergency, response_time_limit, slove_time_limit,service_type):
        """
        更新故障申请模块
        """
        itsm_id = str(id)
        this = self.search([("itsm_id", "=", itsm_id)])
        data = {
            "name": str(name),
            "emergency": str(emergency),
            "response_time_limit": str(response_time_limit),
            "slove_time_limit": str(slove_time_limit),
            "service_type": service_type
        }
        this.write(data)

    def unlink_trouble_repair(self, id):
        """
        删除故障申请模块
        """
        itsm_id = str(id)
        this = self.search([("itsm_id", "=", itsm_id)])
        this.unlink()

    @api.depends("phone", "telephone", "fault_description")
    def _compute_name(self):
        """
        表单自动填写申请人姓名
        """
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TITLE = "{},{}".format(now_time, self.name)
        self.applicant_name = self.env.user.id,
        self.title = TITLE

    def return_view(self):
        """
        定义返回视图按钮
        :return:
        """
        action = {
            "type": "ir.actions.act_window",
            "name": "返回视图",
            "res_model": "itsm.reception_trouble_repair",
            "view_mode": "kanban,form",
        }
        return action



class Itsm_Failure_registration(models.Model):
    """
    故障登记模块
    """
    _name = "itsm.failure_registration"

    itsm_id = fields.Char("id")
    name = fields.Char(string="名称")
    applicant_name = fields.Many2one("res.users", string="申请人姓名", required=True)
    phone = fields.Char(string="手机号码", required=True)
    telephone = fields.Char(string="联系电话")
    area = fields.Char(related="applicant_name.area_id.name", string="区域", store=True)
    position = fields.Char(related="applicant_name.position_id.name", string="位置", store=True)
    room_number = fields.Char(related="applicant_name.room_number", string="房间号", store=True)
    title = fields.Char(string="标题", store=True)
    device_number = fields.Char("设备资产编号")
    fault_description = fields.Text(string="故障描述", required=True)
    time_of_appointment = fields.Datetime(string="预约上门时间", required=True)
    enclosure = fields.Binary(string="附件")
    order_attachment_number = fields.Integer(compute='_compute_order_attachment_number', string='测试附件')
    classification = fields.Selection([("故障报修", "故障报修")], string="所属分类")
    classification2 = fields.Selection([("软件故障", "软件故障"), ("硬件故障", "硬件故障")], string="类")
    classification3 = fields.Char(string="属")
    source_of_failure = fields.Selection([("电话", "电话"), ("自助", "自助"), ("其他", "其他"), ("邮件", "邮件"), ("运维中发现", "运维中发现"),
                                          ("第三方系统", "第三方系统"), ("微信", "微信"), ("app", "app")], string="故障来源",
                                         default="电话")
    emergency = fields.Selection([("低", "低"), ("中", "中"), ("高", "高"), ("紧急", "紧急")], string="优先级", default="低")

    def get_applications_data(self):
        """
        事件处理：
        model:itsm.event_processing
        :return:
        """
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        coding = "IM" + now_time
        data = {
            "name": "故障登记",
            "working_condition": "处理中",
            "priority": self.emergency,
            "task_coding": coding,
            "title": self.title,
            "applicant_name": self.applicant_name.id,
            "device_number":self.device_number,
            "phone": self.phone,
            "create_time": create_time,
            "describe": self.fault_description,
            "response_time_limit": "36", #故障申请表单默认响应的时间
            "slove_time_limit": "36"  #故障申请表单默认响应的时间
        }
        self.env["itsm.event_processing"].search([]).create(data)

class Itsm_Satisfaction_Return(models.Model):
    """
    满意度回访模型
    """
    _name = "itsm.satisfaction_return"

    itsm_id = fields.Char("id")
    name = fields.Char(string="服务目录")
    working_condition = fields.Char(string="编号")
    title = fields.Char(string="标题")
    evaluation_results = fields.Selection([("1", "★"), ("2", "★★"), ("3", "★★★"), ("4", "★★★★"), ("5", "★★★★★")],
                                          default="3", string="评价结果")
    create_time = fields.Char(string="提交时间")
    """
    评分表所需字段
    """
    all_evaluation_results = fields.Selection([("1", "★"), ("2", "★★"), ("3", "★★★"), ("4", "★★★★"), ("5", "★★★★★")],
                                              default="3", string="整体评价")
    service_attitude = fields.Selection([("1", "★"), ("2", "★★"), ("3", "★★★"), ("4", "★★★★"), ("5", "★★★★★")],
                                        default="3", string="服务态度")
    quality_of_service = fields.Selection([("1", "★"), ("2", "★★"), ("3", "★★★"), ("4", "★★★★"), ("5", "★★★★★")],
                                          default="3", string="服务质量")
    response_speed = fields.Selection([("1", "★"), ("2", "★★"), ("3", "★★★"), ("4", "★★★★"), ("5", "★★★★★")],
                                      default="3", string="响应速度")
    label = fields.Many2many("itsm.evaluation_tag", string="评价印象")

    def write_data(self):
        evaluation_results_data = (int(self.all_evaluation_results) + int(self.service_attitude) + int(self.quality_of_service) + int(self.response_speed)) / 4
        char_data = int(evaluation_results_data)
        now_time = datetime.datetime.now().strftime('%Y-%m')
        data = {
            "evaluation_results": str(char_data),
            "create_time": str(now_time)
        }
        self.write(data)#修改评价结果和评价时间
        """
        #根据评价时间创建图形界面字段：月份
        todo:目前只写7月份字段
        """
        satisfaction_measure_time = datetime.datetime.now().strftime('%Y') #获取当前年份
        satisfaction_measure_data = {
            "time": satisfaction_measure_time
        }
        satisfaction_measure = self.env["itsm.satisfaction_measure"].search([("time", "=", satisfaction_measure_time)]) #查找年份相同的数据
        if not satisfaction_measure:  #判断数据是否存在
            self.env["itsm.satisfaction_measure"].search([]).create(satisfaction_measure_data) #如果不存在则创建该月份数据
        action = {
            "type": "ir.actions.act_window",
            "name": "视图", #名称
            "res_model": "itsm.satisfaction_return", #返回视图
            "view_mode": "tree,form", #视图类型
        }
        return action

    @api.model
    def set_star_data(self, data, name, res_id):
        """
        将前端获取的数据写进itsm.satisfaction_return 中(星标)
        """
        new_data = {
            name: str(data)
        }
        odoo = self.env["itsm.satisfaction_return"].search([("id", "=", int(res_id))])
        odoo.write(new_data)

    @api.model
    def get_star_data(self, value):
        """
        返回数据到星标中
        """
        return int(value)

class Satisfaction_measure(models.Model):
    """
    图形数据展示
    """
    _name = "itsm.satisfaction_measure"

    time = fields.Char(string="客户评价月份满意度平均值")
    month_data = fields.Char(string="1月数据")
    month2_data = fields.Char(string="2月数据")
    month3_data = fields.Char(string="3月数据")
    month4_data = fields.Char(string="4月数据")
    month5_data = fields.Char(string="5月数据")
    month6_data = fields.Char(string="6月数据")
    month7_data = fields.Char(string="7月数据")
    month8_data = fields.Char(string="8月数据")
    month9_data = fields.Char(string="9月数据")
    month10_data = fields.Char(string="10月数据")
    month11_data = fields.Char(string="11月数据")
    month12_data = fields.Char(string="12月数据")
    avg_all_evaluation_results1 = fields.Char(string="整体评价平均数")
    avg_service_attitude1 = fields.Char(string="服务态度平均数")
    avg_quality_of_service1 = fields.Char(string="服务质量平均数")
    avg_response_speed1 = fields.Char(string="响应速度平均数")

    @api.model
    def create_data(self, time, id):
        month = time + "-01"
        month2 = time + "-02"
        month3 = time + "-03"
        month4 = time + "-04"
        month5 = time + "-05"
        month6 = time + "-06"
        month7 = time + "-07"
        month8 = time + "-08"
        month9 = time + "-09"
        month10 = time + "-10"
        month11 = time + "-11"
        month12 = time + "-12"

        satisfaction_return = self.env["itsm.satisfaction_return"] #实例化综合评分表对象
        data1 = 0
        records1 = satisfaction_return.search([("create_time", "=", month)])#查找1月份数据
        length1 = len(records1)
        if length1 == 0:
            length1 = 1
        for record in records1: #查找1月份数据
            data1 = data1 + int(record.evaluation_results)
        data2 = 0
        records2 = satisfaction_return.search([("create_time", "=", month2)])#查找2月份数据
        length2 = len(records2)
        if length2 == 0:
            length2 = 1
        for record in records2: #查找2月份数据
            data2 = data2 + int(record.evaluation_results)
        data3 = 0
        records3 = satisfaction_return.search([("create_time", "=", month3)])#查找3月份数据
        length3 = len(records3)
        if length3 == 0:
            length3 = 1
        for record in records3:#查找3月份数据
            data3 = data3 + int(record.evaluation_results)
        data4 = 0
        records4 = satisfaction_return.search([("create_time", "=", month4)])
        length4 = len(records4)
        if length4 == 0:
            length4 = 1
        for record in records4:#查找4月份数据
            data4 = data4 + int(record.evaluation_results)
        data5 = 0
        records5 = satisfaction_return.search([("create_time", "=", month5)])
        length5 = len(records5)
        if length5 == 0:
            length5 = 1
        for record in records5:#查找5月份数据
            data5 = data5 + int(record.evaluation_results)
        data6 = 0
        records6 = satisfaction_return.search([("create_time", "=", month6)])
        length6 = len(records6)
        if length6 == 0:
            length6 = 1
        for record in records6:#查找6月份数据
            data6 = data6 + int(record.evaluation_results)
        data7 = 0
        records7 = satisfaction_return.search([("create_time", "=", month7)])
        length7 = len(records7)
        if length7 == 0:
            length7 = 1
        for record in records7:#查找7月份数据
            data7 = data7 + int(record.evaluation_results)
        data8 = 0
        records8 = satisfaction_return.search([("create_time", "=", month8)])
        length8 = len(records8)
        if length8 == 0:
            length8 = 1
        for record in records8:#查找8月份数据
            data8 = data8 + int(record.evaluation_results)
        data9 = 0
        records9 = satisfaction_return.search([("create_time", "=", month9)])
        length9 = len(records9)
        if length9 == 0:
            length9 = 1
        for record in records9:#查找9月份数据
            data9 = data9 + int(record.evaluation_results)
        data10 = 0
        records10 = satisfaction_return.search([("create_time", "=", month10)])
        length10 = len(records10)
        if length10 == 0:
            length10 = 1
        for record in records10:#查找10月份数据
            data10 = data10 + int(record.evaluation_results)
        data11 = 0
        records11 = satisfaction_return.search([("create_time", "=", month11)])
        length11 = len(records11)
        if length11 == 0:
            length11 = 1
        for record in records11:#查找11月份数据
            data11 = data11 + int(record.evaluation_results)
        data12 = 0
        records12 = satisfaction_return.search([("create_time", "=", month12)])
        length12 = len(records12)
        if length12 == 0:
            length12 = 1
        for record in records12:#查找12月份数据
            data12 = data12 + int(record.evaluation_results)

        all_evaluation_results1 = 0
        service_attitude1 = 0
        quality_of_service1 = 0
        response_speed1 = 0
        details_data = satisfaction_return.search([])
        all_length = len(details_data)
        for details in details_data:
            all_evaluation_results1 = all_evaluation_results1 + int(details.all_evaluation_results)
            service_attitude1 = service_attitude1 + int(details.service_attitude)
            quality_of_service1 = quality_of_service1 + int(details.quality_of_service)
            response_speed1 = response_speed1 + int(details.response_speed)
        print(all_evaluation_results1, service_attitude1, quality_of_service1, response_speed1, all_length)
        odoo = self.env["itsm.satisfaction_measure"].search([("id", "=", id)]) #查找当前id的对象
        satisfaction_measure_data = {
            "month_data": str(data1 / length1),
            "month2_data": str(data2 / length2),
            "month3_data": str(data3 / length3),
            "month4_data": str(data4 / length4),
            "month5_data": str(data5 / length5),
            "month6_data": str(data6 / length6),
            "month7_data": str(data7 / length7),
            "month8_data": str(data8 / length8),
            "month9_data": str(data9 / length9),
            "month10_data": str(data10 / length10),
            "month11_data": str(data11 / length11),
            "month12_data": str(data12 / length12),
            "avg_all_evaluation_results1": str(all_evaluation_results1 / all_length),
            "avg_service_attitude1": str(service_attitude1 / all_length),
            "avg_quality_of_service1": str(quality_of_service1 / all_length),
            "avg_response_speed1": str(response_speed1 / all_length)
        }
        odoo.write(satisfaction_measure_data)
