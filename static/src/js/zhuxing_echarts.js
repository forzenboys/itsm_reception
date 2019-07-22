// 基于准备好的dom，初始化echarts实例




        var myChart = echarts.init(document.getElementById('main'));
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: 'ECharts 入门示例'
            },
            tooltip: {},
            legend: {
                data:['用户满意度统计']
            },
            xAxis: {
                data: ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]
            },
            yAxis: {},
            series: [{
                name: '用户满意度统计',
                type: 'bar',
                data: [4.5, 5, 5, 5, 5, 5]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);