<template>
  <div class="min-h-screen bg-blue-600 p-4">
    <div class="max-w-2xl mx-auto bg-white rounded-lg p-6">
      <h1 class="text-2xl font-bold mb-4">体检报告解读结果</h1>
      
      <!-- 加载状态 -->
      <div v-if="!displayedText" class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-2 text-gray-600">正在解读报告，请稍候...</span>
      </div>

      <!-- 错误状态 -->
      <div v-if="error" class="text-red-600 py-4">
        {{ error }}
      </div>

      <!-- 结果展示 -->
      <div v-if="displayedText" class="whitespace-pre-wrap font-mono">
        {{ displayedText }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const error = ref('')
const displayedText = ref('')
let eventSource = null

onMounted(() => {
  // 创建 EventSource 连接
  eventSource = new EventSource('/api/stream-report')

  // 监听消息
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (data.result) {
        displayedText.value += data.result
      }
      // 如果是最后一条消息，关闭连接
      if (data.is_end) {
        eventSource.close()
      }
    } catch (e) {
      console.error('Error parsing message:', e)
    }
  }

  // 监听错误
  eventSource.onerror = (event) => {
    error.value = '连接中断，请刷新页面重试'
    eventSource.close()
  }
})

// 组件卸载时关闭连接
onUnmounted(() => {
  if (eventSource) {
    eventSource.close()
  }
})
</script> 