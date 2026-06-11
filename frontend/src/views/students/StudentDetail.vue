<template>
  <div class="page-container" v-if="student">
    <div class="detail-card">
      <div class="detail-header">
        <el-avatar :size="56" class="detail-avatar">
          {{ student.name?.charAt(0) }}
        </el-avatar>
        <div class="detail-title">
          <h2>{{ student.name }}</h2>
          <p>{{ student.student_no }} | {{ student.class_name }}</p>
        </div>
      </div>

      <div class="detail-grid">
        <div class="detail-item">
          <span class="detail-label">性别</span>
          <span class="detail-value">
            <span class="gender-tag" :class="student.gender">{{ student.gender === 'male' ? '男' : '女' }}</span>
          </span>
        </div>
        <div class="detail-item">
          <span class="detail-label">年龄</span>
          <span class="detail-value">{{ student.age || '-' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">电话</span>
          <span class="detail-value">{{ student.phone || '-' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">邮箱</span>
          <span class="detail-value">{{ student.email || '-' }}</span>
        </div>
        <div class="detail-item full">
          <span class="detail-label">地址</span>
          <span class="detail-value">{{ student.address || '-' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">状态</span>
          <span class="detail-value">
            <span class="status-tag" :class="student.status">{{ student.status === 'normal' ? '正常' : '待审核' }}</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import request from '../../api'

const route = useRoute()
const student = ref(null)

onMounted(async () => {
  student.value = await request.get(`/students/${route.params.id}/`)
})
</script>

<style scoped>
.page-container { max-width: 640px; }

.detail-card {
  background: #fff; border-radius: 14px; padding: 28px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.045);
}

.detail-header {
  display: flex; align-items: center; gap: 18px;
  padding-bottom: 24px; border-bottom: 1px solid #f0f0f0; margin-bottom: 24px;
}

.detail-avatar {
  background: linear-gradient(135deg, #6388a0, #b7d9c8);
  color: #fff; font-size: 22px; font-weight: 600;
}

.detail-title h2 { font-size: 20px; font-weight: 600; color: #3a4f63; margin: 0; }
.detail-title p { font-size: 13px; color: #999; margin-top: 4px; }

.detail-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
}

.detail-item { display: flex; flex-direction: column; gap: 6px; }
.detail-item.full { grid-column: 1 / -1; }

.detail-label { font-size: 12px; color: #999; }
.detail-value { font-size: 14px; color: #333; }

.gender-tag { display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 500; }
.gender-tag.male { background: rgba(99,136,160,0.1); color: #6388a0; }
.gender-tag.female { background: rgba(233,201,188,0.2); color: #c4887a; }

.status-tag { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.status-tag.normal { background: rgba(183,217,200,0.2); color: #5a9a78; }
.status-tag.pending { background: rgba(233,201,188,0.2); color: #c4887a; }
</style>
