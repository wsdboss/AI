import io from 'socket.io-client'
import axios from 'axios'

class SocketService {
  constructor() {
    this.socket = null
    this.isConnected = false
    this.eventHandlers = {}
    this.websocketAvailable = null // WebSocket服务可用性状态
    this.initializationAttempted = false // 是否已尝试初始化
    this.initTimeout = null // 初始化超时计时器
  }

  // 检查WebSocket服务可用性
  async checkWebSocketAvailability() {
    try {
      const response = await axios.get('/api/websocket-status', {
        timeout: 5000 // 5秒超时
      })
      return response.data.available
    } catch (error) {
      console.warn('WebSocket状态检查失败:', error)
      return false
    }
  }

  // 初始化连接，添加可用性检测
  async init() {
    // 如果已经尝试初始化，直接返回
    if (this.initializationAttempted) {
      return
    }
    this.initializationAttempted = true

    console.log('开始初始化WebSocket服务...')
    
    // 首先检查WebSocket服务是否可用
    try {
      this.websocketAvailable = await this.checkWebSocketAvailability()
      
      if (!this.websocketAvailable) {
        console.warn('WebSocket服务不可用，将使用HTTP API作为备选方案')
        this.emitEvent('websocket_unavailable')
        return
      }
      
      console.log('WebSocket服务可用，开始建立连接...')
      
      // 获取当前页面的协议和主机，用于构建WebSocket URL
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = window.location.host
      const url = `${protocol}//${host}`

      this.socket = io(url, {
        path: '/socket.io',
        transports: ['websocket', 'polling'],
        timeout: 30000, // 增加超时时间到30秒
        reconnection: true, // 启用自动重连
        reconnectionAttempts: 5, // 减少重连尝试次数，避免大量错误日志
        reconnectionDelay: 3000, // 增加重连延迟到3秒
        reconnectionDelayMax: 30000, // 最大重连延迟30秒
        randomizationFactor: 0.5, // 重连延迟随机因子
        pingTimeout: 60000, // 心跳超时时间60秒
        pingInterval: 25000 // 心跳发送间隔25秒
      })

      // 连接成功事件
      this.socket.on('connect', () => {
        console.log('WebSocket连接成功')
        this.isConnected = true
        this.emitEvent('connect')
      })

      // 连接断开事件
      this.socket.on('disconnect', (reason) => {
        console.log('WebSocket连接断开，原因:', reason)
        this.isConnected = false
        this.emitEvent('disconnect', { reason })
      })

      // 连接错误事件
      this.socket.on('connect_error', (error) => {
        console.error('WebSocket连接错误:', error)
        // 只在控制台打印，不发送到UI，避免用户看到过多错误信息
        // this.emitEvent('error', error)
      })

      // 重连尝试事件
      this.socket.on('reconnect_attempt', (attemptNumber) => {
        console.log(`WebSocket正在尝试重连，第${attemptNumber}次`)
        // 只在控制台打印，不发送到UI
      })

      // 重连成功事件
      this.socket.on('reconnect', (attemptNumber) => {
        console.log(`WebSocket重连成功，共尝试${attemptNumber}次`)
        this.isConnected = true
        this.emitEvent('reconnect', { attemptNumber })
      })

      // 重连失败事件
      this.socket.on('reconnect_failed', () => {
        console.error('WebSocket重连失败')
        this.emitEvent('reconnect_failed')
        // 重连失败后，标记服务不可用
        this.websocketAvailable = false
        this.emitEvent('websocket_unavailable')
      })

      // 接收接口列表响应
      this.socket.on('interfaces_response', (data) => {
        this.emitEvent('interfaces_response', data)
      })

      // 接收动态接口响应
      this.socket.on('dynamic_response', (data) => {
        this.emitEvent('dynamic_response', data)
      })

      // 接收错误响应
      this.socket.on('error', (data) => {
        this.emitEvent('error', data)
      })

      // 接收连接响应
      this.socket.on('connection_response', (data) => {
        this.emitEvent('connection_response', data)
      })
      
      console.log('WebSocket服务初始化完成')
    } catch (error) {
      console.error('WebSocket初始化失败:', error)
      this.emitEvent('websocket_unavailable')
    }
  }

  // 发送消息，添加错误处理
  emit(event, data) {
    if (this.isConnected && this.socket) {
      this.socket.emit(event, data)
    } else {
      console.error('WebSocket未连接，无法发送消息')
      this.emitEvent('send_error', { event, data, message: 'WebSocket未连接，无法发送消息' })
    }
  }

  // 注册事件监听器
  on(event, callback) {
    if (!this.eventHandlers[event]) {
      this.eventHandlers[event] = []
    }
    this.eventHandlers[event].push(callback)
  }

  // 取消事件监听器
  off(event, callback) {
    if (this.eventHandlers[event]) {
      this.eventHandlers[event] = this.eventHandlers[event].filter(handler => handler !== callback)
    }
  }

  // 触发事件监听器
  emitEvent(event, data) {
    if (this.eventHandlers[event]) {
      this.eventHandlers[event].forEach(handler => {
        try {
          handler(data)
        } catch (error) {
          console.error(`处理WebSocket事件${event}时出错:`, error)
        }
      })
    }
  }

  // 获取接口列表 - 添加降级处理
  async getInterfaces(fileId = null) {
    // 如果WebSocket可用且已连接，使用WebSocket发送
    if (this.isConnected && this.socket) {
      this.emit('get_interfaces', { file_id: fileId })
    } else {
      // 降级使用HTTP API
      console.warn('WebSocket未连接，使用HTTP API获取接口列表')
      try {
        const response = await axios.get('/api/interfaces', {
          params: fileId ? { file_id: fileId } : {}
        })
        this.emitEvent('interfaces_response', { interfaces: response.data })
      } catch (error) {
        console.error('HTTP API获取接口列表失败:', error)
        this.emitEvent('error', { message: '获取接口列表失败' })
      }
    }
  }

  // 调用动态接口 - 添加降级处理
  async callDynamicInterface(path, method = 'GET', params = {}) {
    // 如果WebSocket可用且已连接，使用WebSocket发送
    if (this.isConnected && this.socket) {
      this.emit('dynamic_interface', {
        path,
        method,
        params
      })
    } else {
      // 降级使用HTTP API
      console.warn('WebSocket未连接，使用HTTP API调用动态接口')
      try {
        const response = await axios({
          url: `/api/dynamic${path}`,
          method: method,
          data: { params }
        })
        this.emitEvent('dynamic_response', response.data)
      } catch (error) {
        console.error('HTTP API调用动态接口失败:', error)
        this.emitEvent('error', { message: '调用接口失败' })
      }
    }
  }

  // 关闭连接
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
    this.isConnected = false
    this.eventHandlers = {}
    this.initializationAttempted = false // 重置初始化标志，允许重新初始化
  }

  // 检查连接状态
  getConnectionStatus() {
    return this.isConnected
  }

  // 获取WebSocket服务可用性状态
  getWebSocketAvailability() {
    return this.websocketAvailable
  }

  // 重新初始化连接
  async reinitialize() {
    this.disconnect()
    this.initializationAttempted = false
    await this.init()
  }
}

// 导出单例实例
export default new SocketService()