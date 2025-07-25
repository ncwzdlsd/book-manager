<template>
  <div class="notice-page">
    <div class="page-header">
      <h2>私の通知</h2>
      <el-button type="primary" @click="refreshData">更新</el-button>
    </div>

    <!-- 検索とフィルター -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="通知内容">
          <el-input
            v-model="searchForm.content"
            placeholder="通知内容のキーワードを入力"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="送信日">
          <el-date-picker
            v-model="searchForm.send_date"
            type="date"
            value-format="YYYY-MM-DD"     
            placeholder="送信日を選択"
            clearable>
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">検索</el-button>
          <el-button @click="resetSearch">リセット</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 通知リスト -->
    <el-card class="table-card">
      <el-table
        :data="notices"
        v-loading="loading"
        style="width: 100%">
        
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="content" label="通知内容" show-overflow-tooltip>
          <template #default="scope">
            <span class="notice-content">{{ scope.row.content }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="staff_name" label="送信者" width="120" />
        
        <el-table-column prop="send_date" label="送信日" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.send_date) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleViewDetail(scope.row)">
              詳細表示
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

    <!-- 通知詳細ダイアログ -->
    <el-dialog
      v-model="detailDialogVisible"
      title="通知詳細"
      width="600px">
      <div class="notice-detail">
        <div class="detail-item">
          <label>通知ID：</label>
          <span>{{ currentNotice.id }}</span>
        </div>
        <div class="detail-item">
          <label>送信者：</label>
          <span>{{ currentNotice.staff_name || 'システム' }}</span>
        </div>
        <div class="detail-item">
          <label>送信日：</label>
          <span>{{ formatDate(currentNotice.send_date) }}</span>
        </div>
        <div class="detail-item">
          <label>通知内容：</label>
          <div class="content-box">
            {{ currentNotice.content }}
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">閉じる</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'ReaderNotice',
  data() {
    return {
      notices: [],
      loading: false,
      searchForm: {
        content: '',
        send_date: ''
      },
      currentPage: 1,
      pageSize: 10,
      total: 0,
      
      // 详情对话框
      detailDialogVisible: false,
      currentNotice: {}
    }
  },
  mounted() {
    this.loadNotices()
  },
  methods: {
    async loadNotices() {
      this.loading = true
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          reader_id: userInfo.id,
          ...this.searchForm
        }
        
        const response = await axios.get('http://localhost:8000/reader/notices', { params })
        
        if (response.data.success) {
          this.notices = response.data.data
          this.total = response.data.total
        } else {
          ElMessage.error(response.data.message || '通知リストの取得に失敗しました')
        }
      } catch (error) {
        console.error('Load notices error:', error)
        ElMessage.error('通知リストの取得に失敗しました')
      } finally {
        this.loading = false
      }
    },

    handleViewDetail(row) {
      this.currentNotice = { ...row }
      this.detailDialogVisible = true
    },

    handleSearch() {
      this.currentPage = 1
      this.loadNotices()
    },

    resetSearch() {
      this.searchForm = {
        content: '',
        send_date: ''
      }
      this.currentPage = 1
      this.loadNotices()
    },

    handleSizeChange(val) {
      this.pageSize = val
      this.loadNotices()
    },

    handleCurrentChange(val) {
      this.currentPage = val
      this.loadNotices()
    },

    refreshData() {
      this.loadNotices()
    },

    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString() + ' ' + new Date(date).toLocaleTimeString()
    }
  }
}
</script>

<style scoped>
.notice-page {
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

.notice-content {
  max-width: 300px;
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-detail {
  padding: 20px 0;
}

.detail-item {
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
}

.detail-item label {
  font-weight: bold;
  min-width: 80px;
  color: #606266;
}

.detail-item span {
  color: #303133;
}

.content-box {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-top: 10px;
  line-height: 1.6;
  color: #303133;
  white-space: pre-wrap;
  word-break: break-word;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style> 