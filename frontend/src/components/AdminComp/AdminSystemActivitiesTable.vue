<template>
  <div ref="chart" style="width: 100%; height: 300px;"></div>
</template>

<script>
import * as echarts from 'echarts';
import { ref, onMounted } from 'vue';

export default {
  name: 'SystemActivityChart',
  setup() {
    const chart = ref(null);

    onMounted(() => {
      const myChart = echarts.init(chart.value);

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: ['Orders', 'Users', 'Page Views'],
          textStyle: {
            color: '#6c757d'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
            axisLine: {
              lineStyle: {
                color: '#6c757d'
              }
            },
            axisLabel: {
              color: '#6c757d'
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            axisLine: {
              lineStyle: {
                color: '#6c757d'
              }
            },
            axisLabel: {
              color: '#6c757d'
            },
            splitLine: {
              lineStyle: {
                color: '#f1f1f1'
              }
            }
          }
        ],
        series: [
          {
            name: 'Orders',
            type: 'line',
            stack: 'Total',
            smooth: true,
            lineStyle: {
              width: 0
            },
            showSymbol: false,
            areaStyle: {
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(74, 107, 87, 0.8)'
                },
                {
                  offset: 1,
                  color: 'rgba(74, 107, 87, 0.1)'
                }
              ])
            },
            emphasis: {
              focus: 'series'
            },
            data: [140, 90, 120, 180, 130, 140, 130]
          },
          {
            name: 'Users',
            type: 'line',
            stack: 'Total',
            smooth: true,
            lineStyle: {
              width: 0
            },
            showSymbol: false,
            areaStyle: {
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(72, 219, 251, 0.8)'
                },
                {
                  offset: 1,
                  color: 'rgba(72, 219, 251, 0.1)'
                }
              ])
            },
            emphasis: {
              focus: 'series'
            },
            data: [120, 82, 91, 154, 162, 140, 130]
          },
          {
            name: 'Page Views',
            type: 'line',
            stack: 'Total',
            smooth: true,
            lineStyle: {
              width: 0
            },
            showSymbol: false,
            areaStyle: {
              opacity: 0.8,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(254, 202, 87, 0.8)'
                },
                {
                  offset: 1,
                  color: 'rgba(254, 202, 87, 0.1)'
                }
              ])
            },
            emphasis: {
              focus: 'series'
            },
            data: [320, 232, 201, 334, 390, 330, 320]
          }
        ]
      };

      myChart.setOption(option);

      window.addEventListener('resize', function() {
        myChart.resize();
      });
    });

    return {
      chart
    };
  }
}
</script>