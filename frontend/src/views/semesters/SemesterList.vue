<template>
  <div class="page-container">
    <!-- 操作栏 -->
    <div class="search-card">
      <div class="search-left">
        <span class="card-title-sm">学期管理</span>
      </div>
      <div class="search-right">
        <el-button class="btn-mint" @click="showAdd">
          <el-icon><Plus /></el-icon>新增学期
        </el-button>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <el-table :data="list" style="width: 100%">
        <el-table-column prop="name" label="学期名称" min-width="200" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <span v-if="row.is_current" class="status-current">当前学期</span>
            <span v-else class="status-normal">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button size="small" class="btn-edit" @click="showEdit(row)">编辑</el-button>
            <el-button size="small" class="btn-mint-sm" @click="handleSetCurrent(row)" :disabled="row.is_current">
              {{ row.is_current ? '已是当前' : '设为当前' }}
            </el-button>
            <el-button size="small" class="btn-delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑学期' : '新增学期'" width="420px" class="custom-dialog">
      <el-form :model="form" label-width="80px" class="dialog-form">
        <el-form-item label="学期名称">
          <el-input v-model="form.name" placeholder="如 2025-2026-1" />
        </el-form-item>
        <el-form-item label="设为当前">
          <el-switch v-model="form.is_current" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" class="btn-cancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit" class="btn-submit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = reactive({ name: '', is_current: false })

const loadData = async () => {
  const data = await request.get('/courses/semesters/')
  list.value = data.results || data
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { name: '', is_current: false })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, is_current: row.is_current })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.name.trim()) {
    ElMessage.warning('请输入学期名称')
    return
  }
  if (isEdit.value) {
    await request.put(`/courses/semesters/${editId.value}/`, form)
  } else {
    await request.post('/courses/semesters/', form)
  }
  dialogVisible.value = false
  ElMessage.success(isEdit.value ? '修改成功' : '新增成功')
  loadData()
}

const handleSetCurrent = (row) => {
  ElMessageBox.confirm(`确认将 ${row.name} 设为当前学期？`, '提示', { type: 'warning' }).then(async () => {
    await request.put(`/courses/semesters/${row.id}/set-current/`)
    ElMessage.success('设置成功')
    loadData()
  })
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除学期 ${row.name}？有关联课程时无法删除。`, '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/courses/semesters/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

onMounted(() => { loadData() })
</script>

<style scoped>
.page-container { display: flex; flex-direction: column; gap: 16px; }

.search-card {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 22px; background: #fff; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.card-title-sm { font-size: 14px; font-weight: 600; color: #3a4f63; }
.search-right { display: flex; gap: 10px; }

.btn-mint { background: linear-gradient(135deg, #b7d9c8, #c8e6d6); border: none; border-radius: 8px; color: #3a6b52; }
.btn-mint:hover { background: linear-gradient(135deg, #a8cebb, #b7d9c8); }
.btn-mint-sm { background: rgba(183,217,200,0.2); border: none; color: #5a9a78; border-radius: 6px; }
.btn-mint-sm:hover { background: #b7d9c8; color: #3a6b52; }
.btn-mint-sm:disabled { opacity: 0.5; cursor: not-allowed; }

.table-card { background: #fff; border-radius: 14px; padding: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.045); }
.table-card :deep(.el-table) { border-radius: 10px; overflow: hidden; }
.table-card :deep(.el-table th.el-table__cell) { background: rgba(99,136,160,0.08) !important; color: #3a4f63; font-weight: 600; font-size: 13px; }
.table-card :deep(.el-table td.el-table__cell) { font-size: 13px; color: #555; border-bottom: 1px solid #f5f5f5; }
.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) { background: rgba(183,217,200,0.08) !important; }

.status-current { display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; background: rgba(183,217,200,0.2); color: #5a9a78; font-weight: 500; }
.status-normal { color: #ccc; }

.btn-edit { background: rgba(99,136,160,0.1); border: none; color: #6388a0; border-radius: 6px; }
.btn-edit:hover { background: #6388a0; color: #fff; }
.btn-delete { background: rgba(233,201,188,0.2); border: none; color: #c4887a; border-radius: 6px; }
.btn-delete:hover { background: #e9c9bc; color: #8a5a48; }

.custom-dialog :deep(.el-dialog) { border-radius: 16px; overflow: hidden; }
.custom-dialog :deep(.el-dialog__header) { background: rgba(99,136,160,0.06); padding: 16px 24px; margin: 0; }
.custom-dialog :deep(.el-dialog__title) { font-size: 15px; font-weight: 600; color: #3a4f63; }
.custom-dialog :deep(.el-dialog__body) { padding: 24px; }
.dialog-form :deep(.el-input__wrapper) { border-radius: 8px; }
.btn-cancel { border-radius: 8px; }
.btn-submit { background: linear-gradient(135deg, #6388a0, #7a9ab4); border: none; border-radius: 8px; }
.btn-submit:hover { background: linear-gradient(135deg, #577a92, #6388a0); }
</style>
