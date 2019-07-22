odoo.define("pie_chart.Pie_chart", function(require) {
  "use strict";

  var AbstractField = require("web.AbstractField");
  var field_registry = require("web.field_registry");

  var Pie_chart = AbstractField.extend({
    init: function() {
      this._super.apply(this, arguments);
    },
    _render: function() {

//        self._rpc({
//              model: "itsm.satisfaction_measure",
//              method: "create_data",
//              })
       var self = this;
       var odoo = $("<div>1</div>");
       var chart = {
       plotBackgroundColor: null,
       plotBorderWidth: null,
       plotShadow: false
   };
   var title = {
      text: ''
   };
   var tooltip = {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
   };
   var plotOptions = {
      pie: {
         allowPointSelect: true,
         cursor: 'pointer',
         dataLabels: {
            enabled: true,
            format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
            style: {
               color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
            }
         }
      }
   };
  console.log(self.recordData)
   var series= [{
      type: 'pie',
      name: 'Browser share',
      data: [
         [self.odoo_data,   45.0],
         ['IE',       26.8],
         ['hjm', 12.8],
         ['Safari',    8.5],
         ['Opera',     6.2],
         ['Others',   0.7]
      ]
   }];
   var json = {};
   json.chart = chart;
   json.title = title;
   json.tooltip = tooltip;
   json.series = series;
   json.plotOptions = plotOptions;
   odoo.highcharts(json);
   this.$el.html(odoo);
    }
  });

  field_registry.add("pie_chart", Pie_chart);
  return Pie_chart;
});
