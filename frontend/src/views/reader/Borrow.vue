<template>
  <div class="borrow-page">
    <div class="page-header">
      <h2>私の貸出</h2>
      <el-button type="primary" @click="refreshData">更新</el-button>
    </div>

    <!-- 検索とフィルター -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="状態">
          <el-select v-model="searchForm.status" placeholder="状態を選択" clearable style="min-width: 120px;">
            <el-option label="貸出中" value="貸出中" />
            <el-option label="返却済み" value="返却済み" />
            <el-option label="延滞" value="延滞" />
          </el-select>
        </el-form-item>
        <el-form-item label="貸出日">
          <el-date-picker
            v-model="searchForm.lend_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="貸出日を選択"
            clearable>
          </el-date-picker>
        </el-form-item>
        <el-form-item label="返却予定日">
          <el-date-picker
            v-model="searchForm.due_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="返却予定日を選択"
            clearable>
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">検索</el-button>
          <el-button @click="resetSearch">リセット</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 貸出リスト -->
    <el-card class="table-card">
      <el-table
        :data="borrows"
        v-loading="loading"
        style="width: 100%">
        
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="book_title" label="図書名" />
        
        <el-table-column prop="lend_date" label="貸出日" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.lend_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="due_date" label="返却予定日" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.due_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="return_date" label="返却日" width="120">
          <template #default="scope">
            {{ scope.row.return_date ? formatDate(scope.row.return_date) : '-' }}
          </template>
        </el-table-column>
        
        <el-table-column label="状態" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row)">
              {{ getStatusText(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button
              v-if="!scope.row.return_date"
              size="small"
              type="success"
              @click="handleReturn(scope.row)">
              返却
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- ページネーション -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ReaderBorrow',
  data() {
    return {
      borrows: [],
      loading: false,
      searchForm: {
        status: '',
        lend_date: '',
        due_date: ''
      },
      currentPage: 1,
      pageSize: 10,
      total: 0
    }
  },
  mounted() {
    this.loadBorrows()
  },
  methods: {
    async loadBorrows() {
      this.loading = true
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          reader_id: userInfo.id,
          ...this.searchForm
        }
        
        const response = await axios.get('http://localhost:8000/reader/borrows', { params })
        
        if (response.data.success) {
          this.borrows = response.data.data
          this.total = response.data.total
        } else {
          ElMessage.error(response.data.message || '貸出リストの取得に失敗しました')
        }
      } catch (error) {
        console.error('Load borrows error:', error)
        ElMessage.error('貸出リストの取得に失敗しました')
      } finally {
        this.loading = false
      }
    },

    async handleReturn(row) {
      try {
        await ElMessageBox.confirm(
          `《${row.book_title}》を返却しますか？`,
          '返却確認',
          {
            confirmButtonText: '確定',
            cancelButtonText: 'キャンセル',
            type: 'warning'
          }
        )

        const response = await axios.put(`http://localhost:8000/reader/borrows/${row.id}/return`)
        
        if (response.data.success) {
          ElMessage.success('返却に成功しました')
          this.loadBorrows()
        } else {
          ElMessage.error(response.data.message || '返却に失敗しました')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Return book error:', error)
          ElMessage.error('返却に失敗しました')
        }
      }
    },

    handleSearch() {
      this.currentPage = 1
      this.loadBorrows()
    },

    resetSearch() {
      this.searchForm = {
        status: '',
        lend_date: '',
        due_date: ''
      }
      this.currentPage = 1
      this.loadBorrows()
    },

    handleSizeChange(val) {
      this.pageSize = val
      this.loadBorrows()
    },

    handleCurrentChange(val) {
      this.currentPage = val
      this.loadBorrows()
    },

    refreshData() {
      this.loadBorrows()
    },

    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },

    getStatusType(row) {
      if (row.return_date) {
        return 'success' // 返却済み
      } else {
        const dueDate = new Date(row.due_date)
        const today = new Date()
        if (dueDate < today) {
          return 'danger' // 延滞
        } else {
          return 'warning' // 貸出中
        }
      }
    },

    getStatusText(row) {
      if (row.return_date) {
        return '返却済み'
      } else {
        const dueDate = new Date(row.due_date)
        const today = new Date()
        if (dueDate < today) {
          return '延滞'
        } else {
          return '貸出中'
        }
      }
    }
  }
}
</script>

<style scoped>
.borrow-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  align-items: center;
  gap: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.el-table {
  margin-bottom: 20px;
}
</style> 