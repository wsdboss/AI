## 问题分析
1. **前端问题**：WebSocket连接在Vue实例创建前就初始化，可能导致连接过早建立
2. **配置缺失**：缺少关键的pingTimeout和pingInterval配置，影响连接保持
3. **后端问题**：SocketIO自动选择的async_mode可能不适合当前环境
4. **错误处理**：缺少详细的错误日志和处理机制

## 修复方案

### 1. 前端修复（socketService.js）
- 添加pingTimeout和pingInterval配置，确保连接保持活跃
- 调整重连策略，增加最大重连次数
- 增强错误处理机制

### 2. 后端修复（simple_app.py）
- 明确指定SocketIO的async_mode，确保在打包环境中正常工作
- 添加更多的WebSocket连接日志
- 优化SocketIO初始化错误处理

### 3. 初始化时机调整（main.js）
- 考虑调整WebSocket初始化时机，确保在应用完全准备好后再建立连接

### 4. 配置优化
- 确保前后端配置一致，特别是超时和重连参数

## 修复步骤
1. 修改前端socketService.js，添加ping参数和优化重连策略
2. 修改后端simple_app.py，明确指定async_mode
3. 测试WebSocket连接，验证修复效果
4. 添加更多日志，便于后续调试

## 预期效果
- 减少WebSocket连接超时问题
- 提高连接稳定性
- 增强错误处理和日志记录
- 确保在打包环境中正常工作