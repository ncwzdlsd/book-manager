import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import StaffHome from '../views/staff/Home.vue'
import Reservation from '../views/staff/Reservation.vue'
import ReaderHome from '../views/reader/Home.vue'
import ReaderReservation from '../views/reader/Reservation.vue'

const routes = [
  {
    path: '/',
    name: 'Root',
    redirect: '/login'  // 将根路径重定向到登录页
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/staff',
    name: 'StaffHome',
    component: StaffHome,
    meta: { requiresAuth: true, role: 'staff' },
    redirect: '/staff/reservation',  // 职员根路径重定向到预约管理
    children: [
      {
        path: 'reservation',
        name: 'StaffReservation',
        component: Reservation
      },
      {
        path: 'borrow',
        name: 'StaffBorrow',
        component: () => import('../views/staff/Borrow.vue')
      },
      {
        path: 'book',
        name: 'StaffBook',
        component: () => import('../views/staff/Book.vue')
      },
      {
        path: 'notice',
        name: 'StaffNotice',
        component: () => import('../views/staff/Notice.vue')
      },
      {
        path: 'suggestion',
        name: 'StaffSuggestion',
        component: () => import('../views/staff/Suggestion.vue')
      }
    ]
  },
  {
    path: '/reader',
    name: 'ReaderHome',
    component: ReaderHome,
    meta: { requiresAuth: true, role: 'reader' },
    redirect: '/reader/reservation',  // 读者根路径重定向到我的预约
    children: [
      {
        path: 'reservation',
        name: 'ReaderReservation',
        component: ReaderReservation
      },
      {
        path: 'borrow',
        name: 'ReaderBorrow',
        component: () => import('../views/reader/Borrow.vue')
      },
      {
        path: 'book',
        name: 'ReaderBook',
        component: () => import('../views/reader/Book.vue')
      },
      {
        path: 'notice',
        name: 'ReaderNotice',
        component: () => import('../views/reader/Notice.vue')
      },
      {
        path: 'suggestion',
        name: 'ReaderSuggestion',
        component: () => import('../views/reader/Suggestion.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL || '/'),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userInfo = localStorage.getItem('userInfo')
  
  if (to.meta.requiresAuth) {
    if (!userInfo) {
      next('/login')
    } else {
      const user = JSON.parse(userInfo)
      if (to.meta.role && to.meta.role !== user.role) {
        next('/login')
      } else {
        next()
      }
    }
  } else {
    next()
  }
})

export default router 