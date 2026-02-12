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
              <el-descriptions-item label="请求方式">
                <div style="display: flex; align-items: center;">
                  <el-select v-model="interfaceMethod" size="small" @change="handleMethodChange" style="width: 120px; margin-right: 10px;">
                    <el-option label="GET" value="GET"></el-option>
                    <el-option label="POST" value="POST"></el-option>
                  </el-select>
                  <el-button type="primary" size="small" @click="saveInterfaceMethod" :loading="savingMethod">
                    保存
                  </el-button>
                </div>
              </el-descriptions-item>
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
            <div class="section-header" style="margin-bottom: 16px;">
              <h4>请求参数列表</h4>
            </div>
            
            <el-table :data="interfaceParams" stripe style="width: 100%" v-if="interfaceParams.length > 0" @cell-dblclick="handleCellDblClick">
              <el-table-column prop="name" label="参数名" width="150">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">{{ scope.row.name }}</span>
                  <el-input v-else v-model="scope.row.name" size="small" style="width: 120px;"></el-input>
                </template>
              </el-table-column>
              <el-table-column prop="param_type" label="参数类型" width="150">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">{{ scope.row.param_type }}</span>
                  <el-select v-else v-model="scope.row.param_type" size="small" style="width: 120px;">
                    <el-option label="string" value="string"></el-option>
                    <el-option label="int" value="int"></el-option>
                    <el-option label="boolean" value="boolean"></el-option>
                    <el-option label="double" value="double"></el-option>
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column prop="required" label="是否必填" width="100">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">
                    <el-tag type="success" v-if="scope.row.required">必填</el-tag>
                    <el-tag type="info" v-else>可选</el-tag>
                  </span>
                  <el-switch v-else v-model="scope.row.required" size="small"></el-switch>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="描述">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">{{ scope.row.description || '' }}</span>
                  <el-input v-else v-model="scope.row.description" size="small" type="textarea"></el-input>
                </template>
              </el-table-column>
              <el-table-column prop="example" label="示例值">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">{{ scope.row.example || '' }}</span>
                  <el-input v-else v-model="scope.row.example" size="small"></el-input>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="250" fixed="right">
                <template slot-scope="scope">
                  <template v-if="!scope.row.editing">
                    <el-button type="primary" size="small" @click="handleEditParamField(scope.row)" style="margin-right: 10px;">
                      <i class="el-icon-edit"></i> 编辑
                    </el-button>
                    <el-button type="success" size="small" @click="handleAddParamField(scope.$index)" style="margin-right: 10px;">
                      <i class="el-icon-plus"></i> 新增
                    </el-button>
                    <el-button type="danger" size="small" @click="handleDeleteParamField(scope.row.id)">
                      <i class="el-icon-delete"></i> 删除
                    </el-button>
                  </template>
                  <template v-else>
                    <el-button type="success" size="small" @click="handleSaveParamField(scope.row)" style="margin-right: 10px;">
                      <i class="el-icon-check"></i> 保存
                    </el-button>
                    <el-button type="warning" size="small" @click="handleCancelEditParam(scope.row)">
                      <i class="el-icon-close"></i> 取消
                    </el-button>
                  </template>
                </template>
              </el-table-column>
            </el-table>
            <el-empty description="暂无请求参数" v-else>
              <el-button type="primary" @click="handleAddParamField()">
                <i class="el-icon-plus"></i> 添加参数
              </el-button>
            </el-empty>
          </div>
        </el-tab-pane>
        
        <!-- 响应参数 -->
        <el-tab-pane label="响应参数" name="responses">
          <div class="detail-section">
            <div class="section-header" style="margin-bottom: 16px;">
              <h4>响应参数列表</h4>
            </div>
            
            <el-table :data="interfaceResponses" stripe style="width: 100%" v-if="interfaceResponses.length > 0" @cell-dblclick="handleCellDblClick">
              <el-table-column prop="name" label="字段名" width="150">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">{{ scope.row.name }}</span>
                  <el-input v-else v-model="scope.row.name" size="small" style="width: 120px;"></el-input>
                </template>
              </el-table-column>
              <el-table-column prop="response_type" label="字段类型" width="150">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">{{ scope.row.response_type }}</span>
                  <el-select v-else v-model="scope.row.response_type" size="small" style="width: 120px;">
                    <el-option label="string" value="string"></el-option>
                    <el-option label="int" value="int"></el-option>
                    <el-option label="boolean" value="boolean"></el-option>
                    <el-option label="double" value="double"></el-option>
                    <el-option label="object" value="object"></el-option>
                    <el-option label="array" value="array"></el-option>
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="描述">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">{{ scope.row.description || '' }}</span>
                  <el-input v-else v-model="scope.row.description" size="small" type="textarea"></el-input>
                </template>
              </el-table-column>
              <el-table-column prop="example" label="示例值">
                <template slot-scope="scope">
                  <span v-if="!scope.row.editing">{{ scope.row.example || '' }}</span>
                  <el-input v-else v-model="scope.row.example" size="small"></el-input>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="250" fixed="right">
                <template slot-scope="scope">
                  <template v-if="!scope.row.editing">
                    <el-button type="primary" size="small" @click="handleEditField(scope.row)" style="margin-right: 10px;">
                      <i class="el-icon-edit"></i> 编辑
                    </el-button>
                    <el-button type="success" size="small" @click="handleAddField(scope.$index)" style="margin-right: 10px;">
                      <i class="el-icon-plus"></i> 新增
                    </el-button>
                    <el-button type="danger" size="small" @click="handleDeleteField(scope.row.id)">
                      <i class="el-icon-delete"></i> 删除
                    </el-button>
                  </template>
                  <template v-else>
                    <el-button type="success" size="small" @click="handleSaveField(scope.row)" style="margin-right: 10px;">
                      <i class="el-icon-check"></i> 保存
                    </el-button>
                    <el-button type="warning" size="small" @click="handleCancelEdit(scope.row)">
                      <i class="el-icon-close"></i> 取消
                    </el-button>
                  </template>
                </template>
              </el-table-column>
            </el-table>
            <el-empty description="暂无响应参数" v-else>
              <el-button type="primary" @click="handleAddField()">
                <i class="el-icon-plus"></i> 添加字段
              </el-button>
            </el-empty>
            
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
        
        <!-- 请求日志 -->
        <el-tab-pane label="请求日志" name="logs">
          <div class="detail-section">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
              <h4>请求日志记录</h4>
              <div style="display: flex; align-items: center;">
                <span style="margin-right: 10px;">展示条数：</span>
                <el-select v-model="logLimit" size="small" @change="handleLogLimitChange">
                  <el-option label="10条" value="10"></el-option>
                  <el-option label="100条" value="100"></el-option>
                  <el-option label="500条" value="500"></el-option>
                  <el-option label="1000条" value="1000"></el-option>
                </el-select>
              </div>
            </div>
            <el-divider></el-divider>
            <div class="log-list" v-if="requestLogs.length > 0">
              <div 
                v-for="log in requestLogs" 
                :key="log.id" 
                class="log-item"
              >
                <div class="log-header">
                  <span class="log-method" :class="'method-' + log.method.toLowerCase()">
                    {{ log.method }}
                  </span>
                  <span class="log-path">{{ log.path }}</span>
                  <span class="log-time">{{ log.request_time }}</span>
                </div>
                <div class="log-content">
                  <div><strong>请求参数：</strong>{{ log.params || '无' }}</div>
                  <div><strong>响应状态：</strong>{{ log.response_status }}</div>
                  <div><strong>执行时间：</strong>{{ log.execution_time || '未知' }}ms</div>
                  <div v-if="log.response_body" style="margin-top: 5px;">
                    <strong>响应内容：</strong>
                    <pre>{{ log.response_body }}</pre>
                  </div>
                </div>
              </div>
            </div>
            <el-empty description="暂无请求日志记录" v-else></el-empty>
          </div>
        </el-tab-pane>
        
        <!-- HTTP请求发送 -->
        <el-tab-pane label="HTTP请求发送" name="request-send">
          <div class="detail-section">
            <!-- HTTP请求内容 -->
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
                <el-input-number v-model="requestForm.mock_count" :min="1" :max="1000" :step="1"></el-input-number>
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
  
  <!-- 添加/编辑响应字段对话框 -->
  <el-dialog
    :title="dialogTitle"
    :visible.sync="dialogVisible"
    width="500px"
  >
    <el-form :model="fieldForm" label-width="100px">
      <el-form-item label="字段名" required>
        <el-input v-model="fieldForm.name" placeholder="请输入字段名"></el-input>
      </el-form-item>
      <el-form-item label="字段类型" required>
        <el-select v-model="fieldForm.response_type" placeholder="请选择字段类型">
          <el-option label="string" value="string"></el-option>
          <el-option label="int" value="int"></el-option>
          <el-option label="boolean" value="boolean"></el-option>
          <el-option label="double" value="double"></el-option>
          <el-option label="object" value="object"></el-option>
          <el-option label="array" value="array"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="描述">
        <el-input type="textarea" v-model="fieldForm.description" placeholder="请输入描述"></el-input>
      </el-form-item>
      <el-form-item label="示例值">
        <el-input v-model="fieldForm.example" placeholder="请输入示例值"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="saveField" :loading="savingField">保存</el-button>
    </span>
  </el-dialog>
  
  <!-- 添加/编辑请求参数对话框 -->
  <el-dialog
    :title="paramDialogTitle"
    :visible.sync="paramDialogVisible"
    width="500px"
  >
    <el-form :model="paramForm" label-width="100px">
      <el-form-item label="参数名" required>
        <el-input v-model="paramForm.name" placeholder="请输入参数名"></el-input>
      </el-form-item>
      <el-form-item label="参数类型" required>
        <el-select v-model="paramForm.param_type" placeholder="请选择参数类型">
          <el-option label="string" value="string"></el-option>
          <el-option label="int" value="int"></el-option>
          <el-option label="boolean" value="boolean"></el-option>
          <el-option label="double" value="double"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="是否必填">
        <el-switch v-model="paramForm.required"></el-switch>
      </el-form-item>
      <el-form-item label="描述">
        <el-input type="textarea" v-model="paramForm.description" placeholder="请输入描述"></el-input>
      </el-form-item>
      <el-form-item label="示例值">
        <el-input v-model="paramForm.example" placeholder="请输入示例值"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="paramDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="saveParamField" :loading="savingParamField">保存</el-button>
    </span>
  </el-dialog>
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
      interfaceMethod: 'GET',
      savingMethod: false,
      // 响应字段编辑相关
      dialogVisible: false,
      dialogTitle: '添加响应字段',
      fieldForm: {
        id: 0,
        name: '',
        response_type: 'string',
        description: '',
        example: ''
      },
      savingField: false,
      
      // 请求参数编辑相关
      paramDialogVisible: false,
      paramDialogTitle: '添加请求参数',
      paramForm: {
        id: 0,
        name: '',
        param_type: 'string',
        required: true,
        description: '',
        example: ''
      },
      savingParamField: false,

      requestForm: {
        params: '{}',
        mock_count: 10
      },
      // 请求日志相关
      logLimit: '10'
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
          // 加载请求日志
          this.$store.dispatch('loadRequestLogs', {
            interfaceId: newInterface.id,
            limit: this.logLimit
          })
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
        if (newInterface) {
          this.interfaceMethod = newInterface.method
        } else {
          this.interfaceMethod = 'GET'
        }
      },
      deep: true
    },
    // 当请求参数变化时，更新HTTP请求发送表单中的请求参数
    interfaceParams: {
      handler(newParams) {
        if (newParams && newParams.length > 0) {
          const defaultParams = {}
          newParams.forEach(param => {
            // 根据参数类型设置默认值
            let defaultValue = ''
            switch (param.param_type) {
              case 'int':
              case 'long':
                defaultValue = 0
                break
              case 'boolean':
                defaultValue = false
                break
              case 'double':
              case 'float':
                defaultValue = 0.0
                break
              case 'object':
                defaultValue = {}
                break
              case 'array':
                defaultValue = []
                break
              default:
                defaultValue = ''
            }
            defaultParams[param.name] = defaultValue
          })
          this.requestForm.params = JSON.stringify(defaultParams, null, 2)
        } else {
          // 如果没有请求参数，设置为空对象
          this.requestForm.params = '{}'
        }
      },
      deep: true
    }
  },
  
  computed: {
    // 从Vuex store中获取请求日志
    requestLogs() {
      return this.$store.getters.getRequestLogs || []
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
        // 为每个参数添加editing属性，确保响应式
        this.interfaceParams = paramsResponse.data.map(param => ({
          ...param,
          editing: false
        }))
        
        // 自动填充请求参数到HTTP请求发送表单
        if (this.interfaceParams.length > 0) {
          const defaultParams = {}
          this.interfaceParams.forEach(param => {
            // 根据参数类型设置默认值
            let defaultValue = ''
            switch (param.param_type) {
              case 'int':
              case 'long':
                defaultValue = 0
                break
              case 'boolean':
                defaultValue = false
                break
              case 'double':
              case 'float':
                defaultValue = 0.0
                break
              case 'object':
                defaultValue = {}
                break
              case 'array':
                defaultValue = []
                break
              default:
                defaultValue = ''
            }
            defaultParams[param.name] = defaultValue
          })
          this.requestForm.params = JSON.stringify(defaultParams, null, 2)
        } else {
          // 如果没有请求参数，设置为空对象
          this.requestForm.params = '{}'
        }
        
        // 加载接口响应字段
        const responsesResponse = await this.$axios.get(`/interfaces/${interfaceId}/responses`)
        // 为每个字段添加editing属性，确保响应式
        this.interfaceResponses = responsesResponse.data.map(field => ({
          ...field,
          editing: false
        }))
        
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
        
        // 重新加载请求日志，确保显示最新的请求记录
        this.$store.dispatch('loadRequestLogs', this.currentInterface.id)
        
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
      if (tab.name === 'request-send') {
        this.updateRequestUrl()
      }
    },
    
    // 更新请求URL并检查浏览器支持
    updateRequestUrl() {
      if (this.currentInterface && this.currentInterface.path) {
        // 生成完整的请求URL，包含/api前缀
        const baseUrl = window.location.origin
        this.requestUrl = `${baseUrl}/dynamic${this.currentInterface.path}`
        
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
    },
    
    // 处理接口调用方式变更
    handleMethodChange() {
      console.log('接口调用方式变更为:', this.interfaceMethod)
    },
    
    // 保存接口调用方式
    async saveInterfaceMethod() {
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      try {
        this.savingMethod = true
        
        // 调用后端API更新接口调用方式
        const response = await this.$axios.post(`/interfaces/update-method/${this.currentInterface.id}`, {
          method: this.interfaceMethod
        })
        
        this.$message.success('接口调用方式更新成功')
        
        // 更新当前接口的method属性（使用大写形式）
        this.currentInterface.method = this.interfaceMethod.toUpperCase()
        
        // 更新Vuex中的接口信息
        this.$store.commit('SET_CURRENT_INTERFACE', this.currentInterface)
        
        // 重新加载接口列表，确保其他组件也能看到更新
        this.$store.dispatch('loadInterfaces', this.currentFile?.id)
        
      } catch (error) {
        this.$message.error(`接口调用方式更新失败: ${error.response?.data?.message || error.message}`)
        console.error('接口调用方式更新失败:', error)
        // 恢复原来的调用方式
        this.interfaceMethod = this.currentInterface.method
      } finally {
        this.savingMethod = false
      }
    },
    
    // 处理添加字段
    handleAddField(index) {
      console.log('点击了添加字段按钮，在索引', index, '下方添加')
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      // 创建新字段对象
      const newField = {
        id: 0,
        name: 'new_field',
        response_type: 'string',
        description: '',
        example: '',
        interface_id: this.currentInterface.id,
        editing: true // 直接进入编辑状态
      }
      
      // 在指定索引下方添加新行
      if (typeof index === 'number') {
        this.interfaceResponses.splice(index + 1, 0, newField)
      } else {
        // 如果没有指定索引，添加到末尾
        this.interfaceResponses.push(newField)
      }
      console.log('添加了新字段并进入编辑状态', newField)
    },
    
    // 处理编辑字段
    handleEditField(row) {
      console.log('点击了编辑字段按钮', row)
      if (!row) {
        console.error('编辑字段时row为null')
        this.$message.error('编辑失败：数据无效')
        return
      }
      // 设置编辑状态
      row.editing = true
      console.log('设置字段为编辑状态', row)
    },
    
    // 保存字段
    async saveField() {
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      if (!this.fieldForm.name || !this.fieldForm.response_type) {
        this.$message.error('字段名和字段类型不能为空')
        return
      }
      
      try {
        this.savingField = true
        
        if (this.fieldForm.id === 0) {
          // 添加新字段
          const response = await this.$axios.post(`/interfaces/${this.currentInterface.id}/responses`, this.fieldForm)
          this.interfaceResponses.push(response.data)
          this.$message.success('字段添加成功')
        } else {
          // 更新字段
          const response = await this.$axios.put(`/interfaces/${this.currentInterface.id}/responses/${this.fieldForm.id}`, this.fieldForm)
          const index = this.interfaceResponses.findIndex(item => item.id === this.fieldForm.id)
          if (index !== -1) {
            this.interfaceResponses[index] = response.data
          }
          this.$message.success('字段更新成功')
        }
        
        this.dialogVisible = false
      } catch (error) {
        console.error('保存字段失败:', error)
        this.$message.error('保存字段失败，请重试')
      } finally {
        this.savingField = false
      }
    },
    
    // 保存字段编辑
    async handleSaveField(row) {
      console.log('保存字段编辑', row)
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      if (!row.name || !row.response_type) {
        this.$message.error('字段名和字段类型不能为空')
        return
      }
      
      try {
        let response
        if (row.id === 0) {
          // 调用后端API创建新字段
          response = await this.$axios.post(`/interfaces/${this.currentInterface.id}/responses`, row)
          // 更新本地数据，替换临时字段
          const index = this.interfaceResponses.findIndex(item => item.id === row.id)
          if (index !== -1) {
            this.interfaceResponses[index] = response.data
          }
          this.$message.success('字段添加成功')
        } else {
          // 调用后端API更新字段
          response = await this.$axios.put(`/interfaces/${this.currentInterface.id}/responses/${row.id}`, row)
          // 更新本地数据
          const index = this.interfaceResponses.findIndex(item => item.id === row.id)
          if (index !== -1) {
            this.interfaceResponses[index] = response.data
          }
          this.$message.success('字段更新成功')
        }
        // 取消编辑状态
        row.editing = false
      } catch (error) {
        console.error('保存字段失败:', error)
        this.$message.error('保存字段失败，请重试')
      }
    },
    
    // 取消字段编辑
    handleCancelEdit(row) {
      console.log('取消字段编辑', row)
      // 取消编辑状态
      row.editing = false
      // 重新加载数据，恢复原始值
      if (this.currentInterface) {
        this.loadInterfaceDetail(this.currentInterface.id)
      }
    },
    
    // 处理删除字段
    async handleDeleteField(fieldId) {
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      try {
        await this.$axios.delete(`/interfaces/${this.currentInterface.id}/responses/${fieldId}`)
        this.interfaceResponses = this.interfaceResponses.filter(item => item.id !== fieldId)
        this.$message.success('字段删除成功')
      } catch (error) {
        console.error('删除字段失败:', error)
        this.$message.error('删除字段失败，请重试')
      }
    },
    
    // 处理添加请求参数
    handleAddParamField(index) {
      console.log('点击了添加请求参数按钮，在索引', index, '下方添加')
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      // 创建新参数对象
      const newParam = {
        id: 0,
        name: 'new_param',
        param_type: 'string',
        required: true,
        description: '',
        example: '',
        interface_id: this.currentInterface.id,
        editing: true // 直接进入编辑状态
      }
      
      // 在指定索引下方添加新行
      if (typeof index === 'number') {
        this.interfaceParams.splice(index + 1, 0, newParam)
      } else {
        // 如果没有指定索引，添加到末尾
        this.interfaceParams.push(newParam)
      }
      console.log('添加了新请求参数并进入编辑状态', newParam)
    },
    
    // 处理编辑请求参数
    handleEditParamField(row) {
      console.log('点击了编辑请求参数按钮', row)
      if (!row) {
        console.error('编辑请求参数时row为null')
        this.$message.error('编辑失败：数据无效')
        return
      }
      // 设置编辑状态
      row.editing = true
      console.log('设置请求参数为编辑状态', row)
    },
    
    // 保存请求参数
    async saveParamField() {
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      if (!this.paramForm.name || !this.paramForm.param_type) {
        this.$message.error('参数名和参数类型不能为空')
        return
      }
      
      try {
        this.savingParamField = true
        
        if (this.paramForm.id === 0) {
          // 添加新参数
          const response = await this.$axios.post(`/interfaces/${this.currentInterface.id}/params`, this.paramForm)
          this.interfaceParams.push(response.data)
          this.$message.success('参数添加成功')
        } else {
          // 更新参数
          const response = await this.$axios.put(`/interfaces/${this.currentInterface.id}/params/${this.paramForm.id}`, this.paramForm)
          const index = this.interfaceParams.findIndex(item => item.id === this.paramForm.id)
          if (index !== -1) {
            this.interfaceParams[index] = response.data
          }
          this.$message.success('参数更新成功')
        }
        
        this.paramDialogVisible = false
      } catch (error) {
        console.error('保存参数失败:', error)
        this.$message.error('保存参数失败，请重试')
      } finally {
        this.savingParamField = false
      }
    },
    
    // 保存请求参数编辑
    async handleSaveParamField(row) {
      console.log('保存请求参数编辑', row)
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      if (!row.name || !row.param_type) {
        this.$message.error('参数名和参数类型不能为空')
        return
      }
      
      try {
        let response
        if (row.id === 0) {
          // 调用后端API创建新参数
          response = await this.$axios.post(`/interfaces/${this.currentInterface.id}/params`, row)
          // 更新本地数据，替换临时参数
          const index = this.interfaceParams.findIndex(item => item.id === row.id)
          if (index !== -1) {
            this.interfaceParams[index] = response.data
          }
          this.$message.success('参数添加成功')
        } else {
          // 调用后端API更新参数
          response = await this.$axios.put(`/interfaces/${this.currentInterface.id}/params/${row.id}`, row)
          // 更新本地数据
          const index = this.interfaceParams.findIndex(item => item.id === row.id)
          if (index !== -1) {
            this.interfaceParams[index] = response.data
          }
          this.$message.success('参数更新成功')
        }
        // 取消编辑状态
        row.editing = false
      } catch (error) {
        console.error('保存参数失败:', error)
        this.$message.error('保存参数失败，请重试')
      }
    },
    
    // 取消请求参数编辑
    handleCancelEditParam(row) {
      console.log('取消请求参数编辑', row)
      // 取消编辑状态
      row.editing = false
      // 重新加载数据，恢复原始值
      if (this.currentInterface) {
        this.loadInterfaceDetail(this.currentInterface.id)
      }
    },
    
    // 处理删除请求参数
    async handleDeleteParamField(paramId) {
      if (!this.currentInterface) {
        this.$message.error('请先选择一个接口')
        return
      }
      
      try {
        await this.$axios.delete(`/interfaces/${this.currentInterface.id}/params/${paramId}`)
        this.interfaceParams = this.interfaceParams.filter(item => item.id !== paramId)
        this.$message.success('参数删除成功')
      } catch (error) {
        console.error('删除参数失败:', error)
        this.$message.error('删除参数失败，请重试')
      }
    },
    
    // 处理表格单元格双击事件
    handleCellDblClick(row, column, cell, event) {
      console.log('双击了表格单元格', row, column)
      if (!row) {
        console.error('双击时row为null')
        return
      }
      // 设置编辑状态
      row.editing = true
      console.log('设置行为编辑状态', row)
    },
    
    // 处理日志展示条数变更
    handleLogLimitChange() {
      if (this.currentInterface) {
        this.$store.dispatch('loadRequestLogs', {
          interfaceId: this.currentInterface.id,
          limit: this.logLimit
        })
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
</style>