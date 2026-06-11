<template>
  <div class="page-container">
    <!-- 标题栏 -->
    <div class="search-card">
      <div class="search-left">
        <span class="card-title-sm">我的申请记录</span>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <el-table :data="list" style="width: 100%">
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
        <el-table-column prop="remark" label="审核备注" min-width="120" />
        <el-table-column prop="created_at" label="申请时间" width="160" />
      </el-table>

      <div v-if="!list.length" class="empty-tip">暂无申请记录</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api'

const list = ref([])

onMounted(async () => {
  const data = await request.get('/students/info-changes/')
  list.value = data.results
})
</script>

<style scoped>
.page-container { display: flex; flex-direction: column; gap: 16px; }

.search-card {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 22px; background: #fff; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.card-title-sm { font-size: 14px; font-weight: 600; color: #3a4f63; }

.table-card { background: #fff; border-radius: 14px; padding: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.045); }
.table-card :deep(.el-table) { border-radius: 10px; overflow: hidden; }
.table-card :deep(.el-table th.el-table__cell) { background: rgba(99,136,160,0.08) !important; color: #3a4f63; font-weight: 600; font-size: 13px; }
.table-card :deep(.el-table td.el-table__cell) { font-size: 13px; color: #555; border-bottom: 1px solid #f5f5f5; }
.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) { background: rgba(183,217,200,0.08) !important; }
.table-card :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) { background: #fafbfc; }

.field-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; background: rgba(99,136,160,0.08); color: #6388a0; }

.status-tag { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.status-tag.pending { background: rgba(233,201,188,0.2); color: #c4887a; }
.status-tag.approved { background: rgba(183,217,200,0.2); color: #5a9a78; }
.status-tag.rejected { background: rgba(200,120,120,0.12); color: #b06060; }

.empty-tip { text-align: center; color: #ccc; font-size: 13px; padding: 40px 0; }
</style>
