<template>
  <div class="file-upload-view">
    <!-- 上传区 -->
    <div class="upload-section">
      <h3 class="section-title">上传区域</h3>
      <div class="upload-content">
        <el-upload
          class="upload-demo"
          drag
          :action="uploadUrl"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :before-upload="beforeUpload"
          multiple
          :show-file-list="false"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">拖拽文件到此处或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">
            支持格式：JSON/YAML/XLSX/MD/TXT/DOC/DOCX/PDF/PNG/JPG
          </div>
        </el-upload>
      </div>
    </div>
    
    <!-- 文件解析结果区 -->
    <div class="file-result-section">
      <h3 class="section-title">文件解析结果区</h3>
      <!-- 添加查看所有接口按钮 -->
      <div class="file-actions-header" v-if="files.length > 0">
        <el-button size="small" type="primary" @click="loadAllInterfaces">
          <i class="el-icon-view"></i> 查看所有接口
        </el-button>
      </div>
      <div class="file-list">
        <el-empty description="暂无上传的文件" v-if="files.length === 0"></el-empty>
        <el-card v-for="file in files" :key="file.id" class="file-card" @click.native="selectFile(file)">
          <div class="file-info">
            <div class="file-name">{{ file.filename }}</div>
            <div class="file-meta">
              <span class="file-type">{{ file.file_type }}</span>
              <span class="file-size">{{ formatFileSize(file.size) }}</span>
              <span class="file-time">{{ formatDateTime(file.uploaded_at) }}</span>
            </div>
            <!-- 文件上传状态 -->
            <div class="file-status">
              <el-tag :type="file.parsed ? 'success' : 'danger'" size="small" effect="light">
                {{ file.parsed ? '上传成功' : '上传失败' }}
              </el-tag>
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
            <!-- 添加查看按钮，用于加载接口列表 -->
            <el-button size="mini" type="success" @click.stop="selectFile(file)">
              <i class="el-icon-view"></i> 查看
            </el-button>
            <!-- 增加导出按钮 -->
            <el-button size="mini" type="primary" @click.stop="downloadFile(file)">
              <i class="el-icon-download"></i> 导出
            </el-button>
            <el-button size="mini" type="danger" @click.stop="deleteFile(file)">
              <i class="el-icon-delete"></i> 删除
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUploadView',
  data() {
    return {
      showUploadDialog: false,
      files: [],
      uploadUrl: '/files/upload' // 使用相对路径，直接访问后端
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
      // 上传完成后默认展示所有接口
      this.loadAllInterfaces()
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
    },
    
    // 导出文件
    downloadFile(file) {
      try {
        // 使用window.open直接打开下载链接，使用正确的路径（无前缀）
        window.open(`/files/download/${file.id}`, '_blank')
      } catch (error) {
        this.$message.error('文件下载失败')
        console.error('文件下载失败:', error)
      }
    },
    
    // 加载所有接口
    loadAllInterfaces() {
      this.$store.commit('SET_CURRENT_FILE', null)
      // 加载所有接口
      this.$store.dispatch('loadInterfaces')
    }
  }
}
</script>

<style scoped>
.file-upload-view {
  height: 100%;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  overflow-y: auto;
}

/* 上传区样式 */
.upload-section {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* 文件解析结果区样式 */
.file-result-section {
  flex: 1;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  min-height: 0;
}

/* 区域标题样式 */
.section-title {
  margin: 0 0 15px 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 8px;
}

/* 上传内容样式 */
.upload-content {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  padding: 15px;
  text-align: center;
  transition: all 0.3s ease;
  max-width: 100%;
  box-sizing: border-box;
}

/* 设置上传拖拽区域宽度 */
.upload-demo >>> .el-upload-dragger {
  width: 258px !important;
  box-sizing: border-box;
}

.upload-content:hover {
  border-color: #409eff;
}

/* 文件列表样式 */
.file-list {
  height: calc(100% - 40px);
  overflow-y: auto;
}

/* 文件卡片样式 */
.file-card {
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 文件信息样式 */
.file-info {
  margin-bottom: 5px;
}

.file-name {
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 14px;
}

.file-meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

/* 文件上传状态样式 */
.file-status {
  margin-bottom: 8px;
}

/* 解析结果样式 */
.file-parse-result {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 8px 10px;
  background-color: #f0f9eb;
  border-radius: 4px;
  margin-bottom: 10px;
  font-size: 12px;
}

.parse-count {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #67c23a;
}

.parse-count i {
  font-size: 13px;
}

/* 文件操作样式 */
.file-actions {
  display: flex;
  justify-content: flex-end;
  gap: 5px;
}

/* 滚动条样式优化 */
.file-upload-view::-webkit-scrollbar,
.file-result-section::-webkit-scrollbar,
.file-list::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.file-upload-view::-webkit-scrollbar-track,
.file-result-section::-webkit-scrollbar-track,
.file-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.file-upload-view::-webkit-scrollbar-thumb,
.file-result-section::-webkit-scrollbar-thumb,
.file-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.file-upload-view::-webkit-scrollbar-thumb:hover,
.file-result-section::-webkit-scrollbar-thumb:hover,
.file-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>