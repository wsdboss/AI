## 问题分析
发送请求tab页面没有看到请求完整路径，可能的原因包括：
1. 当切换到发送请求tab时，没有触发`updateRequestUrl`方法
2. `currentInterface.path`可能为空或未正确设置
3. 缺少tab切换时的事件处理

## 修复方案

### 1. 添加tab切换事件处理
在`el-tabs`组件中添加`tab-click`事件监听器，当切换到发送请求tab时，重新调用`updateRequestUrl`方法。

### 2. 增强`updateRequestUrl`方法的健壮性
- 检查`currentInterface.path`是否存在，确保生成有效的请求URL
- 添加调试信息，方便查看当前状态

### 3. 添加默认值和错误处理
- 当`currentInterface`或`currentInterface.path`为空时，显示适当的提示信息
- 确保请求路径输入框始终有值显示

## 具体修改

1. **修改模板中的`el-tabs`组件**
   - 添加`@tab-click`事件监听器

2. **添加`handleTabClick`方法**
   - 处理tab切换事件
   - 当切换到发送请求tab时，调用`updateRequestUrl`

3. **优化`updateRequestUrl`方法**
   - 添加条件检查，确保`currentInterface`和`currentInterface.path`存在
   - 添加调试日志

4. **确保请求路径始终有值**
   - 当路径为空时，显示默认提示
   - 增强用户体验

## 预期效果
- 当切换到发送请求tab时，自动生成并显示完整的请求URL
- 即使在特殊情况下，也能显示适当的提示信息
- 提高代码的健壮性和用户体验