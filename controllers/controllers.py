# -*- coding: utf-8 -*-
from odoo import http

class ItsmReception(http.Controller):
    @http.route('/itsm/zhuxing_echarts', csrf=False, auth='public')
    def zhuxing_echarts(self, **kwargs):
        list = http.request.env['itsm.satisfaction_measure'].search([])
        return http.request.render('itsm_reception.zhu_echarts', {'lists': list})

    @http.route('/itsm_reception/zhuxing_echarts_data', csrf=False, auth='public')
    def zhuxing_echarts_data(self, **kwargs):
        list = http.request.env['itsm.satisfaction_return'].search([]).set_satisfaction_measure_data()
        return list