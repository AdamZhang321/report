<template>
  <!-- 整体容器：最小高度为屏幕高度，蓝色背景，内边距4，子元素间距6，添加适当的顶部间距 pt-4 -->
  <div class="min-h-screen bg-blue-600 px-4 pb-4 pt-4 space-y-6">
    <!-- 头部区域：包含标题和图片 -->
    <div class="flex justify-between items-start max-w-2xl mx-auto">
      <!-- 左侧文字区域 -->
      <div class="space-y-4" style="margin-left: 2px;">
        <!-- 主标题 -->
        <h1 class="text-3xl font-bold text-white">报告解读助手</h1>
        <!-- 特点标签区域 -->
        <div class="flex gap-4">
          <!-- "专业可靠"标签 -->
          <div class="flex items-center gap-2 text-white">
            <div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center">✓</div>
            <span class="text-sm">专业可靠</span>
          </div>
          <!-- "隐私保护"标签 -->
          <div class="flex items-center gap-2 text-white">
            <div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center">✓</div>
            <span class="text-sm">隐私保护</span>
          </div>
        </div>
        <!-- 描述文字 -->
        <p class="text-sm text-white/90">上传体检报告，获得专业、个性化的健康管理建议</p>
      </div>
      <!-- 右侧图片区域 -->
      <div class="relative w-[80%] h-auto">
        <img src="/images/girl.png" alt="Medical assistant illustration" class="object-contain image_2 pos" />
      </div>
    </div>

    <!-- 核心功能区域 -->
    <div class="max-w-2xl mx-auto bg-white rounded-lg p-6 relative z-10">
      <!-- <div class="text-center text-blue-600 font-medium mb-4 text-lg">核心功能</div> -->
      <div class="grid grid-cols-3 gap-4">
        <!-- 循环渲染每个功能项 -->
        <div v-for="feature in features" :key="feature.title" class="flex flex-col items-center gap-2">
          <!-- 功能图标 -->
          <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center">
            <component :is="feature.icon" class="w-8 h-8 text-blue-600" />
          </div>
          <!-- 功能标题和描述 -->
          <div class="text-center">
            <div v-html="feature.title"></div>
            <div class="text-sm text-gray-500">{{ feature.subtitle }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ常见问题区域 -->
    <div class="max-w-2xl mx-auto bg-white rounded-lg p-4">
      <div class="text-center text-blue-600 font-medium mb-3 text-lg">常见问题</div>
      <!-- FAQ列表 -->
      <div class="space-y-3">
        <div v-for="faq in faqs" :key="faq.question">
          <h3 class="text-blue-600 font-medium">{{ faq.question }}</h3>
          <p class="text-gray-600 mt-1">{{ faq.answer }}</p>
        </div>
      </div>
    </div>

    <!-- 底部区域：包含隐私协议和上传按钮 -->
    <div class="max-w-2xl mx-auto space-y-4">
      <!-- 隐私协议勾选框 -->
      <div class="flex items-center text-left">
        <input type="checkbox" id="terms" v-model="agreed" class="rounded" />
        <label for="terms" class="text-white text-sm ml-2">勾选即同意《报告解读助手隐私协议》</label>
      </div>
      <!-- 隐藏的文件输入框 -->
      <input
        type="file"
        ref="fileInput"
        accept=".pdf"
        class="hidden"
        @change="handleFileChange"
      />
      <!-- 上传按钮 -->
      <button
        class="w-full bg-white text-blue-600 hover:bg-white/90 py-3 rounded-lg font-medium"
        :disabled="uploading"
        @click="handleUpload"
      >
        {{ uploading ? '正在上传...' : '上传报告' }}
      </button>
    </div>
  </div>
</template>

<script setup>
// 导入所需的Vue组件和图标
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Upload, FileText, Lightbulb } from 'lucide-vue-next'

// 初始化路由器和响应式变量
const router = useRouter()
const fileInput = ref(null)  // 文件输入框引用
const agreed = ref(false)    // 是否同意隐私协议
const uploading = ref(false) // 是否正在上传

// 定义核心功能数据
const features = [
  { icon: Upload, title: '一键上传<br>体检报告' },
  { icon: FileText, title: 'AI智能解读<br>报告结果' },
  { icon: Lightbulb, title: '生成健康<br>管理建议' }
]

// 定义FAQ数据
const faqs = [
  {
    question: '如何上传体检报告？',
    answer: '您可以通过上传PDF文件的方式上传体检报告，上传后系统将自动识别并进行解读。'
  },
  {
    question: '解读报告需要多长时间?',
    answer: '一般情况下，上传报告后几分钟内即可收到解读结果。'
  },
  {
    question: '我的数据是否安全？',
    answer: '我们非常重视您的隐私，所有体检数据都将经过严格加密并保密处理，保证您的信息不会外泄。'
  }
]

// 处理上传按钮点击事件
const handleUpload = () => {
  if (!agreed.value) {
    alert('请先同意隐私协议')
    return
  }
  fileInput.value.click() // 触发隐藏的文件输入框
}

// 处理文件选择变更事件
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file || file.type !== 'application/pdf') {
    alert('请选择PDF文件')
    return
  }

  uploading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    // 先上传文件获取 reportId
    const response = await fetch('/api/uploadReport', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('上传失败')
    }

    // 跳转到结果页面并传递 reportId
    router.push({
      name: 'Result',
      query: { timestamp: Date.now() } // 添加时间戳确保每次都是新的连接
    })
    
  } catch (error) {
    console.error('Upload failed:', error)
    alert('上传失败，请重试')
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
/* 设置图片尺寸 */
.image_2 {
  width: 154px;
  height: 261px;
}

/* 设置图片位置 */
.pos {
  position: absolute;
  right: 0px;
  top: 0px;
}
</style> 