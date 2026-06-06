<template>
  <div>
    <h3>我的申请记录</h3>
    <el-table :data="list" border stripe>
      <el-table-column prop="field_name" label="修改字段" />
      <el-table-column prop="old_value" label="原值" />
      <el-table-column prop="new_value" label="新值" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="{ pending: 'warning', approved: 'success', rejected: 'danger' }[row.status]">
            {{ { pending: '待审核', approved: '已通过', rejected: '已驳回' }[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="审核备注" />
      <el-table-column prop="created_at" label="申请时间" width="180" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api'

const list = ref([])

onMounted(async () => {
  const data = await request.get('/info-changes/')
  list.value = data.results
})
</script>
