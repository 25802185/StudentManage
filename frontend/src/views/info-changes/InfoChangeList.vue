<template>
  <div class="page-container">
    <!-- 标题栏 -->
    <div class="search-card">
      <div class="search-left">
        <span class="card-title-sm">信息审核</span>
      </div>
      <div class="search-right">
        <span class="pending-count" v-if="pendingCount > 0">{{ pendingCount }} 项待审核</span>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <el-table :data="list" style="width: 100%">
        <el-table-column prop="student_name" label="学生" width="100" />
        <el-table-column prop="field_name" label="修改字段" width="100">
          <template #default="{ row }">
            <span class="field-tag">{{ row.field_name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="old_value" label="原值" min-width="120" />
        <el-table-column prop="new_value" label="新值" min-width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <span class="status-tag" :class="row.status">
              {{ { pending: '待审核', approved: '已通过', rejected: '已驳回' }[row.status] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="申请时间" width="160" />
        <el-table-column label="操作" width="180" fixed="right" v-if="userStore.userInfo?.role !== 'student'">
          <template #default="{ row }">
            <template v-if="row.status === 'pending'">
              <el-button size="small" class="btn-mint-sm" @click="handleApprove(row)">通过</el-button>
              <el-button size="small" class="btn-delete" @click="handleReject(row)">驳回</el-button>
            </template>
            <span v-else class="remark-text">{{ row.remark || '-' }}</span>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination v-model:current-page="page" :total="total" layout="prev, pager, next" background @current-change="loadData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import request from '../../api'
import { useUserStore } from '../../store/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const list = ref([])
const total = ref(0)
const page = ref(1)
const pendingCount = ref(0)

const loadData = async () => {
  const data = await request.get('/students/info-changes/', { params: { page: page.value } })
  list.value = data.results
  total.value = data.count
  // 单独获取待审核总数
  try {
    const pendingData = await request.get('/students/info-changes/', { params: { status: 'pending', page_size: 1 } })
    pendingCount.value = pendingData.count || 0
  } catch {
    pendingCount.value = list.value.filter(r => r.status === 'pending').length
  }
}

const handleApprove = (row) => {
  ElMessageBox.confirm('确认通过该申请？', '提示', { type: 'info' }).then(async () => {
    await request.put(`/students/info-changes/${row.id}/approve/`)
    ElMessage.success('已通过')
    loadData()
  })
}

const handleReject = (row) => {
  ElMessageBox.prompt('请输入驳回原因', '驳回', { type: 'warning' }).then(async ({ value }) => {
    await request.put(`/students/info-changes/${row.id}/reject/`, { remark: value })
    ElMessage.success('已驳回')
    loadData()
  })
}

onMounted(loadData)
</script>

<style scoped>
.page-container { display: flex; flex-direction: column; gap: 16px; }

.search-card {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 22px; background: #fff; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.card-title-sm { font-size: 14px; font-weight: 600; color: #3a4f63; }

.pending-count {
  font-size: 12px; color: #c4887a; background: rgba(233,201,188,0.15);
  padding: 4px 12px; border-radius: 20px; font-weight: 500;
}

.table-card { background: #fff; border-radius: 14px; padding: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.045); }
.table-card :deep(.el-table) { border-radius: 10px; overflow: hidden; }
.table-card :deep(.el-table th.el-table__cell) { background: rgba(99,136,160,0.08) !important; color: #3a4f63; font-weight: 600; font-size: 13px; }
.table-card :deep(.el-table td.el-table__cell) { font-size: 13px; color: #555; border-bottom: 1px solid #f5f5f5; }
.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) { background: rgba(183,217,200,0.08) !important; }
.table-card :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) { background: #fafbfc; }

.field-tag {
  display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;
  background: rgba(99,136,160,0.08); color: #6388a0;
}

.status-tag { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.status-tag.pending { background: rgba(233,201,188,0.2); color: #c4887a; }
.status-tag.approved { background: rgba(183,217,200,0.2); color: #5a9a78; }
.status-tag.rejected { background: rgba(200,120,120,0.12); color: #b06060; }

.remark-text { font-size: 12px; color: #aaa; }

.btn-mint-sm { background: rgba(183,217,200,0.2); border: none; color: #5a9a78; border-radius: 6px; }
.btn-mint-sm:hover { background: #b7d9c8; color: #3a6b52; }
.btn-delete { background: rgba(233,201,188,0.2); border: none; color: #c4887a; border-radius: 6px; }
.btn-delete:hover { background: #e9c9bc; color: #8a5a48; }

.pagination-wrap { display: flex; justify-content: center; margin-top: 18px; }
.pagination-wrap :deep(.el-pager li.is-active) { background-color: #b7d9c8 !important; color: #fff !important; border-radius: 6px; }
.pagination-wrap :deep(.el-pager li) { border-radius: 6px; min-width: 32px; }
</style>
