<template>
  <div class="interface-detail-view">
    <div class="detail-title">
      <h2>接口详情</h2>
    </div>
    <div class="view-header" v-if="currentInterface">
      <h3>{{ currentInterface.name }}</h3>
      <div class="interface-basic-info">
        <span class="interface-method" :class="'method-' + currentInterface.method.toLowerCase()">
          {{ currentInterface.method }}
        </span>
        <span class="interface-path">{{ currentInterface.path }}</span>
      </div>
    </div>
    <div class="no-data" v-else>
      <el-empty description="请选择一个接口查看详情"></el-empty>
    </div>
    
    <!-- 接口详情内容 - 使用Tab形式 -->
    <div class="detail-content" v-if="currentInterface">
      <el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick">
        <!-- 接口信息 -->
        <el-tab-pane label="接口信息" name="info">
          <div class="detail-section">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="接口名称">{{ currentInterface.name }}</el-descriptions-item>
              <el-descriptions-item label="请求方式">{{ currentInterface.method }}</el-descriptions-item>
              <el-descriptions-item label="接口路径">{{ currentInterface.path }}</el-descriptions-item>
              <el-descriptions-item label="接口描述" v-if="currentInterface.description">
                {{ currentInterface.description }}
              </el-descriptions-item>
              <el-descriptions-item label="所属文件">{{ currentFile?.filename || '未知文件' }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-tab-pane>
        
        <!-- 请求参数 -->
        <el-tab-pane label="请求参数" name="params">
          <div class="detail-section">
            <el-table :data="interfaceParams" stripe style="width: 100%" v-if="interfaceParams.length > 0">
              <el-table-column prop="name" label="参数名" width="150"></el-table-column>
              <el-table-column prop="param_type" label="参数类型" width="150"></el-table-column>
              <el-table-column prop="required" label="是否必填" width="100">
                <template slot-scope="scope">
                  <el-tag type="success" v-if="scope.row.required">必填</el-tag>
                  <el-tag type="info" v-else>可选</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="描述"></el-table-column>
              <el-table-column prop="example" label="示例值"></el-table-column>
            </el-table>
            <el-empty description="暂无请求参数" v-else></el-empty>
          </div>
        </el-tab-pane>
        
        <!-- 响应参数 -->
        <el-tab-pane label="响应参数" name="responses">
          <div class="detail-section">
            <el-table :data="interfaceResponses" stripe style="width: 100%" v-if="interfaceResponses.length > 0">
              <el-table-column prop="name" label="字段名" width="150"></el-table-column>
              <el-table-column prop="response_type" label="字段类型" width="150"></el-table-column>
              <el-table-column prop="description" label="描述"></el-table-column>
              <el-table-column prop="example" label="示例值"></el-table-column>
            </el-table>
            <el-empty description="暂无响应参数" v-else></el-empty>
          </div>
        </el-tab-pane>
        
        <!-- Mock配置 -->
        <el-tab-pane label="Mock配置" name="mock-config">
          <div class="detail-section">
            <el-form :model="mockConfigForm" label-width="120px">
              <el-form-item label="Mock服务开关">
                <el-switch v-model="mockConfigForm.enabled"></el-switch>
              </el-form-item>
              <el-form-item label="默认Mock条数">
                <el-input-number v-model="mockConfigForm.default_count" :min="1" :max="1000" :step="1"></el-input-number>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveMockConfig">保存配置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>

        
        <!-- 发送请求 -->
        <el-tab-pane label="发送请求" name="request">
          <div class="detail-section">
            <el-form :model="requestForm" label-width="80px">
              <!-- 请求路径展示 -->
              <el-form-item label="请求路径">
                <div class="request-path-container">
                  <el-input
                    v-model="requestUrl"
                    readonly
                    placeholder="请求路径"
                    prefix-icon="el-icon-link"
                  ></el-input>
                  <el-button type="primary" size="small" @click="copyRequestUrl" style="margin-left: 10px;">
                    <i class="el-icon-document-copy"></i> 复制
                  </el-button>
                </div>
                <div class="browser-support-tip" v-if="!isBrowserSupported">
                  <el-alert
                    title="浏览器支持提示"
                    type="warning"
                    description="当前浏览器可能不支持直接访问该地址，建议使用发送请求功能进行测试。"
                    show-icon
                    :closable="false"
                    size="small"
                  ></el-alert>
                </div>
              </el-form-item>
              
              <el-form-item label="请求参数">
                <el-input
                  type="textarea"
                  v-model="requestForm.params"
                  :rows="6"
                  placeholder="请输入JSON格式的请求参数"
                ></el-input>
              </el-form-item>
              <el-form-item label="Mock条数">
                <div class="mock-count-display">{{ requestForm.mock_count }}</div>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="sendRequest" :loading="sending">发送请求</el-button>
                <el-button @click="resetRequestForm">重置</el-button>
              </el-form-item>
            </el-form>
            
            <!-- 响应结果 -->
            <div class="response-result" v-if="responseResult">
              <h4>响应结果</h4>
              <el-divider></el-divider>
              <div class="response-status" :class="responseResult.code === 0 ? 'status-success' : 'status-error'">
                <span class="status-code">{{ responseResult.code }}</span>
                <span class="status-message">{{ responseResult.message }}</span>
              </div>
              <div class="response-data">
                <el-input
                  type="textarea"
                  v-model="responseResultStr"
                  :rows="10"
                  readonly
                  placeholder="响应数据"
                ></el-input>
              </div>
            </div>
          </div>
        </el-tab-pane>
        

      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InterfaceDetailView',
  data() {
    return {
      activeTab: 'info',
      sending: false,
      responseResult: null,
      responseResultStr: '',
      currentInterface: null,
      currentFile: null,
      interfaceParams: [],
      interfaceResponses: [],
      mockConfig: null,
      mockConfigForm: {
        enabled: true,
        default_count: 10
      },
      requestUrl: '',
      isBrowserSupported: true,

      requestForm: {
        params: '{}',
        mock_count: 10
      }
    }
  },
  created() {
    // 监听Vuex中当前接口的变化
    this.$store.watch(
      state => state.currentInterface,
      (newInterface) => {
        this.currentInterface = newInterface
        if (newInterface) {
          this.loadInterfaceDetail(newInterface.id)
        }
      },
      { deep: true }
    )
    
    // 监听Vuex中当前文件的变化
    this.$store.watch(
      state => state.currentFile,
      (newFile) => {
        this.currentFile = newFile
      },
      { deep: true }
    )
    
  },
  
  watch: {
    // 当当前接口变化时，更新请求URL和浏览器支持状态
    currentInterface: {
      handler(newInterface) {
        this.updateRequestUrl()
      },
      deep: true
    }
  },
  
  mounted() {
    this.updateRequestUrl()
  },

  methods: {
    
    // 加载接口详情
    async loadInterfaceDetail(interfaceId) {
      try {
        // 移除/api前缀，因为axios.defaults.baseURL已经配置了/api
        // 加载接口参数
        const paramsResponse = await this.$axios.get(`/interfaces/${interfaceId}/params`)
        this.interfaceParams = paramsResponse.data
        
        // 加载接口响应字段
        const responsesResponse = await this.$axios.get(`/interfaces/${interfaceId}/responses`)
        this.interfaceResponses = responsesResponse.data
        
        // 加载Mock配置，确保和后端数据库同步
        const mockResponse = await this.$axios.get(`/interfaces/${interfaceId}/mock-config`)
        // 保存Mock配置到组件数据中，用于发送请求时使用
        this.mockConfig = mockResponse.data
        // 将mock配置同步到表单中
        this.mockConfigForm = {
          enabled: mockResponse.data.enabled,
          default_count: mockResponse.data.default_count
        }
        // 将mock配置中的默认条数设置到请求表单中
        this.requestForm.mock_count = mockResponse.data.default_count
        
        // 更新请求URL
        this.updateRequestUrl()
      } catch (error) {
        console.error('加载接口详情失败:', error)
      }
    },
    
    // 保存Mock配置
    async saveMockConfig() {
      try {
        if (!this.currentInterface) return
        
        // 保存Mock配置到后端
        await this.$axios.put(`/interfaces/${this.currentInterface.id}/mock-config`, this.mockConfigForm)
        
        // 更新本地mockConfig
        this.mockConfig = {...this.mockConfigForm}
        
        // 更新请求表单中的mock_count
        this.requestForm.mock_count = this.mockConfigForm.default_count
        
        this.$message.success('Mock配置保存成功')
      } catch (error) {
        console.error('保存Mock配置失败:', error)
        this.$message.error('保存Mock配置失败')
      }
    },
    
    // 发送请求
    async sendRequest() {
      try {
        // 检查Mock服务是否启用
        if (!this.mockConfig || !this.mockConfig.enabled) {
          this.$message.error('该接口的Mock服务未启用')
          return
        }
        
        this.sending = true
        this.responseResult = null
        this.responseResultStr = ''
        
        // 移除/api前缀，因为axios.defaults.baseURL已经配置了/api
        const url = `/dynamic${this.currentInterface.path}`
        
        // 解析请求参数
        let params = {}
        try {
          params = JSON.parse(this.requestForm.params)
        } catch (e) {
          this.$message.error('请求参数格式错误，请输入JSON格式')
          this.sending = false
          return
        }
        
        // 构造完整请求参数
        const requestData = {
          params: params,
          mock_count: this.requestForm.mock_count
        }
        
        // 发送请求
        const response = await this.$axios({
          method: this.currentInterface.method.toLowerCase(),
          url: url,
          data: requestData,
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        // 保存响应结果
        this.responseResult = response.data
        this.responseResultStr = JSON.stringify(response.data, null, 2)
        
        // 记录请求日志
        this.$message.success('请求发送成功')
      } catch (error) {
        this.$message.error('请求发送失败')
        console.error('发送请求失败:', error)
      } finally {
        this.sending = false
      }
    },
    
    // 处理Tab切换事件
    handleTabClick(tab) {
      // 当切换到发送请求tab时，更新请求URL
      if (tab.name === 'request') {
        this.updateRequestUrl()
      }
    },
    
    // 更新请求URL并检查浏览器支持
    updateRequestUrl() {
      if (this.currentInterface && this.currentInterface.path) {
        // 生成完整的请求URL，包含/api前缀
        const baseUrl = window.location.origin
        this.requestUrl = `${baseUrl}/api/dynamic${this.currentInterface.path}`
        
        // 检查浏览器是否支持直接访问该地址
        // 这里简单检查是否为标准HTTP/HTTPS协议
        this.isBrowserSupported = window.location.protocol === 'http:' || window.location.protocol === 'https:'
      } else {
        // 当currentInterface或path为空时，设置默认值
        this.requestUrl = '请选择一个有效的接口'
        this.isBrowserSupported = true
      }
    },
    
    // 复制请求URL到剪贴板
    copyRequestUrl() {
      if (!this.requestUrl) {
        this.$message.warning('请求URL为空')
        return
      }
      
      // 使用Clipboard API复制文本
      navigator.clipboard.writeText(this.requestUrl)
        .then(() => {
          this.$message.success('请求URL已复制到剪贴板')
        })
        .catch(err => {
          console.error('复制失败:', err)
          this.$message.error('复制失败，请手动复制')
        })
    },
    
    // 重置请求表单
    resetRequestForm() {
      this.requestForm = {
        params: '{}',
        mock_count: 10
      }
      this.responseResult = null
      this.responseResultStr = ''
    }
  }
}
</script>

<style scoped>
.interface-detail-view {
  height: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.detail-title {
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eaeaea;
}

.detail-title h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.view-header {
  margin-bottom: 10px;
}

.interface-basic-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.interface-method {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.method-get {
  background-color: #67c23a;
}

.method-post {
  background-color: #409eff;
}

.method-put {
  background-color: #e6a23c;
}

.method-delete {
  background-color: #f56c6c;
}

.interface-path {
  font-size: 13px;
  color: #606266;
  font-family: 'Courier New', Courier, monospace;
}

.no-data {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.detail-content {
  flex: 1;
  overflow: hidden;
  padding: 16px 0;
}



/* 章节样式 */
.detail-section {
  margin-bottom: 30px;
  padding: 16px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s ease;
}

.detail-section:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  padding-bottom: 8px;
  border-bottom: 2px solid #409eff;
}

.response-result {
  margin-top: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.log-list {
  max-height: 300px;
  overflow-y: auto;
}

.log-item {
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.log-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.log-method {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: bold;
  color: white;
}

.log-path {
  font-size: 12px;
  color: #606266;
  font-family: 'Courier New', Courier, monospace;
  flex: 1;
}

.log-time {
  font-size: 11px;
  color: #999;
}

.log-content {
    margin-top: 5px;
    padding: 8px;
    background-color: white;
    border-radius: 4px;
    font-size: 12px;
    overflow-x: auto;
  }
  
  /* 请求路径展示样式 */
  .request-path-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .browser-support-tip {
    margin-top: 10px;
  }
  
  /* Mock条数展示样式 */
  .mock-count-display {
    display: inline-block;
    padding: 8px 15px;
    background-color: #f5f7fa;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    font-size: 14px;
    color: #606266;
    min-width: 80px;
    text-align: center;
  }
</style>