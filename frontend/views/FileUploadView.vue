<template>
  <div class="file-upload-view">
    <div class="view-header">
      <h3>文件管理</h3>
      <el-button type="primary" size="small" @click="showUploadDialog = true">
        <i class="el-icon-upload"></i> 上传文件
      </el-button>
    </div>
    
    <!-- 上传文件对话框 -->
    <el-dialog
      title="上传接口文档"
      :visible.sync="showUploadDialog"
      width="500px"
      @close="resetUploadForm"
    >
      <el-upload
        class="upload-demo"
        drag
        action="/api/files/upload"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
        multiple
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">
          支持上传任意格式的文件，单文件大小不超过10MB
        </div>
      </el-upload>
    </el-dialog>
    
    <!-- 文件列表 -->
    <div class="file-list">
      <el-empty description="暂无上传的文件" v-if="files.length === 0"></el-empty>
      <el-card v-for="file in files" :key="file.id" class="file-card" @dblclick="selectFile(file)">
        <div class="file-info">
          <div class="file-name">{{ file.filename }}</div>
          <div class="file-meta">
            <span class="file-type">{{ file.file_type }}</span>
            <span class="file-size">{{ formatFileSize(file.size) }}</span>
            <span class="file-time">{{ formatDateTime(file.uploaded_at) }}</span>
          </div>
          <!-- 解析结果显示 -->
          <div class="file-parse-result" v-if="file.parsed">
            <el-tag type="success" size="small" effect="light">已解析</el-tag>
            <span class="parse-count">
              <i class="el-icon-document"></i> 接口: {{ file.parsed_interfaces || 0 }}
            </span>
            <span class="parse-count">
              <i class="el-icon-s-promotion"></i> 参数: {{ file.parsed_params || 0 }}
            </span>
            <span class="parse-count">
              <i class="el-icon-reading"></i> 响应: {{ file.parsed_responses || 0 }}
            </span>
          </div>
          <div class="file-parse-result" v-else>
            <el-tag type="info" size="small" effect="light">未解析</el-tag>
          </div>
        </div>
        <div class="file-actions">
          <el-button size="mini" @click="selectFile(file)">
            <i class="el-icon-folder-opened"></i> 查看
          </el-button>
          <el-button size="mini" type="danger" @click="deleteFile(file)">
            <i class="el-icon-delete"></i> 删除
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUploadView',
  data() {
    return {
      showUploadDialog: false,
      files: []
    }
  },
  created() {
    // 初始化加载文件列表
    this.loadFiles()
  },
  methods: {
    // 加载文件列表
    async loadFiles() {
      try {
        // 添加详细的错误处理和调试信息
        console.log('开始加载文件列表...')
        // 移除/api前缀，因为axios.defaults.baseURL已经配置了/api
        const response = await this.$axios.get('/files', { cache: false })
        console.log('文件列表响应:', response)
        
        // 过滤掉无效的文件数据
        const validFiles = response.data.filter(file => {
          // 只保留具有有效ID和文件名的文件
          return file && file.id && file.filename
        })
        this.files = validFiles
        this.$store.commit('SET_FILES', validFiles)
        console.log('文件列表加载成功:', validFiles.length, '个文件')
      } catch (error) {
        console.error('加载文件列表失败:', error)
        console.error('错误详情:', error.response)
        this.$message.error('加载文件列表失败: ' + (error.message || '未知错误'))
        // 确保files数组为空，避免显示无效数据
        this.files = []
        this.$store.commit('SET_FILES', [])
      }
    },
    
    // 重置上传表单
    resetUploadForm() {
      // 重置上传表单逻辑
    },
    
    // 文件上传前的校验
    beforeUpload(file) {
      const fileSize = file.size / 1024 / 1024 // 转换为MB
      if (fileSize > 10) {
        this.$message.error('文件大小不能超过10MB')
        return false
      }
      return true
    },
    
    // 文件上传成功处理
    handleUploadSuccess() {
      this.$message.success('文件上传成功')
      this.loadFiles() // 重新加载文件列表
    },
    
    // 文件上传失败处理
    handleUploadError() {
      this.$message.error('文件上传失败')
    },
    
    // 格式化文件大小
    formatFileSize(size) {
      if (size == null || isNaN(size) || size < 0) {
        return '0 B'
      }
      if (size < 1024) {
        return size + ' B'
      } else if (size < 1024 * 1024) {
        return (size / 1024).toFixed(2) + ' KB'
      } else {
        return (size / (1024 * 1024)).toFixed(2) + ' MB'
      }
    },
    
    // 格式化日期时间
    formatDateTime(dateTime) {
      if (!dateTime) {
        return '未上传'
      }
      const date = new Date(dateTime)
      if (isNaN(date.getTime())) {
        return '无效日期'
      }
      return date.toLocaleString()
    },
    
    // 选择文件
    selectFile(file) {
      this.$store.commit('SET_CURRENT_FILE', file)
      // 加载该文件的接口列表
      this.$store.dispatch('loadInterfaces', file.id)
    },
    
    // 删除文件
    async deleteFile(file) {
      try {
        await this.$confirm(`确定要删除文件 "${file.filename}" 吗？`, '确认删除', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        // 移除/api前缀，因为axios.defaults.baseURL已经配置了/api
        const response = await this.$axios.delete(`/files/${file.id}`)
        this.$message.success(response.data.message)
        this.loadFiles() // 重新加载文件列表
        
        // 如果删除的是当前选中的文件，清除当前文件和接口列表
        if (this.$store.state.currentFile && this.$store.state.currentFile.id === file.id) {
          this.$store.commit('SET_CURRENT_FILE', null)
          this.$store.commit('SET_INTERFACES', [])
        }
      } catch (error) {
        if (error.message !== '取消') {
          this.$message.error('删除文件失败')
          console.error('删除文件失败:', error)
        }
      }
    }
  }
}
</script>

<style scoped>
.file-upload-view {
  height: 100%;
  padding: 10px;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.file-list {
  height: calc(100% - 60px);
  overflow-y: auto;
}

.file-card {
  margin-bottom: 10px;
  cursor: pointer;
}

.file-info {
  margin-bottom: 5px;
}

.file-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.file-meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #999;
  margin-bottom: 10px;
}

/* 解析结果样式 */
.file-parse-result {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
  background-color: #f0f9eb;
  border-radius: 4px;
  margin-bottom: 10px;
  font-size: 13px;
}

.parse-count {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #67c23a;
}

.parse-count i {
  font-size: 14px;
}

.file-actions {
  display: flex;
  justify-content: flex-end;
  gap: 5px;
}
</style>