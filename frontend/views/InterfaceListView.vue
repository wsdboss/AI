<template>
  <div class="interface-list-view">
    <div class="view-header">
      <h3>接口列表</h3>
      <div class="view-actions">
        <el-select v-model="filterMethod" placeholder="请求方式" clearable size="small" @change="handleFilterChange">
          <el-option label="GET" value="GET"></el-option>
          <el-option label="POST" value="POST"></el-option>
          <el-option label="PUT" value="PUT"></el-option>
          <el-option label="DELETE" value="DELETE"></el-option>
          <el-option label="PATCH" value="PATCH"></el-option>
        </el-select>
        <el-input
          v-model="searchKeyword"
          placeholder="搜索接口名称或路径"
          size="small"
          prefix-icon="el-icon-search"
          clearable
          @input="handleSearch"
        ></el-input>
      </div>
    </div>
    
    <!-- 接口列表 - 参考APIFox风格 -->
    <div class="interface-list">
      <div class="interface-stats">
        <div class="stats-item">
          <span class="stats-label">接口总数:</span>
          <span class="stats-value">{{ filteredInterfaces.length }}</span>
        </div>
        <div class="stats-item">
          <span class="stats-label">未生成服务:</span>
          <span class="stats-value warning">{{ filteredInterfaces.filter(intf => !intf.service_generated).length }}</span>
        </div>
      </div>
      
      <div class="interface-list-container">
        <div v-if="filteredInterfaces.length === 0" class="empty-state">
          <el-empty description="暂无接口数据"></el-empty>
        </div>
        
        <div v-else>

          
          <!-- 接口列表 -->
          <div class="interface-items">
            <div
              v-for="intf in filteredInterfaces"
              :key="intf.id"
              class="interface-item"
              :class="{ 'selected': currentInterface && currentInterface.id === intf.id }"
              @click="selectInterface(intf)"
            >
              <!-- 接口头部 -->
              <div class="interface-item-header">
                <div class="interface-method" :class="'method-' + intf.method.toLowerCase()">
                  {{ intf.method }}
                </div>
                <div class="interface-path">{{ intf.path }}</div>
                <div class="interface-status" v-if="!intf.service_generated">
                  <el-tag :type="getMockConfig(intf.id).enabled ? 'success' : 'warning'" size="mini">
                    {{ getMockConfig(intf.id).enabled ? '已启用Mock' : '未生成' }}
                  </el-tag>
                </div>
              </div>
              
              <!-- 接口名称 -->
              <div class="interface-name">{{ intf.name }}</div>
              
              <!-- 接口描述 -->
              <div class="interface-description" v-if="intf.description">
                {{ intf.description }}
              </div>
              
              <!-- Mock服务状态 -->
              <div class="mock-status">
                <span class="mock-label">Mock服务:</span>
                <el-switch 
                  v-model="getMockConfig(intf.id).enabled" 
                  size="mini" 
                  @change="handleMockToggle(intf.id, $event)"
                ></el-switch>
                <span class="mock-status-text" :class="getMockConfig(intf.id).enabled ? 'enabled' : 'disabled'">
                  {{ getMockConfig(intf.id).enabled ? '已启用' : '已禁用' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InterfaceListView',
  data() {
    return {
      filterMethod: '',
      searchKeyword: '',
      interfaces: [],
      currentFile: null,
      currentInterface: null,
      activeInterfaceId: '',
      mockConfigs: {}, // 存储每个接口的Mock配置
      requestForms: {} // 存储每个接口的请求表单数据
    }
  },
  computed: {
    // 过滤后的接口列表
    filteredInterfaces() {
      console.log('计算属性 filteredInterfaces 被调用，接口列表:', this.interfaces)
      console.log('过滤条件 - method:', this.filterMethod, 'keyword:', this.searchKeyword)
      const result = this.interfaces.filter(intf => {
        // 按请求方式过滤
        if (this.filterMethod && intf.method !== this.filterMethod) {
          return false
        }
        // 按关键词搜索
        if (this.searchKeyword) {
          const keyword = this.searchKeyword.toLowerCase()
          return intf.name.toLowerCase().includes(keyword) || 
                 intf.path.toLowerCase().includes(keyword) ||
                 (intf.description && intf.description.toLowerCase().includes(keyword))
        }
        return true
      })
      console.log('过滤结果:', result.length, '个接口')
      return result
    },
    
    // 已启用Mock服务的接口数量
    mockEnabledCount() {
      return this.filteredInterfaces.filter(intf => {
        const mockConfig = this.getMockConfig(intf.id)
        return mockConfig.enabled
      }).length
    },
    
    // 全部Mock服务状态
    allMockEnabled: {
      get() {
        // 当所有接口的Mock服务都启用时，返回true
        if (this.filteredInterfaces.length === 0) {
          return false
        }
        return this.filteredInterfaces.every(intf => {
          const mockConfig = this.getMockConfig(intf.id)
          return mockConfig.enabled
        })
      },
      set(value) {
        // 当设置为true时，将所有接口的Mock服务设置为启用状态
        // 当设置为false时，保持当前状态不变
        if (value) {
          this.filteredInterfaces.forEach(intf => {
            this.$set(this.mockConfigs, intf.id, {
              ...this.getMockConfig(intf.id),
              enabled: true
            })
            this.updateMockConfig(intf.id)
          })
        }
      }
    },
    
    // 全部Mock服务状态文本
    allMockStatusText() {
      if (this.filteredInterfaces.length === 0) {
        return '已禁用'
      }
      const enabledCount = this.mockEnabledCount
      if (enabledCount === 0) {
        return '已禁用'
      } else if (enabledCount === this.filteredInterfaces.length) {
        return '已全部启用'
      } else {
        return '已部分启用'
      }
    }
  },
  created() {
    // 从store获取初始接口列表和当前文件
    this.interfaces = this.$store.state.interfaces
    this.currentFile = this.$store.state.currentFile
    
    // 重置过滤条件，确保不会过滤掉接口
    this.filterMethod = ''
    this.searchKeyword = ''
    console.log('初始化 - 接口列表:', this.interfaces)
    console.log('初始化 - 当前文件:', this.currentFile)
    
    // 监听Vuex中接口列表的变化
    this.$store.watch(
      state => state.interfaces,
      (newInterfaces) => {
        console.log('Vuex接口列表变化:', newInterfaces)
        this.interfaces = newInterfaces
        console.log('组件接口列表更新:', this.interfaces.length, '个接口')
        // 重置过滤条件，确保不会过滤掉接口
        this.filterMethod = ''
        this.searchKeyword = ''
      },
      { deep: true }
    )
    
    // 监听Vuex中当前文件的变化，自动加载对应文件的接口
    this.$store.watch(
      state => state.currentFile,
      (newFile) => {
        console.log('当前文件变化:', newFile)
        this.currentFile = newFile
        if (newFile) {
          console.log('加载文件', newFile.id, '的接口列表')
          this.loadInterfacesFromStore(newFile.id)
        } else {
          console.log('当前文件为空，清除接口列表')
          this.interfaces = []
        }
      },
      { deep: true }
    )
  },
  methods: {
    // 从store加载接口列表
    async loadInterfacesFromStore(fileId = null) {
      try {
        await this.$store.dispatch('loadInterfaces', fileId)
      } catch (error) {
        this.$message.error('加载接口列表失败')
      }
    },
    
    // 处理筛选条件变化
    handleFilterChange() {
      // 筛选条件变化时自动过滤
    },
    
    // 处理搜索
    handleSearch() {
      // 搜索关键词变化时自动过滤
    },
    
    // 切换接口展开/收起状态
    toggleInterface(intf) {
      if (this.activeInterfaceId === intf.id) {
        this.activeInterfaceId = ''
      } else {
        this.activeInterfaceId = intf.id
      }
    },
    
    // 处理手风琴状态变化
    handleAccordionChange(interfaceId) {
      if (interfaceId) {
        const intf = this.interfaces.find(i => i.id === interfaceId)
        if (intf) {
          this.selectInterface(intf)
        }
      }
    },
    
    // 选择接口
    selectInterface(intf) {
      this.currentInterface = intf
      this.$store.commit('SET_CURRENT_INTERFACE', intf)
      // 加载接口详情
      this.$store.dispatch('loadInterfaceDetail', intf.id)
      // 加载Mock配置
      this.$store.dispatch('loadMockConfig', intf.id)
      // 加载请求日志
      this.$store.dispatch('loadRequestLogs', intf.id)
      // 跳转到接口详情页，避免重复导航
      const targetPath = `/interface/${intf.id}`
      if (this.$router.currentRoute.path !== targetPath) {
        this.$router.push(targetPath)
      }
    },
    
    // 获取接口参数
    getInterfaceParams(interfaceId) {
      // 直接从接口对象中获取参数
      const intf = this.filteredInterfaces.find(item => item.id === interfaceId)
      return intf?.params || []
    },
    
    // 获取接口响应参数
    getInterfaceResponses(interfaceId) {
      // 直接从接口对象中获取响应参数
      const intf = this.filteredInterfaces.find(item => item.id === interfaceId)
      return intf?.responses || []
    },
    
    // 获取接口Mock配置
    getMockConfig(interfaceId) {
      if (!this.mockConfigs[interfaceId]) {
        // 使用Vue的$set方法确保响应式
        this.$set(this.mockConfigs, interfaceId, {
          enabled: true,
          default_count: 10
        })
      }
      return this.mockConfigs[interfaceId]
    },
    
    // 处理单个接口Mock服务开关变化
    handleMockToggle(interfaceId, enabled) {
      // 使用Vue的$set方法确保响应式
      this.$set(this.mockConfigs, interfaceId, {
        ...this.getMockConfig(interfaceId),
        enabled: enabled
      })
      // 调用后端API更新配置
      this.updateMockConfig(interfaceId)
    },
    
    // 更新接口Mock配置
    async updateMockConfig(interfaceId) {
      try {
        const mockConfig = this.getMockConfig(interfaceId)
        await this.$axios.put(`/interfaces/${interfaceId}/mock-config`, mockConfig)
      } catch (error) {
        console.error('Mock配置更新失败:', error)
        // 恢复之前的状态
        // this.$message.error('Mock配置更新失败')
      }
    },
    
    // 获取请求表单
    getRequestForm(interfaceId) {
      if (!this.requestForms[interfaceId]) {
        this.requestForms[interfaceId] = {
          params: '{}',
          sending: false,
          responseResult: null,
          responseResultStr: '',
          requestUrl: ''
        }
      }
      return this.requestForms[interfaceId]
    },
    
    // 发送请求
    async sendRequest(intf) {
      try {
        const requestForm = this.getRequestForm(intf.id)
        requestForm.sending = true
        requestForm.responseResult = null
        requestForm.responseResultStr = ''
        
        // 解析请求参数
        let params = {}
        try {
          params = JSON.parse(requestForm.params)
        } catch (e) {
          this.$message.error('请求参数格式错误，请输入JSON格式')
          requestForm.sending = false
          return
        }
        
        // 获取Mock配置中的条数
        const mockConfig = this.getMockConfig(intf.id)
        
        // 构造完整请求参数
        const requestData = {
          params: params,
          mock_count: mockConfig.default_count // 使用Mock配置中的条数
        }
        
        // 构造请求地址
        const requestUrl = `/dynamic${intf.path}`
        requestForm.requestUrl = requestUrl // 保存请求地址
        
        // 发送请求
        const response = await this.$axios({
          method: intf.method.toLowerCase(),
          url: requestUrl,
          data: requestData,
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        // 保存响应结果
        requestForm.responseResult = response.data
        requestForm.responseResultStr = JSON.stringify(response.data, null, 2)
        
        // 记录请求日志
        this.$message.success('请求发送成功')
      } catch (error) {
        this.$message.error('请求发送失败')
        console.error('发送请求失败:', error)
      } finally {
        this.getRequestForm(intf.id).sending = false
      }
    },
    
    // 重置请求表单
    resetRequestForm(interfaceId) {
      this.requestForms[interfaceId] = {
        params: '{}',
        sending: false,
        responseResult: null,
        responseResultStr: '',
        requestUrl: ''
      }
    },
    

  }
}
</script>

<style scoped>
.interface-list-view {
  height: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 头部搜索栏 */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 6px;
  border: 1px solid #eaeaea;
}

.view-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.view-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* 接口统计信息 */
.interface-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #eaeaea;
}

.stats-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stats-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.stats-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.stats-value.warning {
  color: #e6a23c;
}



/* 接口列表容器 */
.interface-list-container {
  flex: 1;
  overflow-y: auto;
  background-color: #ffffff;
  border-radius: 6px;
  border: 1px solid #eaeaea;
  padding: 8px;
}

/* 空状态 */
.empty-state {
  padding: 40px 0;
}

/* 接口列表 */
.interface-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 接口项样式 - 参考APIFox */
.interface-item {
  background-color: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 6px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.interface-item:hover {
  background-color: #f0f7ff;
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);
}

.interface-item.selected {
  background-color: #ecf5ff;
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}

/* 接口项头部 */
.interface-item-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

/* 接口方法标签 */
.interface-method {
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 11px;
  font-weight: 600;
  color: white;
  min-width: 50px;
  text-align: center;
  text-transform: uppercase;
  transition: all 0.2s ease;
}

/* 接口方法颜色 */
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

.method-patch {
  background-color: #909399;
}

/* 接口路径 */
.interface-path {
  font-size: 13px;
  color: #666;
  font-family: 'SF Mono', 'Menlo', 'Monaco', 'Courier New', Courier, monospace;
  flex: 1;
  word-break: break-all;
  line-height: 1.4;
}

/* 接口状态 */
.interface-status {
  margin-left: auto;
}

/* 接口名称 */
.interface-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  line-height: 1.3;
}

/* 接口描述 */
.interface-description {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
  line-height: 1.4;
}

/* Mock状态 */
.mock-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 8px;
  border-top: 1px dashed #eaeaea;
}

