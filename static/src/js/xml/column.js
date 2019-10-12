odoo.define("itsm.column_chart", function(require) {
	"use strict";

	var AbstractField = require("web.AbstractField");
	var field_registry = require("web.field_registry");

	var column_chart = AbstractField.extend({
		init: function() {
			this._super.apply(this, arguments);
		},
		_render: function() {
			var self = this;
			var root = $("<div style='width: 600px; height: 400px; margin: 0 auto'></div>");
			self
				._rpc({
					model: "itsm.satisfaction_measure",
					method: "create_data",
					args: [self.value, self.res_id]
				});
			var chart = {
				type: 'column'
			};
			var title = {
				text: ''
			};
			var subtitle = {
				text: ''
			};
			var xAxis = {
				categories: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
				crosshair: true,
				labels: {
					y: 20,
				},

			};
			var yAxis = {
				min: 0,
				title: {
					//         text: '降雨量 (mm)'
					x: 1500,
				},
				labels: {
					x: 10,
				},
			};
			var tooltip = {
				headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
				pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
					'<td style="padding:0"><b>{point.y:.1f} 评分值</b></td></tr>',
				footerFormat: '</table>',
				shared: true,
				useHTML: true
			};
			var plotOptions = {
				column: {
					pointPadding: 0.2,
					borderWidth: 5
				}
			};
			var credits = {
				enabled: false
			};
			var legend = {
				// layout: 'horizontal', // default
				itemDistance: 70,
			};
			var labels = {
				items: [{
					html: '客户满意度',
					style: {
						left: '50px',
						top: '18px',
						color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
					}
				}]
			};
			var series = [{
				type: 'column',
				name: '综合',
				data: [parseInt(self.recordData.month_data), parseInt(self.recordData.month2_data), parseInt(self.recordData
						.month3_data), parseInt(self.recordData.month4_data), parseInt(self.recordData.month5_data), parseInt(
						self.recordData.month6_data), parseInt(self.recordData.month7_data), parseInt(self.recordData.month8_data),
					parseInt(self.recordData.month9_data), parseInt(self.recordData.month10_data), parseInt(self.recordData.month11_data),
					parseInt(self.recordData.month12_data)
				],
				color: 'rgb(120,223,215)',
				shadow: {
					color: 'rgb(120,223,215)',
					width: 1,
					offsetX: 0,
					offsetY: 0
				}
			},
			{
				type: 'spline',
				name: '曲线',
				data: [3, 2.67, 1, 1.33, 3.33, 1,1.4,1,2.5,1.1,2.55,3.66],
				marker: {
					lineWidth: 2,
					lineColor: 'rgb(120,223,215)',
					fillColor: 'white',
				},
				color: 'rgb(120,223,215)',
			},
			{
				type: 'pie',
				name: '工单评价',
				data: [{
						name: '整体评价',
						y: parseInt(self.recordData.avg_all_evaluation_results1),
						color: 'rgb(120,223,215)' // Jane 的颜色
					}, {
						name: '服务态度',
						y: parseInt(self.recordData.avg_quality_of_service1),
						color: 'rgb(120,223,215)' // John 的颜色
					}, {
						name: '服务质量',
						y: parseInt(self.recordData.avg_service_attitude1),
						color: 'rgb(120,223,215)' // Joe 的颜色
					},
					{
						name: '响应速度',
						y: parseInt(self.recordData.avg_response_speed1),
						color: 'rgb(120,223,215)' // Joe 的颜色
					}
				],
				center: [100, 80],
				size: 100,
				showInLegend: false,
				dataLabels: {
					enabled: false
				}
			}];

			var json = {};
			json.labels = labels;
			json.chart = chart;
			json.title = title;
			json.subtitle = subtitle;
			json.tooltip = tooltip;
			json.xAxis = xAxis;
			json.yAxis = yAxis;
			json.series = series;
			json.plotOptions = plotOptions;
			json.credits = credits;
			json.legend = legend;
			root.highcharts(json);
			this.$el.html(root);
			console.log(self)
		}
	});

	field_registry.add("column_chart", column_chart);
	return column_chart;
});
