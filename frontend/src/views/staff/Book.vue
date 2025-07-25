<template>
  <div class="book-page">
    <div class="page-header">
      <h2>図書管理</h2>
      <el-button type="primary" @click="showAddDialog">新規図書</el-button>
    </div>

    <!-- 検索とフィルター -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="図書名">
          <el-input v-model="searchForm.title" placeholder="図書名を入力" clearable />
        </el-form-item>
        <el-form-item label="著者">
          <el-input v-model="searchForm.author" placeholder="著者を入力" clearable />
        </el-form-item>
        <el-form-item label="出版社">
          <el-input v-model="searchForm.publisher" placeholder="出版社を入力" clearable />
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
        
        <el-table-column prop="isbn" label="ISBN" width="150" />
        
        <el-table-column prop="stock" label="在庫" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.stock > 0 ? 'success' : 'danger'">
              {{ scope.row.stock }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="showEditDialog(scope.row)">
              編集
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

    <!-- 新規/編集ダイアログ -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="resetForm">
      
      <el-form
        ref="bookForm"
        :model="bookForm"
        :rules="bookRules"
        label-width="100px">
        
        <el-form-item label="図書名" prop="title">
          <el-input v-model="bookForm.title" placeholder="図書名を入力" />
        </el-form-item>
        
        <el-form-item label="著者" prop="author">
          <el-input v-model="bookForm.author" placeholder="著者を入力" />
        </el-form-item>
        
        <el-form-item label="出版社" prop="publisher">
          <el-input v-model="bookForm.publisher" placeholder="出版社を入力" />
        </el-form-item>
        
        <el-form-item label="ISBN" prop="isbn">
          <el-input v-model="bookForm.isbn" placeholder="ISBNを入力" />
        </el-form-item>
        
        <el-form-item label="在庫" prop="stock">
          <el-input-number 
            v-model="bookForm.stock" 
            :min="0" 
            placeholder="在庫数を入力" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">キャンセル</el-button>
          <el-button type="primary" @click="handleSubmit">確定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'Book',
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
      dialogVisible: false,
      dialogTitle: '新規図書',
      isEdit: false,
      bookForm: {
        title: '',
        author: '',
        publisher: '',
        isbn: '',
        stock: 0
      },
      bookRules: {
        title: [
          { required: true, message: '図書名を入力してください', trigger: 'blur' }
        ],
        author: [
          { required: true, message: '著者を入力してください', trigger: 'blur' }
        ],
        publisher: [
          { required: true, message: '出版社を入力してください', trigger: 'blur' }
        ],
        isbn: [
          { required: true, message: 'ISBNを入力してください', trigger: 'blur' }
        ],
        stock: [
          { required: true, message: '在庫数を入力してください', trigger: 'blur' }
        ]
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
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          ...this.searchForm
        }
        
        const response = await axios.get('http://localhost:8000/books', { params })
        
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

    showAddDialog() {
      this.isEdit = false
      this.dialogTitle = '新規図書'
      this.dialogVisible = true
      this.resetForm()
    },

    showEditDialog(row) {
      this.isEdit = true
      this.dialogTitle = '図書編集'
      this.dialogVisible = true
      this.bookForm = { ...row }
    },

    async handleSubmit() {
      try {
        const valid = await this.$refs.bookForm.validate()
        if (!valid) return

        let response
        if (this.isEdit) {
          response = await axios.put(`http://localhost:8000/books/${this.bookForm.id}`, this.bookForm)
        } else {
          response = await axios.post('http://localhost:8000/books', this.bookForm)
        }
        
        if (response.data.success) {
          ElMessage.success(this.isEdit ? '編集に成功しました' : '新規作成に成功しました')
          this.dialogVisible = false
          this.loadBooks()
        } else {
          ElMessage.error(response.data.message || '操作に失敗しました')
        }
      } catch (error) {
        console.error('Submit book error:', error)
        ElMessage.error('操作に失敗しました')
      }
    },

    async handleDelete(row) {
      try {
        await ElMessageBox.confirm(
          `図書《${row.title}》を削除しますか？この操作は元に戻せません。`,
          '削除確認',
          {
            confirmButtonText: '確定',
            cancelButtonText: 'キャンセル',
            type: 'warning'
          }
        )

        const response = await axios.delete(`http://localhost:8000/books/${row.id}`)
        
        if (response.data.success) {
          ElMessage.success('削除に成功しました')
          this.loadBooks()
        } else {
          ElMessage.error(response.data.message || '削除に失敗しました')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Delete book error:', error)
          ElMessage.error('削除に失敗しました')
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

    resetForm() {
      this.bookForm = {
        title: '',
        author: '',
        publisher: '',
        isbn: '',
        stock: 0
      }
      if (this.$refs.bookForm) {
        this.$refs.bookForm.resetFields()
      }
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