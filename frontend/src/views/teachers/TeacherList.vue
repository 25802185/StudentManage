<template>
  <div>
    <el-form inline style="margin-bottom: 16px">
      <el-form-item label="姓名">
        <el-input v-model="query.name" placeholder="搜索姓名" clearable @clear="loadData" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadData">搜索</el-button>
        <el-button type="success" @click="showAdd">新增教师</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="list" border stripe>
      <el-table-column prop="teacher_no" label="工号" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别">
        <template #default="{ row }">{{ row.gender === 'male' ? '男' : '女' }}</template>
      </el-table-column>
      <el-table-column prop="title" label="职称" />
      <el-table-column prop="class_name" label="所带班级" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button size="small" :type="row.is_active ? 'warning' : 'success'" @click="handleToggle(row)">
            {{ row.is_active ? '禁用' : '启用' }}
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination style="margin-top: 16px; justify-content: center" v-model:current-page="page" :total="total" layout="prev, pager, next" @current-change="loadData" />

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑教师' : '新增教师'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="工号"><el-input v-model="form.teacher_no" :disabled="isEdit" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="职称"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="班级">
          <el-select v-model="form.class_ref_id" placeholder="选择班级" clearable>
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
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
const query = reactive({ name: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const classList = ref([])
const form = reactive({ teacher_no: '', name: '', gender: 'male', title: '', class_ref_id: null, phone: '', email: '' })

const loadData = async () => {
  const data = await request.get('/teachers/', { params: { page: page.value, ...query } })
  list.value = data.results
  total.value = data.count
}

const loadClasses = async () => {
  const data = await request.get('/classes/', { params: { page_size: 100 } })
  classList.value = data.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { teacher_no: '', name: '', gender: 'male', title: '', class_ref_id: null, phone: '', email: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, gender: row.gender, title: row.title, class_ref_id: row.class_ref, phone: row.phone, email: row.email })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/teachers/${editId.value}/`, form)
  } else {
    await request.post('/teachers/', form)
  }
  dialogVisible.value = false
  ElMessage.success(isEdit.value ? '修改成功' : '新增成功')
  loadData()
}

const handleToggle = async (row) => {
  await request.put(`/teachers/${row.id}/toggle/`)
  ElMessage.success('操作成功')
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/teachers/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

onMounted(() => { loadData(); loadClasses() })
</script>
