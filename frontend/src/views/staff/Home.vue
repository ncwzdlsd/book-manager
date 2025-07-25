<template>
  <div class="staff-home">
    <el-container>
      <!-- トップナビゲーションバー -->
      <el-header class="header">
        <div class="header-left">
          <h2>図書館管理システム - 職員端</h2>
        </div>
        <div class="header-right">
          <span class="user-info">
            ようこそ、{{ userInfo.name || userInfo.username }} ({{ userInfo.role === 'staff' ? '職員' : '読者' }})
          </span>
          <el-button type="danger" size="small" @click="handleLogout">ログアウト</el-button>
        </div>
      </el-header>

      <el-container>
        <!-- サイドメニュー -->
        <el-aside width="200px" class="sidebar">
          <el-menu
            :default-active="activeMenu"
            class="menu"
            @select="handleMenuSelect"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b">
            
            <el-menu-item index="reservation">
              <el-icon><Calendar /></el-icon>
              <span>予約管理</span>
            </el-menu-item>
            
            <el-menu-item index="borrow">
              <el-icon><Document /></el-icon>
              <span>貸出管理</span>
            </el-menu-item>
            
            <el-menu-item index="book">
              <el-icon><Reading /></el-icon>
              <span>図書管理</span>
            </el-menu-item>
            
            <el-menu-item index="notice">
              <el-icon><Bell /></el-icon>
              <span>通知管理</span>
            </el-menu-item>
            
            <el-menu-item index="suggestion">
              <el-icon><ChatDotRound /></el-icon>
              <span>提案管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <!-- メインコンテンツエリア -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { Calendar, Document, Reading, Bell, ChatDotRound } from '@element-plus/icons-vue'

export default {
  name: 'StaffHome',
  components: {
    Calendar,
    Document,
    Reading,
    Bell,
    ChatDotRound
  },
  data() {
    return {
      activeMenu: 'reservation'
    }
  },
  computed: {
    userInfo() {
      const userInfo = localStorage.getItem('userInfo')
      return userInfo ? JSON.parse(userInfo) : {}
    }
  },
  methods: {
    handleMenuSelect(key) {
      this.activeMenu = key
      this.$router.push(`/staff/${key}`)
    },
    handleLogout() {
      localStorage.removeItem('userInfo')
      localStorage.removeItem('token')
      this.$store.dispatch('logout')
      this.$router.push('/login')
    }
  },
  watch: {
    $route(to) {
      // 根据当前路由更新菜单激活状态
      const path = to.path
      if (path.includes('/staff/')) {
        const menuKey = path.split('/staff/')[1]
        this.activeMenu = menuKey
      }
    }
  },
  mounted() {
    // 根据当前路由设置菜单激活状态
    const path = this.$route.path
    if (path.includes('/staff/')) {
      const menuKey = path.split('/staff/')[1]
      this.activeMenu = menuKey
    }
  }
}
</script>

<style scoped>
.staff-home {
  height: 100vh;
}

.header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left h2 {
  margin: 0;
  color: white;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  color: white;
  font-size: 14px;
}

.sidebar {
  background-color: #545c64;
}

.menu {
  border-right: none;
}

.main-content {
  background-color: #f5f5f5;
  padding: 20px;
}

.el-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style> 