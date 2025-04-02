<template>
  <div ref="chart" style="width: 95%; height: 400px;"></div>
</template>

<script>
import * as echarts from 'echarts';
import { ref, onMounted } from 'vue';
import {getTopFlweor} from "@/api/admin.js";

export default {
  name: 'TopFlowersChart',
  setup() {
    const chart = ref(null);

    onMounted(async () => {
      const topFlowers = await getTopFlweor();

      const myChart = echarts.init(chart.value);

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: 'category',
          data: topFlowers.map(flower => flower.name),
          axisLabel: {
            interval: 0, // 强制显示所有标签
            margin: 8,   // 调整标签与轴的距离
            fontSize: 12, // 调整字体大小
            color: '#6c757d' // 调整字体颜色
          }
        },
        series: [
          {
            name: 'Sales',
            type: 'bar',
            data: topFlowers.map(flower => flower.sales),
            label: {
              show: true,
              position: 'right'
            },
            itemStyle: {
              color: '#4a6b57'
            }
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