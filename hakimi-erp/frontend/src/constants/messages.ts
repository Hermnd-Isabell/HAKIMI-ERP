// Standardized message templates.
// Format: [operation] + [result] + [suggestion]

export function createSuccess(entityName: string, nextStep?: string): string {
  const suggestion = nextStep ? `，${nextStep}` : ''
  return `${entityName}创建成功${suggestion}`
}

export function saveSuccess(entityName: string): string {
  return `${entityName}保存成功`
}

export function updateSuccess(entityName: string): string {
  return `${entityName}更新成功`
}

export function deleteSuccess(entityName: string): string {
  return `${entityName}已取消/作废` // Business documents are never physically deleted.
}

export function submitSuccess(entityName: string): string {
  return `${entityName}提交成功`
}

export function operationFailed(operation: string, reason?: string): string {
  const detail = reason ? `：${reason}` : ''
  return `${operation}失败${detail}，请稍后重试或联系管理员`
}

export function validationFailed(count: number): string {
  return `存在 ${count} 条数据校验不通过，请修正后提交`
}

export function fetchFailed(entityName: string): string {
  return `${entityName}数据加载失败，请刷新重试`
}

export function confirmCancel(entityName: string): string {
  return `确定要作废该${entityName}吗？此操作不可恢复`
}
