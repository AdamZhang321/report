import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Result from '../views/Result.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/result',
      name: 'Result',
      component: Result
    }
  ]
})

export default router 