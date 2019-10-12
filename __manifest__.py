# -*- coding: utf-8 -*-
{
    'name': "itsm_reception",

    'summary': """itsm服务台""",

    'description': """添加工单图表筛选等功能""",

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '12.1.1',
    'depends': ['base', 'board', 'barcodes', 'itsm_stock','web_dashboard'],
    'external_dependencies': {'python': ['pystrich']},
    'data': [
        'security/itsm_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menus.xml',
        'views/templates.xml',
        'static/src/js/xml/zhuxing.xml',
        "views/operation-center/views.xml",
        "views/settings/organization/views.xml",
        "views/settings/service/views.xml",
        "views/settings/system/views.xml",
        "views/operation-center/menus.xml",
        "views/settings/organization/menus.xml",
        "views/settings/service/menus.xml",
        "views/settings/system/menus.xml",
        'views/itsm_device_manage.xml',
        'views/itsm_device_check.xml',
        'views/itsm_device_menu.xml',
        'wizard/print_device_label.xml',
        'report/device_label_reports.xml',
        'report/device_label_templates.xml',
        'wizard/itsm_device_check_lines.xml',
        # 'views/itsm_workevent.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}