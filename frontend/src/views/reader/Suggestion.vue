<template>
  <div class="suggestion-page">
    <div class="page-header">
      <h2>私の提案</h2>
      <div class="header-actions">
        <el-button type="primary" @click="handleAdd">新規提案</el-button>
        <el-button type="primary" @click="refreshData">更新</el-button>
      </div>
    </div>

    <!-- 検索とフィルター -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="提案内容">
          <el-input
            v-model="searchForm.content"
            placeholder="提案内容のキーワードを入力"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="提出日">
          <el-date-picker
            v-model="searchForm.comment_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="提出日を選択"
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
        
        <el-table-column prop="content" label="提案内容" show-overflow-tooltip>
          <template #default="scope">
            <span class="suggestion-content">{{ scope.row.content }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="comment_date" label="提出日" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.comment_date) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleViewDetail(scope.row)">
              詳細表示
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

    <!-- 新規/編集提案ダイアログ -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px">
      <el-form :model="suggestionForm" :rules="suggestionRules" ref="suggestionFormRef" label-width="80px">
        <el-form-item label="提案内容" prop="content">
          <el-input
            v-model="suggestionForm.content"
            type="textarea"
            :rows="6"
            placeholder="提案内容を入力してください"
            maxlength="500"
            show-word-limit>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">キャンセル</el-button>
          <el-button type="primary" @click="confirmSubmit">提出確認</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 提案詳細ダイアログ -->
    <el-dialog
      v-model="detailDialogVisible"
      title="提案詳細"
      width="600px">
      <div class="suggestion-detail">
        <div class="detail-item">
          <label>提案ID：</label>
          <span>{{ currentSuggestion.id }}</span>
        </div>
        <div class="detail-item">
          <label>提出日：</label>
          <span>{{ formatDate(currentSuggestion.comment_date) }}</span>
        </div>
        <div class="detail-item">
          <label>提案内容：</label>
          <div class="content-box">
            {{ currentSuggestion.content }}
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
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ReaderSuggestion',
  data() {
    const userInfo = JSON.parse(localStorage.getItem('userInfo'))
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
      
      // 对话框
      dialogVisible: false,
      detailDialogVisible: false,
      dialogTitle: '新規提案',
      isEdit: false,
      
      // 表单
      suggestionForm: {
        id: null,
        content: '',
        reader_id: userInfo? userInfo.id : null
      },
      suggestionRules: {
        content: [
          { required: true, message: '提案内容を入力してください', trigger: 'blur' },
          { min: 10, message: '提案内容は最低10文字必要です', trigger: 'blur' },
          { max: 500, message: '提案内容は500文字以内で入力してください', trigger: 'blur' }
        ]
      },
      
      // 详情
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
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          reader_id: userInfo.id,
          ...this.searchForm
        }
        
        const response = await axios.get('http://localhost:8000/reader/suggestions', { params })
        
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

    handleAdd() {
      this.isEdit = false
      this.dialogTitle = '新規提案'
      this.suggestionForm = {
        id: null,
        content: ''
      }
      this.dialogVisible = true
    },

    handleViewDetail(row) {
      this.currentSuggestion = { ...row }
      this.detailDialogVisible = true
    },

    async handleDelete(row) {
      try {
        await ElMessageBox.confirm(
          `この提案を削除しますか？`,
          '削除確認',
          {
            confirmButtonText: '確定',
            cancelButtonText: 'キャンセル',
            type: 'warning'
          }
        )

        const response = await axios.delete(`http://localhost:8000/reader/suggestions/${row.id}`)
        
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

    async confirmSubmit() {
      try {
        await this.$refs.suggestionFormRef.validate()
        
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        const data = {
          reader_id: userInfo.id,
          content: this.suggestionForm.content
        }
        
        const response = await axios.post('http://localhost:8000/reader/suggestions', data)
        
        if (response.data.success) {
          ElMessage.success('提案提出に成功しました')
          this.dialogVisible = false
          this.loadSuggestions()
        } else {
          ElMessage.error(response.data.message || '提出に失敗しました')
        }
      } catch (error) {
        if (error !== false) { // 表单验证失败不显示错误
          console.error('Submit suggestion error:', error)
          ElMessage.error('提出に失敗しました')
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
      if (!date) return ''
      return new Date(date).toLocaleDateString() + ' ' + new Date(date).toLocaleTimeString()
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

.header-actions {
  display: flex;
  gap: 10px;
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

.suggestion-content {
  max-width: 300px;
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.suggestion-detail {
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
  gap: 10px;
}
</style> 