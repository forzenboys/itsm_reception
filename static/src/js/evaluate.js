odoo.define("itsm.evaluate",function(require){
    "use strict";

    var AbstractField = require("web.AbstractField");
    var field_registry = require("web.field_registry");

    var Evaluate =AbstractField.extend({
        init: function() {
          this._super.apply(this, arguments);
        },
        _render: function () {
            var self = this;
            this.vm = new Vue({
                template:"<el-button plain @click='open1'>提交</el-button>",
                methods:{
                    open1(){
                        this.$notify({
                            title:'成功',
                            message:'您的申请已提交',
                            type:'success'
                        });
                    },
                }
            });
            this.$el.html(this.vm.$el);
        }
    });
    field_registry.add("evaluate", Evaluate);

    return Evaluate;

});