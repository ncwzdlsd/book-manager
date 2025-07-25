<template>
  <div class="notice-page">
    <div class="page-header">
      <h2>通知管理</h2>
      <el-button type="primary" @click="showAddDialog">通知送信</el-button>
    </div>

    <!-- 検索とフィルター -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="内容">
          <el-input v-model="searchForm.content" placeholder="通知内容を入力" clearable />
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
        
        <el-table-column prop="staff_name" label="送信者" width="120" />
        
        <el-table-column prop="reader_name" label="受信者" width="120" />
        
        <el-table-column prop="content" label="通知内容" show-overflow-tooltip />
        
        <el-table-column prop="send_date" label="送信時間" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.send_date) }}
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

    <!-- 新規通知ダイアログ -->
    <el-dialog
      v-model="addDialogVisible"
      title="通知送信"
      width="600px"
      @close="resetForm">
      
      <el-form
        ref="noticeForm"
        :model="noticeForm"
        :rules="noticeRules"
        label-width="100px">
        
        <el-form-item label="受信者" prop="reader_id">
          <el-select v-model="noticeForm.reader_id" placeholder="受信者を選択" style="width: 100%">
            <el-option
              v-for="reader in readers"
              :key="reader.id"
              :label="reader.name"
              :value="reader.id">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="通知内容" prop="content">
          <el-input
            v-model="noticeForm.content"
            type="textarea"
            :rows="6"
            placeholder="通知内容を入力">
          </el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">キャンセル</el-button>
          <el-button type="primary" @click="handleSubmit">送信</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 詳細表示ダイアログ -->
    <el-dialog
      v-model="detailDialogVisible"
      title="通知詳細"
      width="600px">
      
      <div class="notice-detail">
        <div class="detail-item">
          <label>送信者：</label>
          <span>{{ currentNotice.staff_name }}</span>
        </div>
        <div class="detail-item">
          <label>受信者：</label>
          <span>{{ currentNotice.reader_name }}</span>
        </div>
        <div class="detail-item">
          <label>送信時間：</label>
          <span>{{ formatDateTime(currentNotice.send_date) }}</span>
        </div>
        <div class="detail-item">
          <label>通知内容：</label>
          <div class="content-box">{{ currentNotice.content }}</div>
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
  name: 'Notice',
  data() {
    return {
      notices: [],
      readers: [],
      loading: false,
      searchForm: {
        content: '',
        send_date: ''
      },
      currentPage: 1,
      pageSize: 10,
      total: 0,
      addDialogVisible: false,
      detailDialogVisible: false,
      currentNotice: {},
      noticeForm: {
        reader_id: '',
        content: '',
        staff_id: ''
      },
      noticeRules: {
        reader_id: [
          { required: true, message: '受信者を選択してください', trigger: 'change' }
        ],
        content: [
          { required: true, message: '通知内容を入力してください', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.loadNotices()
    this.loadReaders()
  },
  methods: {
    async loadNotices() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          ...this.searchForm
        }
        
        const response = await axios.get('http://localhost:8000/notices', { params })
        
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

    async loadReaders() {
      try {
        const response = await axios.get('http://localhost:8000/readers')
        if (response.data.success) {
          this.readers = response.data.data
        }
      } catch (error) {
        console.error('Load readers error:', error)
      }
    },

    showAddDialog() {      
      this.addDialogVisible = true
      this.resetForm()
    },

    showDetailDialog(row) {
      this.currentNotice = { ...row }
      this.detailDialogVisible = true
    },

    async handleSubmit() {
      try {
        const valid = await this.$refs.noticeForm.validate()
        if (!valid) return

        const response = await axios.post('http://localhost:8000/notices', this.noticeForm)
        
        if (response.data.success) {
          ElMessage.success('通知送信に成功しました')
          this.addDialogVisible = false
          this.loadNotices()
        } else {
          ElMessage.error(response.data.message || '送信に失敗しました')
        }
      } catch (error) {
        console.error('Submit notice error:', error)
        ElMessage.error('送信に失敗しました')
      }
    },

    async handleDelete(row) {
      try {
        await ElMessageBox.confirm(
          `通知 ${row.id} を削除しますか？この操作は元に戻せません。`,
          '削除確認',
          {
            confirmButtonText: '確定',
            cancelButtonText: 'キャンセル',
            type: 'warning'
          }
        )

        const response = await axios.delete(`http://localhost:8000/notices/${row.id}`)
        
        if (response.data.success) {
          ElMessage.success('削除に成功しました')
          this.loadNotices()
        } else {
          ElMessage.error(response.data.message || '削除に失敗しました')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Delete notice error:', error)
          ElMessage.error('削除に失敗しました')
        }
      }
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

    resetForm() {
      const userInfoStr = localStorage.getItem('userInfo')
      let staff_id = ''
      if (userInfoStr) {
        try {
          const userInfo = JSON.parse(userInfoStr)
          // 判断角色，确保是staff
          if (userInfo.role === 'staff') {
            staff_id = userInfo.id
          }
        } catch (e) {
          // 解析失败，staff_id 保持为空
        }
      }

      this.noticeForm = {
        reader_id: '',
        content: '',
        staff_id: staff_id
      }
      if (this.$refs.noticeForm) {
        this.$refs.noticeForm.resetFields()
      }
    },

    formatDateTime(dateTime) {
      if (!dateTime) return '-'
      return new Date(dateTime).toLocaleString()
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.notice-detail {
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