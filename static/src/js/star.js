odoo.define("star.Star", function(require) {
  "use strict";

  var AbstractField = require("web.AbstractField");
  var field_registry = require("web.field_registry");

  var Star = AbstractField.extend({
    init: function() {
      this._super.apply(this, arguments);
    },
    _render: function() {
      var self = this;
      console.log(this);

      this.vm = new Vue({
        template: "<el-rate v-model='value' @change='set_data' ></el-rate>",
        data() {
          return {
            value: 3,
          }
        },
        mounted() {
          var vm = this;
          self
            ._rpc({
              model: "itsm.satisfaction_return",
              method: "get_star_data",
              args: [self.value]
              })
            .then(function(result) {
               vm.value = result
            });
        },
        methods: {
          set_data(data){
            self
            ._rpc({
              model: "itsm.satisfaction_return",
              method: "set_star_data",
              args: [data,self.name,self.res_id]
              })
          }
        }
      }).$mount();

      this.$el.html(this.vm.$el);
    }
  });
  field_registry.add("star", Star);

  return Star;
});
