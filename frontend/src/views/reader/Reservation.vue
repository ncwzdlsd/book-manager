<template>
  <div class="reservation-page">
    <div class="page-header">
      <h2>私の予約</h2>
      <el-button type="primary" @click="refreshData">更新</el-button>
    </div>

    <!-- 検索とフィルター -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="状態">
          <el-select v-model="searchForm.status" placeholder="状態を選択" clearable style="min-width: 120px;">
            <el-option label="処理待ち" value="処理待ち" />
            <el-option label="処理済み" value="処理済み" />
            <el-option label="キャンセル済み" value="キャンセル済み" />
          </el-select>
        </el-form-item>
        <el-form-item label="日付">
          <el-date-picker
            v-model="searchForm.date"
            type="date"       
            value-format="YYYY-MM-DD"     
            placeholder="日付を選択"
            clearable>
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">検索</el-button>
          <el-button @click="resetSearch">リセット</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 予約リスト -->
    <el-card class="table-card">
      <el-table
        :data="reservations"
        v-loading="loading"
        style="width: 100%">
        
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="book_title" label="図書名" />
        
        <el-table-column prop="date" label="予約日" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状態" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button
              v-if="scope.row.status === '処理待ち'"
              size="small"
              type="danger"
              @click="handleDelete(scope.row)">
              予約キャンセル
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
  name: 'ReaderReservation',
  data() {
    return {
      reservations: [],
      loading: false,
      searchForm: {
        status: '',
        date: ''
      },
      currentPage: 1,
      pageSize: 10,
      total: 0
    }
  },
  mounted() {
    this.loadReservations()
  },
  methods: {
    async loadReservations() {
      this.loading = true
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo'))
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          reader_id: userInfo.id,
          ...this.searchForm
        }
        
        const response = await axios.get('http://localhost:8000/reader/reservations', { params })
        
        if (response.data.success) {
          this.reservations = response.data.data
          this.total = response.data.total
        } else {
          ElMessage.error(response.data.message || '予約リストの取得に失敗しました')
        }
      } catch (error) {
        console.error('Load reservations error:', error)
        ElMessage.error('予約リストの取得に失敗しました')
      } finally {
        this.loading = false
      }
    },

    async handleDelete(row) {
      try {
        await ElMessageBox.confirm(
          `《${row.book_title}》の予約をキャンセルしますか？`,
          'キャンセル確認',
          {
            confirmButtonText: '確定',
            cancelButtonText: 'キャンセル',
            type: 'warning'
          }
        )

        const response = await axios.delete(`http://localhost:8000/reader/reservations/${row.id}`)
        
        if (response.data.success) {
          ElMessage.success('予約キャンセルに成功しました')
          this.loadReservations()
        } else {
          ElMessage.error(response.data.message || 'キャンセルに失敗しました')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Delete reservation error:', error)
          ElMessage.error('キャンセルに失敗しました')
        }
      }
    },

    handleSearch() {
      this.currentPage = 1
      this.loadReservations()
    },

    resetSearch() {
      this.searchForm = {
        status: '',
        date: ''
      }
      this.currentPage = 1
      this.loadReservations()
    },

    handleSizeChange(val) {
      this.pageSize = val
      this.loadReservations()
    },

    handleCurrentChange(val) {
      this.currentPage = val
      this.loadReservations()
    },

    refreshData() {
      this.loadReservations()
    },

    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },

    getStatusType(status) {
      const statusMap = {
        '処理待ち': 'warning',
        '処理済み': 'success',
        'キャンセル済み': 'info'
      }
      return statusMap[status] || 'info'
    }
  }
}
</script>

<style scoped>
.reservation-page {
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