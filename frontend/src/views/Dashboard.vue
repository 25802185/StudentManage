<template>
  <div>
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="6" v-for="item in cards" :key="item.label">
        <el-card shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 32px; color: #409eff; font-weight: bold">{{ item.value }}</div>
            <div style="color: #999; margin-top: 8px">{{ item.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>成绩等级分布</template>
          <div ref="scoreChart" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>班级学生人数</template>
          <div ref="classChart" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '../api'

const cards = ref([])
const scoreChart = ref(null)
const classChart = ref(null)

onMounted(async () => {
  const data = await request.get('/stats/dashboard/')
  cards.value = [
    { label: '学生总数', value: data.student_count },
    { label: '教师总数', value: data.teacher_count },
    { label: '班级数量', value: data.class_count },
    { label: '课程数量', value: data.course_count },
  ]

  await nextTick()

  const scoreData = await request.get('/stats/score-distribution/')
  const pie = echarts.init(scoreChart.value)
  pie.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie', radius: '60%',
      data: Object.entries(scoreData).map(([name, value]) => ({ name, value })),
    }],
  })

  const classData = await request.get('/stats/class-students/')
  const bar = echarts.init(classChart.value)
  bar.setOption({
    tooltip: {},
    xAxis: { type: 'category', data: classData.map(c => c.name) },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: classData.map(c => c.count) }],
  })
})
</script>
