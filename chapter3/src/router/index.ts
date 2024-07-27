import { createRouter, createWebHistory } from 'vue-router'

// 导入你的组件
import Home from '../components/Home.vue'
// ...
import Results from '../components/Results.vue'

const routes = [
  {
    path: './Home.vue',
    name: 'Home',
    component: Home
  },
  // ...其他路由配置
  {
    path: './Results.vue',
    name: 'About',
    component: Results
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
