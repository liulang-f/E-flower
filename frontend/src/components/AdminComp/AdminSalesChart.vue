<template>
  <div ref="chart" style="width: 100%; height: 300px;"></div>
</template>

<script>
import * as echarts from 'echarts';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import {getSalesTrend} from "@/api/admin.js";

export default {
  name: 'SalesTrendChart',
  setup() {
    const chart = ref(null);

    onMounted(async () => {
      const myChart = echarts.init(chart.value);

      // 从后端获取数据
      try {
        const { days, order_counts, total_sales } = await getSalesTrend();

        const option = {
          title: {
            text: '',
            left: 'center',
            textStyle: {
              color: '#333',
              fontSize: 16
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: ['订单数量', '订单总金额'],
            left: 'left'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: days,
            axisLine: {
              lineStyle: {
                color: '#6c757d'
              }
            },
            axisLabel: {
              color: '#6c757d'
            }
          },
          yAxis: [
            {
              type: 'value',
              name: '订单数量',
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
            },
            {
              type: 'value',
              name: '订单总金额',
              axisLine: {
                lineStyle: {
                  color: '#6c757d'
                }
              },
              axisLabel: {
                color: '#6c757d',
                formatter: '{value} 元'
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
              name: '订单数量',
              type: 'line',
              yAxisIndex: 0,
              data: order_counts,
              itemStyle: {
                color: '#4a6b57'
              }
            },
            {
              name: '订单总金额',
              type: 'line',
              yAxisIndex: 1,
              data: total_sales,
              itemStyle: {
                color: '#ff6b6b'
              }
            }
          ]
        };

        myChart.setOption(option);
      } catch (error) {
        console.error('Failed to fetch sales trend data:', error);
      }

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