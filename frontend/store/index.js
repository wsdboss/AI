import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 文件相关状态
    files: [],
    currentFile: null,
    
    // 接口相关状态
    interfaces: [],
    currentInterface: null,
    
    // 请求日志相关状态
    requestLogs: [],
    
    // Mock配置相关状态
    mockConfig: null
  },
  
  getters: {
    // 获取文件列表
    getFiles: state => state.files,
    // 获取当前文件
    getCurrentFile: state => state.currentFile,
    // 获取接口列表
    getInterfaces: state => state.interfaces,
    // 获取当前接口
    getCurrentInterface: state => state.currentInterface,
    // 获取请求日志
    getRequestLogs: state => state.requestLogs,
    // 获取Mock配置
    getMockConfig: state => state.mockConfig
  },
  
  mutations: {
    // 设置文件列表
    SET_FILES(state, files) {
      state.files = files
    },
    // 设置当前文件
    SET_CURRENT_FILE(state, file) {
      state.currentFile = file
    },
    // 添加文件
    ADD_FILE(state, file) {
      state.files.push(file)
    },
    // 设置接口列表
    SET_INTERFACES(state, interfaces) {
      // 确保interfaces是数组类型
      state.interfaces = Array.isArray(interfaces) ? interfaces : []
    },
    // 设置当前接口
    SET_CURRENT_INTERFACE(state, intf) {
      state.currentInterface = intf
    },
    // 添加接口
    ADD_INTERFACE(state, intf) {
      state.interfaces.push(intf)
    },
    // 设置请求日志
    SET_REQUEST_LOGS(state, logs) {
      state.requestLogs = logs
    },
    // 添加请求日志
    ADD_REQUEST_LOG(state, log) {
      state.requestLogs.unshift(log) // 最新的日志放在前面
    },
    // 设置Mock配置
    SET_MOCK_CONFIG(state, config) {
      state.mockConfig = config
    }
  },
  
  actions: {
    // 加载文件列表
    async loadFiles({ commit }) {
      try {
        // 移除/api前缀，因为axios.defaults.baseURL已经配置了/api
        const response = await this._vm.$axios.get('/files')
        commit('SET_FILES', response.data)
      } catch (error) {
        console.error('加载文件列表失败:', error)
      }
    },
    
    // 加载接口列表
    async loadInterfaces({ commit }, fileId = null) {
      try {
        // 移除/api前缀，因为axios.defaults.baseURL已经配置了/api
        const url = fileId ? `/interfaces?file_id=${fileId}` : '/interfaces'
        console.log('发送请求:', url)
        const response = await this._vm.$axios.get(url)
        console.log('响应数据:', response.data)
        commit('SET_INTERFACES', response.data)
      } catch (error) {
        console.error('加载接口列表失败:', error)
        console.error('错误详情:', error.response)
        commit('SET_INTERFACES', [])
      }
    },
    
    // 加载接口详情
    async loadInterfaceDetail({ commit }, interfaceId) {
      try {
        // 接口详情直接使用当前接口数据，不需要单独请求
        // 这里可以根据实际需求添加接口详情请求
        // const response = await this._vm.$axios.get(`/api/interfaces/${interfaceId}`)
        // commit('SET_CURRENT_INTERFACE', response.data)
      } catch (error) {
        console.error('加载接口详情失败:', error)
      }
    },
    
    // 加载请求日志
    async loadRequestLogs({ commit }, interfaceId = null) {
      try {
        // 日志功能尚未实现，暂时返回空数组
        commit('SET_REQUEST_LOGS', [])
        // const url = interfaceId ? `/api/logs?interface_id=${interfaceId}` : '/api/logs'
        // const response = await this._vm.$axios.get(url)
        // commit('SET_REQUEST_LOGS', response.data)
      } catch (error) {
        console.error('加载请求日志失败:', error)
      }
    },
    
    // 加载Mock配置
    async loadMockConfig({ commit }, interfaceId) {
      try {
        // Mock配置功能使用已有接口数据，不需要单独请求
        commit('SET_MOCK_CONFIG', null)
        // const response = await this._vm.$axios.get(`/api/interfaces/${interfaceId}/mock-config`)
        // commit('SET_MOCK_CONFIG', response.data)
      } catch (error) {
        console.error('加载Mock配置失败:', error)
      }
    }
  },
  
  modules: {
    // 可以添加子模块
  }
})