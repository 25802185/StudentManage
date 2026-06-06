<template>
  <div>
    <el-table :data="list" border stripe>
      <el-table-column prop="student_name" label="学生" />
      <el-table-column prop="field_name" label="修改字段" />
      <el-table-column prop="old_value" label="原值" />
      <el-table-column prop="new_value" label="新值" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="{ pending: 'warning', approved: 'success', rejected: 'danger' }[row.status]">
            {{ { pending: '待审核', approved: '已通过', rejected: '已驳回' }[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="申请时间" width="180" />
      <el-table-column label="操作" width="200" v-if="userStore.userInfo?.role !== 'student'">
        <template #default="{ row }">
          <template v-if="row.status === 'pending'">
            <el-button size="small" type="success" @click="handleApprove(row)">通过</el-button>
            <el-button size="small" type="danger" @click="handleReject(row)">驳回</el-button>
          </template>
          <span v-else>{{ row.remark }}</span>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination style="margin-top: 16px; justify-content: center" v-model:current-page="page" :total="total" layout="prev, pager, next" @current-change="loadData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api'
import { useUserStore } from '../../store/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const list = ref([])
const total = ref(0)
const page = ref(1)

const loadData = async () => {
  const data = await request.get('/info-changes/', { params: { page: page.value } })
  list.value = data.results
  total.value = data.count
}

const handleApprove = (row) => {
  ElMessageBox.confirm('确认通过？').then(async () => {
    await request.put(`/info-changes/${row.id}/approve/`)
    ElMessage.success('已通过')
    loadData()
  })
}

const handleReject = (row) => {
  ElMessageBox.prompt('请输入驳回原因').then(async ({ value }) => {
    await request.put(`/info-changes/${row.id}/reject/`, { remark: value })
    ElMessage.success('已驳回')
    loadData()
  })
}

onMounted(loadData)
</script>
