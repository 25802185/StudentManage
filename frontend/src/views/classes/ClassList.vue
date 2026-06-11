<template>
  <div class="page-container">
    <!-- 操作栏 -->
    <div class="search-card">
      <div class="search-left">
        <span class="card-title-sm">班级管理</span>
      </div>
      <div class="search-right">
        <el-button class="btn-mint" @click="showAdd">
          <el-icon><Plus /></el-icon>新增班级
        </el-button>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <el-table :data="list" style="width: 100%">
        <el-table-column prop="name" label="班级名称" min-width="180" />
        <el-table-column prop="grade" label="年级" width="100" />
        <el-table-column prop="major" label="专业" min-width="160" />
        <el-table-column prop="student_count" label="学生人数" width="100">
          <template #default="{ row }">
            <span class="count-badge">{{ row.student_count }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" class="btn-edit" @click="showEdit(row)">编辑</el-button>
            <el-button size="small" class="btn-delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination v-model:current-page="page" :total="total" :page-size="10" layout="prev, pager, next" background @current-change="loadData" />
      </div>
    </div>

    <!-- 弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑班级' : '新增班级'" width="460px" class="custom-dialog">
      <el-form :model="form" label-width="80px" class="dialog-form">
        <el-form-item label="班级名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="年级"><el-input v-model="form.grade" /></el-form-item>
        <el-form-item label="专业"><el-input v-model="form.major" /></el-form-item>
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
const total = ref(0)
const page = ref(1)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = reactive({ name: '', grade: '', major: '' })

const loadData = async () => {
  const data = await request.get('/classes/', { params: { page: page.value, page_size: 10 } })
  list.value = data.results
  total.value = data.count
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { name: '', grade: '', major: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, grade: row.grade, major: row.major })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/classes/${editId.value}/`, form)
  } else {
    await request.post('/classes/', form)
  }
  dialogVisible.value = false
  ElMessage.success(isEdit.value ? '修改成功' : '新增成功')
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该班级？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/classes/${row.id}/`)
    ElMessage.success('已删除')
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
.search-right { display: flex; gap: 10px; }

.btn-mint { background: linear-gradient(135deg, #b7d9c8, #c8e6d6); border: none; border-radius: 8px; color: #3a6b52; }
.btn-mint:hover { background: linear-gradient(135deg, #a8cebb, #b7d9c8); }

.table-card { background: #fff; border-radius: 14px; padding: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.045); }
.table-card :deep(.el-table) { border-radius: 10px; overflow: hidden; }
.table-card :deep(.el-table th.el-table__cell) { background: rgba(99,136,160,0.08) !important; color: #3a4f63; font-weight: 600; font-size: 13px; }
.table-card :deep(.el-table td.el-table__cell) { font-size: 13px; color: #555; border-bottom: 1px solid #f5f5f5; }
.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) { background: rgba(183,217,200,0.08) !important; }
.table-card :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) { background: #fafbfc; }

.count-badge { display: inline-block; min-width: 28px; height: 22px; line-height: 22px; text-align: center; background: rgba(99,136,160,0.1); color: #6388a0; border-radius: 10px; font-size: 12px; font-weight: 500; padding: 0 8px; }

.btn-edit { background: rgba(99,136,160,0.1); border: none; color: #6388a0; border-radius: 6px; }
.btn-edit:hover { background: #6388a0; color: #fff; }
.btn-delete { background: rgba(233,201,188,0.2); border: none; color: #c4887a; border-radius: 6px; }
.btn-delete:hover { background: #e9c9bc; color: #8a5a48; }

.pagination-wrap { display: flex; justify-content: center; margin-top: 18px; }
.pagination-wrap :deep(.el-pager li.is-active) { background-color: #b7d9c8 !important; color: #fff !important; border-radius: 6px; }
.pagination-wrap :deep(.el-pager li) { border-radius: 6px; min-width: 32px; }

.custom-dialog :deep(.el-dialog) { border-radius: 16px; overflow: hidden; }
.custom-dialog :deep(.el-dialog__header) { background: rgba(99,136,160,0.06); padding: 16px 24px; margin: 0; }
.custom-dialog :deep(.el-dialog__title) { font-size: 15px; font-weight: 600; color: #3a4f63; }
.custom-dialog :deep(.el-dialog__body) { padding: 24px; }
.dialog-form :deep(.el-input__wrapper) { border-radius: 8px; }
.btn-cancel { border-radius: 8px; }
.btn-submit { background: linear-gradient(135deg, #6388a0, #7a9ab4); border: none; border-radius: 8px; }
.btn-submit:hover { background: linear-gradient(135deg, #577a92, #6388a0); }
</style>
