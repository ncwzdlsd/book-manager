<template>
  <div class="book-page">
    <div class="page-header">
      <h2>図書ホール</h2>
      <el-button type="primary" @click="refreshData">更新</el-button>
    </div>

    <!-- 検索とフィルター -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="図書名">
          <el-input
            v-model="searchForm.title"
            placeholder="図書名を入力"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="著者">
          <el-input
            v-model="searchForm.author"
            placeholder="著者を入力"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="出版社">
          <el-input
            v-model="searchForm.publisher"
            placeholder="出版社を入力"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">検索</el-button>
          <el-button @click="resetSearch">リセット</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 図書リスト -->
    <el-card class="table-card">
      <el-table
        :data="books"
        v-loading="loading"
        style="width: 100%">
        
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="title" label="図書名" />
        
        <el-table-column prop="author" label="著者" width="120" />
        
        <el-table-column prop="publisher" label="出版社" width="150" />
        
        <el-table-column prop="isbn" label="ISBN" width="120" />
        
        <el-table-column prop="stock" label="在庫" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.stock > 0 ? 'success' : 'danger'">
              {{ scope.row.stock }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="私の状態" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.my_status === '貸出中'" type="warning">
              貸出中
            </el-tag>
            <el-tag v-else-if="scope.row.my_status === '予約済み'" type="info">
              予約済み
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <!-- 貸出済み状態 -->
            <template v-if="scope.row.my_status === '貸出中'">
              <el-button
                size="small"
                type="success"
                @click="handleReturn(scope.row)">
                返却
              </el-button>
            </template>
            
            <!-- 予約済み状態 -->
            <template v-else-if="scope.row.my_status === '予約済み'">
              <el-button
                size="small"
                type="danger"
                @click="handleCancelReservation(scope.row)">
                予約キャンセル
              </el-button>
            </template>
            
            <!-- 状態なし且つ在庫あり -->
            <template v-else-if="scope.row.stock > 0">
              <el-button
                size="small"
                type="primary"
                @click="handleReservation(scope.row)">
                予約
              </el-button>
              <el-button
                size="small"
                type="success"
                @click="handleBorrow(scope.row)">
                貸出
              </el-button>
            </template>
            
            <!-- 在庫なし -->
            <template v-else>
              <el-tag type="danger" size="small">在庫なし</el-tag>
            </template>
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

    <!-- 予約ダイアログ -->
    <el-dialog
      v-model="reservationDialogVisible"
      title="図書予約"
      width="500px">
      <el-form :model="reservationForm" label-width="80px">
        <el-form-item label="図書名">
          <el-input v-model="reservationForm.book_title" disabled />
        </el-form-item>
        <el-form-item label="予約日">
          <el-date-picker
            v-model="reservationForm.date"
            type="date"
            placeholder="予約日を選択"
            :disabled-date="disabledDate">
          </el-date-picker>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="reservationDialogVisible = false">キャンセル</el-button>
          <el-button type="primary" @click="confirmReservation">予約確認</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 貸出ダイアログ -->
    <el-dialog
      v-model="borrowDialogVisible"
      title="図書貸出"
      width="500px">
      <el-form :model="borrowForm" label-width="80px">
        <el-form-item label="図書名">
          <el-input v-model="borrowForm.book_title" disabled />
        </el-form-item>
        <el-form-item label="貸出日数">
          <el-input-number
            v-model="borrowForm.days"
            :min="1"
            :max="30"
            placeholder="貸出日数を選択">
          </el-input-number>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="borrowDialogVisible = false">キャンセル</el-button>
          <el-button type="primary" @click="confirmBorrow">貸出確認</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ReaderBook',
  data() {
    return {
      books: [],
      loading: false,
      searchForm: {
        title: '',
        author: '',
        publisher: ''
      },
      currentPage: 1,
      pageSize: 10,
      total: 0,
      
      // 预约对话框
      reservationDialogVisible: false,
      reservationForm: {
        book_id: null,
        book_title: '',
        date: new Date()
      },
      
      // 借阅对话框
      borrowDialogVisible: false,
      borrowForm: {
        book_id: null,
        book_title: '',
        days: 14
      }
    }
  },
  mounted() {
    this.loadBooks()
  },
  methods: {
    async loadBooks() {
      this.loading = true
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          reader_id: userInfo.id,
          ...this.searchForm
        }
        
        const response = await axios.get('http://localhost:8000/reader/books', { params })
        
        if (response.data.success) {
          this.books = response.data.data
          this.total = response.data.total
        } else {
          ElMessage.error(response.data.message || '図書リストの取得に失敗しました')
        }
      } catch (error) {
        console.error('Load books error:', error)
        ElMessage.error('図書リストの取得に失敗しました')
      } finally {
        this.loading = false
      }
    },

    handleReservation(row) {
      this.reservationForm = {
        book_id: row.id,
        book_title: row.title,
        date: new Date()
      }
      this.reservationDialogVisible = true
    },

    async confirmReservation() {
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        const response = await axios.post('http://localhost:8000/reader/reservations', {
          reader_id: userInfo.id,
          book_id: this.reservationForm.book_id,
          date: this.formatDateForAPI(this.reservationForm.date)
        })
        
        if (response.data.success) {
          ElMessage.success('予約に成功しました')
          this.reservationDialogVisible = false
          this.loadBooks()
        } else {
          ElMessage.error(response.data.message || '予約に失敗しました')
        }
      } catch (error) {
        console.error('Reservation error:', error)
        ElMessage.error('予約に失敗しました')
      }
    },

    handleBorrow(row) {
      this.borrowForm = {
        book_id: row.id,
        book_title: row.title,
        days: 14
      }
      this.borrowDialogVisible = true
    },

    async confirmBorrow() {
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        const response = await axios.post('http://localhost:8000/reader/borrows', {
          reader_id: userInfo.id,
          book_id: this.borrowForm.book_id,
          days: this.borrowForm.days
        })
        
        if (response.data.success) {
          ElMessage.success('貸出に成功しました')
          this.borrowDialogVisible = false
          this.loadBooks()
        } else {
          ElMessage.error(response.data.message || '貸出に失敗しました')
        }
      } catch (error) {
        console.error('Borrow error:', error)
        ElMessage.error('貸出に失敗しました')
      }
    },

    async handleCancelReservation(row) {
      try {
        await ElMessageBox.confirm(
          `《${row.title}》の予約をキャンセルしますか？`,
          'キャンセル確認',
          {
            confirmButtonText: '確定',
            cancelButtonText: 'キャンセル',
            type: 'warning'
          }
        )

        const response = await axios.delete(`http://localhost:8000/reader/reservations/${row.reservation_id}`)
        
        if (response.data.success) {
          ElMessage.success('予約キャンセルに成功しました')
          this.loadBooks()
        } else {
          ElMessage.error(response.data.message || 'キャンセルに失敗しました')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Cancel reservation error:', error)
          ElMessage.error('キャンセルに失敗しました')
        }
      }
    },

    async handleReturn(row) {
      try {
        await ElMessageBox.confirm(
          `《${row.title}》を返却しますか？`,
          '返却確認',
          {
            confirmButtonText: '確定',
            cancelButtonText: 'キャンセル',
            type: 'warning'
          }
        )

        const response = await axios.put(`http://localhost:8000/reader/borrows/${row.borrow_id}/return`)
        
        if (response.data.success) {
          ElMessage.success('返却に成功しました')
          this.loadBooks()
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
      this.loadBooks()
    },

    resetSearch() {
      this.searchForm = {
        title: '',
        author: '',
        publisher: ''
      }
      this.currentPage = 1
      this.loadBooks()
    },

    handleSizeChange(val) {
      this.pageSize = val
      this.loadBooks()
    },

    handleCurrentChange(val) {
      this.currentPage = val
      this.loadBooks()
    },

    refreshData() {
      this.loadBooks()
    },

    disabledDate(time) {
      return time.getTime() < Date.now() - 8.64e7 // 今日より前の日付は選択不可
    },

    formatDateForAPI(date) {
      if (!date) return ''
      return date.toISOString().split('T')[0]
    }
  }
}
</script>

<style scoped>
.book-page {
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
</style> 