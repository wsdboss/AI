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
            
            <!-- Mock配置 -->
            <el-divider>Mock配置</el-divider>
            <el-form :model="mockConfigForm" label-width="120px">
              <el-form-item label="默认Mock条数">
                <el-input-number v-model="mockConfigForm.default_count" :min="1" :max="1000" :step="1"></el-input-number>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveMockConfig">保存配置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
        
        <!-- HTTP/WS请求发送 -->
        <el-tab-pane label="HTTP/WS请求发送" name="request-send">
          <div class="detail-section">
            <!-- 接口类型开关 -->
            <div style="text-align: left; margin-bottom: 20px;">
              <span style="margin-right: 10px; font-weight: bold;">接口类型：</span>
              <el-switch 
                v-model="interfaceTypeSwitch" 
                active-text="WebSocket" 
                inactive-text="HTTP" 
                @change="toggleInterfaceType"
                :disabled="false"
              >
              </el-switch>
            </div>
            <!-- HTTP请求内容 -->
            <div v-if="!currentInterface?.is_websocket">
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
            
            <!-- WebSocket请求内容 -->
            <div v-else>
              <!-- WebSocket连接状态 -->
              <div class="websocket-connection-info">
                <el-badge :value="websocketStatus" :type="websocketStatus === '已连接' ? 'success' : websocketStatus === '连接中' ? 'warning' : 'danger'" />
                <span class="websocket-status-text">{{ websocketStatus }}</span>
                <el-button 
                  :type="websocketStatus === '已连接' ? 'danger' : 'primary'" 
                  size="small" 
                  @click="toggleWebSocketConnection"
                  :loading="websocketConnecting"
                  style="margin-left: 10px;"
                >
                  {{ websocketStatus === '已连接' ? '断开连接' : '连接' }}
                </el-button>
              </div>
              
              <!-- WebSocket消息发送表单 -->
              <el-form :model="websocketForm" label-width="80px" style="margin-top: 20px;">
                <!-- WebSocket连接URL -->
                <el-form-item label="WebSocket连接">
                  <div class="websocket-url-container">
                    <el-input
                      v-model="websocketUrl"
                      readonly
                      placeholder="WebSocket连接URL"
                      prefix-icon="el-icon-link"
                    ></el-input>
                    <el-button type="primary" size="small" @click="copyWebSocketUrl" style="margin-left: 10px;">
                      <i class="el-icon-document-copy"></i> 复制
                    </el-button>
                  </div>
                </el-form-item>
                
                <!-- 消息发送区域 -->
                <el-form-item label="发送消息">
                  <el-input
                    type="textarea"
                    v-model="websocketForm.message"
                    :rows="4"
                    placeholder="请输入要发送的消息，支持JSON格式"
                  ></el-input>
                </el-form-item>
                
                <el-form-item label="消息格式">
                  <el-radio-group v-model="websocketForm.format">
                    <el-radio label="raw">原始文本</el-radio>
                    <el-radio label="json">JSON格式化</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item>
                  <el-button 
                    type="primary" 
                    @click="sendWebSocketMessage" 
                    :disabled="websocketStatus !== '已连接'"
                  >
                    发送消息
                  </el-button>
                  <el-button @click="clearWebSocketMessages">清除消息</el-button>
                  <el-button @click="formatWebSocketMessage" :disabled="!websocketForm.message">
                    格式化消息
                  </el-button>
                </el-form-item>
              </el-form>
              
              <!-- 消息历史记录 -->
              <div class="websocket-messages-container" v-if="websocketMessages.length > 0">
                <h4>消息历史</h4>
                <el-divider></el-divider>
                <div class="websocket-messages">
                  <div 
                    v-for="(msg, index) in websocketMessages" 
                    :key="index" 
                    :class="['websocket-message-item', msg.type]"
                  >
                    <div class="message-header">
                      <span class="message-type">{{ msg.type === 'sent' ? '发送' : '接收' }}</span>
                      <span class="message-time">{{ msg.timestamp }}</span>
                    </div>
                    <div class="message-content">
                      <pre v-if="msg.format === 'json'" class="json-message">{{ msg.content }}</pre>
                      <div v-else class="text-message">{{ msg.content }}</div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="no-messages">
                <el-empty description="暂无消息记录"></el-empty>
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
      },
      
      // WebSocket相关状态
      websocketStatus: '未连接', // 未连接、连接中、已连接
      websocketConnecting: false,
      websocketForm: {
        message: '',
        format: 'raw' // raw 或 json
      },
      websocketMessages: [],
      websocketConnectionId: null, // 用于标识当前连接
      websocketUrl: '', // WebSocket连接URL
      interfaceTypeSwitch: false // 接口类型切换开关，false为HTTP，true为WebSocket
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
        this.updateWebSocketUrl()
        // 更新接口类型开关状态
        if (newInterface) {
          this.interfaceTypeSwitch = newInterface.is_websocket
        } else {
          this.interfaceTypeSwitch = false
        }
      },
      deep: true
    },
    // 当接口的is_websocket属性变化时，更新开关状态
    'currentInterface.is_websocket': {
      handler(newValue) {
        this.interfaceTypeSwitch = newValue
      }
    }
  },
  
  mounted() {
    this.updateRequestUrl()
    this.updateWebSocketUrl()
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
        
        // 解析请求参数
        let params = {}
        try {
          params = JSON.parse(this.requestForm.params)
        } catch (e) {
          this.$message.error('请求参数格式错误，请输入JSON格式')
          this.sending = false
          return
        }
        
        // 检查WebSocket连接状态
        if (this.$socket.getConnectionStatus()) {
          // 使用WebSocket发送请求
          this.$socket.callDynamicInterface(
            this.currentInterface.path,
            this.currentInterface.method,
            {
              params: params,
              mock_count: this.requestForm.mock_count
            }
          )
          
          // 监听WebSocket响应
          const responseHandler = (data) => {
            this.responseResult = data
            this.responseResultStr = JSON.stringify(data, null, 2)
            this.$message.success('请求发送成功')
            this.sending = false
            // 移除监听器
            this.$socket.off('dynamic_response', responseHandler)
          }
          
          // 添加响应监听器
          this.$socket.on('dynamic_response', responseHandler)
        } else {
          // WebSocket连接失败，回退到HTTP请求
          console.log('WebSocket未连接，回退到HTTP请求')
          
          // 移除/api前缀，因为axios.defaults.baseURL已经配置了/api
          const url = `/dynamic${this.currentInterface.path}`
          
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
        }
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
    
    // 切换接口类型（HTTP/WebSocket）
    async toggleInterfaceType() {
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      try {
        // 使用Element UI的Loading服务显示加载状态
        const loading = this.$loading({
          lock: true,
          text: `正在${this.interfaceTypeSwitch ? '生成' : '切换回'}WebSocket接口...`,
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        })
        
        let response
        if (this.interfaceTypeSwitch) {
          // 切换为WebSocket接口
          response = await this.$axios.post(`/interfaces/generate-websocket/${this.currentInterface.id}`)
        } else {
          // 切换回HTTP接口
          response = await this.$axios.post(`/interfaces/switch-to-http/${this.currentInterface.id}`)
        }
        
        this.$message.success(`接口已${this.interfaceTypeSwitch ? '切换为WebSocket类型' : '切换回HTTP类型'}`)
        
        // 更新当前接口的is_websocket属性
        this.currentInterface.is_websocket = this.interfaceTypeSwitch
        
        // 更新Vuex中的接口信息
        this.$store.commit('SET_CURRENT_INTERFACE', this.currentInterface)
        
        // 重新加载接口列表，确保其他组件也能看到更新
        this.$store.dispatch('loadInterfaces', this.currentFile?.id)
        
        // 关闭加载状态
        loading.close()
      } catch (error) {
        this.$message.error(`接口类型切换失败: ${error.response?.data?.message || error.message}`)
        console.error('接口类型切换失败:', error)
        // 恢复开关状态
        this.interfaceTypeSwitch = !this.interfaceTypeSwitch
        // 关闭加载状态
        if (this.loadingInstance) {
          this.loadingInstance.close()
        }
      }
    },
    
    // 生成WebSocket接口
    async generateWebSocketInterface() {
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      try {
        // 使用Element UI的Loading服务显示加载状态
        const loading = this.$loading({
          lock: true,
          text: '正在生成WebSocket接口...',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        })
        
        // 调用后端API生成WebSocket接口
        const response = await this.$axios.post(`/interfaces/generate-websocket/${this.currentInterface.id}`)
        
        this.$message.success('WebSocket接口生成成功')
        
        // 更新当前接口的is_websocket属性
        this.currentInterface.is_websocket = true
        
        // 更新Vuex中的接口信息
        this.$store.commit('SET_CURRENT_INTERFACE', this.currentInterface)
        
        // 重新加载接口列表，确保其他组件也能看到更新
        this.$store.dispatch('loadInterfaces', this.currentFile?.id)
        
        // 关闭加载状态
        loading.close()
      } catch (error) {
        this.$message.error('WebSocket接口生成失败')
        console.error('生成WebSocket接口失败:', error)
        // 关闭加载状态
        if (this.loadingInstance) {
          this.loadingInstance.close()
        }
      }
    },
    
    // 重置请求表单
    resetRequestForm() {
      this.requestForm = {
        params: '{}',
        mock_count: 10
      }
      this.responseResult = null
      this.responseResultStr = ''
    },
    
    // WebSocket相关方法
    
    // 切换WebSocket连接状态
    toggleWebSocketConnection() {
      if (this.websocketStatus === '已连接') {
        this.disconnectWebSocket()
      } else {
        this.connectWebSocket()
      }
    },
    
    // 连接WebSocket
    async connectWebSocket() {
      try {
        this.websocketConnecting = true
        this.websocketStatus = '连接中'
        
        // 检查WebSocket服务是否已初始化
        if (!this.$socket.getConnectionStatus()) {
          // 重新初始化WebSocket连接
          this.$socket.init()
        }
        
        // 等待连接建立
        await this.waitForWebSocketConnection()
        
        this.websocketStatus = '已连接'
        this.websocketConnecting = false
        
        // 注册WebSocket消息处理器
        this.registerWebSocketHandlers()
        
        this.$message.success('WebSocket连接成功')
      } catch (error) {
        this.websocketStatus = '未连接'
        this.websocketConnecting = false
        this.$message.error('WebSocket连接失败: ' + error.message)
        console.error('WebSocket连接失败:', error)
      }
    },
    
    // 等待WebSocket连接建立
    waitForWebSocketConnection() {
      return new Promise((resolve, reject) => {
        const maxAttempts = 5
        let attempts = 0
        
        const checkConnection = () => {
          attempts++
          if (this.$socket.getConnectionStatus()) {
            resolve()
          } else if (attempts >= maxAttempts) {
            reject(new Error('连接超时'))
          } else {
            setTimeout(checkConnection, 1000)
          }
        }
        
        checkConnection()
      })
    },
    
    // 断开WebSocket连接
    disconnectWebSocket() {
      try {
        this.websocketStatus = '未连接'
        // 移除当前接口的消息监听器
        this.removeWebSocketHandlers()
        // 断开WebSocket连接
        this.$socket.disconnect()
        this.$message.success('WebSocket连接已断开')
      } catch (error) {
        this.$message.error('断开WebSocket连接失败: ' + error.message)
        console.error('断开WebSocket连接失败:', error)
      }
    },
    
    // 注册WebSocket消息处理器
    registerWebSocketHandlers() {
      // 监听WebSocket消息
      this.$socket.on('message', this.handleWebSocketMessage)
      // 监听动态接口响应（针对WebSocket接口）
      this.$socket.on('dynamic_response', this.handleWebSocketDynamicResponse)
      // 监听连接断开
      this.$socket.on('disconnect', this.handleWebSocketDisconnect)
    },
    
    // 移除WebSocket消息处理器
    removeWebSocketHandlers() {
      this.$socket.off('message', this.handleWebSocketMessage)
      this.$socket.off('dynamic_response', this.handleWebSocketDynamicResponse)
      this.$socket.off('disconnect', this.handleWebSocketDisconnect)
    },
    
    // 处理WebSocket消息
    handleWebSocketMessage(data) {
      this.addWebSocketMessage('received', data)
    },
    
    // 处理WebSocket动态接口响应
    handleWebSocketDynamicResponse(data) {
      this.addWebSocketMessage('received', data)
    },
    
    // 处理WebSocket断开连接
    handleWebSocketDisconnect() {
      if (this.websocketStatus === '已连接') {
        this.websocketStatus = '未连接'
        this.$message.warning('WebSocket连接已断开')
      }
    },
    
    // 发送WebSocket消息
    sendWebSocketMessage() {
      if (!this.currentInterface || !this.$socket.getConnectionStatus()) {
        this.$message.error('WebSocket未连接')
        return
      }
      
      try {
        let message = this.websocketForm.message
        let formattedMessage = message
        
        // 如果选择JSON格式化，尝试解析并格式化
        if (this.websocketForm.format === 'json') {
          try {
            const parsed = JSON.parse(message)
            formattedMessage = JSON.stringify(parsed, null, 2)
          } catch (e) {
            this.$message.warning('消息不是有效的JSON格式，将以原始文本发送')
          }
        }
        
        // 发送消息
        this.$socket.callDynamicInterface(
          this.currentInterface.path,
          this.currentInterface.method,
          {
            params: JSON.parse(this.requestForm.params || '{}'),
            mock_count: this.requestForm.mock_count,
            message: message
          }
        )
        
        // 添加到发送消息历史
        this.addWebSocketMessage('sent', formattedMessage)
        
        // 清空输入框
        this.websocketForm.message = ''
        
        this.$message.success('消息发送成功')
      } catch (error) {
        this.$message.error('消息发送失败: ' + error.message)
        console.error('发送WebSocket消息失败:', error)
      }
    },
    
    // 添加WebSocket消息到历史记录
    addWebSocketMessage(type, content) {
      const timestamp = new Date().toLocaleString()
      let formattedContent = content
      let format = this.websocketForm.format
      
      // 如果内容是对象，转换为字符串
      if (typeof content === 'object' && content !== null) {
        formattedContent = JSON.stringify(content, null, 2)
        format = 'json'
      }
      
      this.websocketMessages.push({
        type: type, // 'sent' 或 'received'
        content: formattedContent,
        timestamp: timestamp,
        format: format
      })
      
      // 限制消息历史记录数量，最多保存50条
      if (this.websocketMessages.length > 50) {
        this.websocketMessages.shift()
      }
      
      // 自动滚动到底部
      this.$nextTick(() => {
        const messagesContainer = this.$el.querySelector('.websocket-messages')
        if (messagesContainer) {
          messagesContainer.scrollTop = messagesContainer.scrollHeight
        }
      })
    },
    
    // 格式化WebSocket消息
    formatWebSocketMessage() {
      try {
        const message = this.websocketForm.message
        if (!message) {
          this.$message.warning('请先输入消息内容')
          return
        }
        
        // 尝试解析为JSON
        const parsed = JSON.parse(message)
        // 格式化
        this.websocketForm.message = JSON.stringify(parsed, null, 2)
        this.websocketForm.format = 'json'
        
        this.$message.success('消息格式化成功')
      } catch (error) {
        this.$message.error('消息格式化失败: ' + error.message)
        console.error('格式化WebSocket消息失败:', error)
      }
    },
    
    // 清除WebSocket消息历史
    clearWebSocketMessages() {
      this.websocketMessages = []
      this.$message.success('消息历史已清除')
    },
    
    // 组件销毁时清理WebSocket连接
    beforeDestroy() {
      this.removeWebSocketHandlers()
    },
    
    // 复制WebSocket连接URL
    copyWebSocketUrl() {
      if (!this.websocketUrl) {
        this.$message.warning('WebSocket连接URL为空')
        return
      }
      
      navigator.clipboard.writeText(this.websocketUrl)
        .then(() => {
          this.$message.success('WebSocket连接已复制到剪贴板')
        })
        .catch(err => {
          console.error('复制失败:', err)
          this.$message.error('复制失败，请手动复制')
        })
    },
    
    // 更新WebSocket连接URL
    updateWebSocketUrl() {
      if (this.currentInterface) {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const host = window.location.host
        const path = this.currentInterface.path
        // 确保路径包含前导斜杠
        const normalizedPath = path.startsWith('/') ? path : `/${path}`
        this.websocketUrl = `${protocol}//${host}${normalizedPath}`
      } else {
        this.websocketUrl = ''
      }
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
  overflow-y: auto;
  padding: 16px 0;
}



/* 章节样式 */
.detail-section {
  margin-bottom: 10px;
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
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
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
  
  /* WebSocket请求样式 */
  .websocket-connection-info {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #f5f7fa;
    border-radius: 4px;
    margin-bottom: 10px;
  }
  
  .websocket-status-text {
    margin-left: 10px;
    font-weight: bold;
  }
  
  .websocket-messages-container {
    margin-top: 20px;
    padding: 10px;
    background-color: #f5f7fa;
    border-radius: 4px;
    max-height: 400px;
    overflow-y: auto;
  }
  
  .websocket-messages {
    max-height: 350px;
    overflow-y: auto;
  }
  
  .websocket-message-item {
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 4px;
    word-wrap: break-word;
  }
  
  .websocket-message-item.sent {
    background-color: #e6f7ff;
    border-left: 4px solid #1890ff;
    margin-right: 20px;
  }
  
  .websocket-message-item.received {
    background-color: #f6ffed;
    border-left: 4px solid #52c41a;
    margin-left: 20px;
  }
  
  .message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
    font-size: 12px;
  }
  
  .message-type {
    font-weight: bold;
    color: #606266;
  }
  
  .message-time {
    color: #909399;
  }
  
  .message-content {
    font-family: 'Courier New', Courier, monospace;
    font-size: 13px;
    line-height: 1.5;
  }
  
  .json-message {
    margin: 0;
    padding: 5px;
    background-color: white;
    border-radius: 3px;
    overflow-x: auto;
  }
  
  .text-message {
    white-space: pre-wrap;
  }
  
  .no-messages {
    text-align: center;
    padding: 20px;
    color: #909399;
  }
  
  .websocket-url-container {
    display: flex;
    align-items: center;
  }
</style>