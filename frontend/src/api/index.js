import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        router.push('/login')
      } else if (error.response.status === 403) {
        ElMessage.error('无权限')
      } else {
        ElMessage.error(error.response.data?.detail || '请求失败')
      }
    }
    return Promise.reject(error)
  }
)

export default request
