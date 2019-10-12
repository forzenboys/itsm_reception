odoo.define("zhu_chart.zhu_chart", function(require) {
	"use strict";

	var AbstractField = require("web.AbstractField");
	var field_registry = require("web.field_registry");

	var zhu_chart = AbstractField.extend({

		init: function() {
			this._super.apply(this, arguments);
		},
		_render: function() {
			var self = this;
			var root = $("<div style='width: 715px; height: 400px; margin: 0 auto'>1</div>");
			var chart = {
				type: 'pie',
				options3d: {
					enabled: true,
					alpha: 45
				}
			};
			var title = {
				text: ''
			};
			var subtitle = {
				text: ''
			};

			var plotOptions = {
				pie: {
					innerSize: 100,
					depth: 45
				}
			};
			var series = [{
				name: '',
				data: [
					['1', 0],
					['2', 0],
					['3', 0],
					['4', 1],
					['5', 5],
					['6', 5],
					['7', 4],
					['8', 4],
					['9', 1],
					['10', 1],
					['11', 11],
					['12', 1],
				]
			}];

			var json = {};
			json.chart = chart;
			json.title = title;
			json.subtitle = subtitle;
			json.plotOptions = plotOptions;
			json.series = series;
			root.highcharts(json);
			this.$el.html(root);
			console.log(root)
		}
	});

	field_registry.add("zhu_chart", zhu_chart);
	return zhu_chart;
});
