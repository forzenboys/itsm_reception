odoo.define("measure_chart.measure_chart", function(require) {
  "use strict";

  var AbstractField = require("web.AbstractField");
  var field_registry = require("web.field_registry");

  var measure_chart = AbstractField.extend({
    init: function() {
      this._super.apply(this, arguments);
    },
    _render: function() {
       var self = this;
       var root = $("<div>1</div>");
       var chart = {
      type: 'gauge',
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false
   };
   var title = {
      text: ''
   };

   var pane = {
      startAngle: -150,
      endAngle: 150,
      background: [{
         backgroundColor: {
            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
            stops: [
               [0, '#FFF'],
               [1, '#333']
            ]
         },
         borderWidth: 0,
         outerRadius: '109%'
      }, {
         backgroundColor: {
            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
            stops: [
               [0, '#333'],
               [1, '#FFF']
            ]
         },
         borderWidth: 1,
         outerRadius: '107%'
     }, {
         // default background
     }, {
         backgroundColor: '#DDD',
         borderWidth: 0,
         outerRadius: '105%',
         innerRadius: '103%'
     }]
   };

   // the value axis
   var yAxis = {
      min: 0,
      max: 100,

      minorTickInterval: 'auto',
      minorTickWidth: 0,
      minorTickLength: 0,
      minorTickPosition: 'inside',
      minorTickColor: '#666',

      tickPixelInterval: 0,
      tickWidth: 2,
      tickPosition: 'inside',
      tickLength: 10,
      tickColor: '#666',
      labels: {
         step: 2,
         rotation: 'auto'
      },
      title: {
         text: '好评率'
      },
      plotBands: [{
         from: 0,
         to: 40,
         color: '#55BF3B' // green
      }, {
         from: 40,
         to: 80,
         color: '#DDDF0D' // yellow
      }, {
         from: 80,
         to: 100,
         color: '#DF5353' // red
      }]
   };
    console.log(self);
   var series= [{
        name: 'Speed',
        data: [80],
        tooltip: {
           valueSuffix: ' test'
        }
   }];
   var json = {};
   json.chart = chart;
   json.title = title;
   json.pane = pane;
   json.yAxis = yAxis;
   json.series = series;

       root.highcharts(json);
       this.$el.html(root);
       console.log(root)
    }
  });
  field_registry.add("measure_chart", measure_chart);
  return measure_chart;
});
