<template>
  <div class="suggestion-page">
    <div class="page-header">
      <h2>提案管理</h2>
      <el-button type="primary" @click="refreshData">更新</el-button>
    </div>

    <!-- 検索とフィルター -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="内容">
          <el-input v-model="searchForm.content" placeholder="提案内容を入力" clearable />
        </el-form-item>
        <el-form-item label="提案日">
          <el-date-picker
            v-model="searchForm.comment_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="提案日を選択"
            clearable>
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">検索</el-button>
          <el-button @click="resetSearch">リセット</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 提案リスト -->
    <el-card class="table-card">
      <el-table
        :data="suggestions"
        v-loading="loading"
        style="width: 100%">
        
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="reader_name" label="提案者" width="120" />
        
        <el-table-column prop="content" label="提案内容" show-overflow-tooltip />
        
        <el-table-column prop="comment_date" label="提案日" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.comment_date) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="info"
              @click="showDetailDialog(scope.row)">
              詳細
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.row)">
              削除
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

    <!-- 詳細表示ダイアログ -->
    <el-dialog
      v-model="detailDialogVisible"
      title="提案詳細"
      width="600px">
      
      <div class="suggestion-detail">
        <div class="detail-item">
          <label>提案者：</label>
          <span>{{ currentSuggestion.reader_name }}</span>
        </div>
        <div class="detail-item">
          <label>提案日：</label>
          <span>{{ formatDate(currentSuggestion.comment_date) }}</span>
        </div>
        <div class="detail-item">
          <label>提案内容：</label>
          <div class="content-box">{{ currentSuggestion.content }}</div>
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
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'Suggestion',
  data() {
    return {
      suggestions: [],
      loading: false,
      searchForm: {
        content: '',
        comment_date: ''
      },
      currentPage: 1,
      pageSize: 10,
      total: 0,
      detailDialogVisible: false,
      currentSuggestion: {}
    }
  },
  mounted() {
    this.loadSuggestions()
  },
  methods: {
    async loadSuggestions() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          ...this.searchForm
        }
        
        const response = await axios.get('http://localhost:8000/suggestions', { params })
        
        if (response.data.success) {
          this.suggestions = response.data.data
          this.total = response.data.total
        } else {
          ElMessage.error(response.data.message || '提案リストの取得に失敗しました')
        }
      } catch (error) {
        console.error('Load suggestions error:', error)
        ElMessage.error('提案リストの取得に失敗しました')
      } finally {
        this.loading = false
      }
    },

    showDetailDialog(row) {
      this.currentSuggestion = { ...row }
      this.detailDialogVisible = true
    },

    async handleDelete(row) {
      try {
        await ElMessageBox.confirm(
          `提案 ${row.id} を削除しますか？この操作は元に戻せません。`,
          '削除確認',
          {
            confirmButtonText: '確定',
            cancelButtonText: 'キャンセル',
            type: 'warning'
          }
        )

        const response = await axios.delete(`http://localhost:8000/suggestions/${row.id}`)
        
        if (response.data.success) {
          ElMessage.success('削除に成功しました')
          this.loadSuggestions()
        } else {
          ElMessage.error(response.data.message || '削除に失敗しました')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Delete suggestion error:', error)
          ElMessage.error('削除に失敗しました')
        }
      }
    },

    handleSearch() {
      this.currentPage = 1
      this.loadSuggestions()
    },

    resetSearch() {
      this.searchForm = {
        content: '',
        comment_date: ''
      }
      this.currentPage = 1
      this.loadSuggestions()
    },

    handleSizeChange(val) {
      this.pageSize = val
      this.loadSuggestions()
    },

    handleCurrentChange(val) {
      this.currentPage = val
      this.loadSuggestions()
    },

    refreshData() {
      this.loadSuggestions()
    },

    formatDate(date) {
      if (!date) return '-'
      return new Date(date).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.suggestion-page {
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.suggestion-detail {
  padding: 20px;
}

.detail-item {
  margin-bottom: 15px;
  display: flex;
  align-items: flex-start;
}

.detail-item label {
  font-weight: bold;
  width: 100px;
  flex-shrink: 0;
}

.content-box {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  margin-top: 10px;
  white-space: pre-wrap;
  line-height: 1.6;
}
</style> 