.mock-label {
  font-size: 12px;
  color: #666;
}

.mock-status-text {
  font-size: 12px;
  font-weight: 500;
}

.mock-status-text.enabled {
  color: #67c23a;
}

.mock-status-text.disabled {
  color: #909399;
}

/* 滚动条样式 */
.interface-list-container::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.interface-list-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.interface-list-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.interface-list-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 表单元素样式 */
.view-actions .el-select,
.view-actions .el-input {
  border-radius: 4px;
  overflow: hidden;
}

.view-actions .el-select >>> .el-input__inner,
.view-actions .el-input >>> .el-input__inner {
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  padding: 6px 12px;
  font-size: 13px;
  transition: all 0.3s ease;
}

.view-actions .el-select >>> .el-input__inner:hover,
.view-actions .el-input >>> .el-input__inner:hover {
  border-color: #c6e2ff;
}

.view-actions .el-select >>> .el-input__inner:focus,
.view-actions .el-input >>> .el-input__inner:focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
  outline: none;
}

/* 按钮样式 */
.mock-toggle .el-button {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 4px;
}

/* 标签样式 */
.interface-item .el-tag {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
}

/* 开关样式 */
.mock-toggle .el-switch,
.mock-status .el-switch {
  font-size: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .interface-list-view {
    padding: 12px;
  }
  
  .view-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .view-actions {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .interface-stats {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .mock-toggle {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .interface-item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .interface-path {
    width: 100%;
  }
  
  .interface-status {
    margin-left: 0;
    align-self: flex-start;
  }
  
  .mock-status {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>