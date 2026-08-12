<script setup lang="ts">
import { ref, nextTick} from 'vue'
import { useChatStore } from './stores/chat'
import apiClient from './api/client'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const chatStore = useChatStore()
const userMessage = ref('')
const isProcessing = ref(false)
// template ref for scroll container
const chatMessagesRef = ref<HTMLDivElement | null>(null)

const scrollToBottomSmart = () => {
  if (!chatMessagesRef.value) return
  const el = chatMessagesRef.value
  const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight
  // Only auto-scroll if user is already within 20px of bottom
  const isNearBottom = distanceFromBottom < 20

  if (isNearBottom) {
    el.scrollTop = el.scrollHeight
  }
}

function renderMarkdown(text: string): string {
  const rawHTML = marked.parse(text) as string
  return DOMPurify.sanitize(rawHTML)
}

async function scrollToBottom() {
  await nextTick() // Wait for DOM render after new message
  if (chatMessagesRef.value) {
    chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
  }
}

async function typeWriter(messageId: number, fullText: string, speed = 10) {
  let currentText = ''
  for (const char of fullText) {
    currentText += char
    chatStore.updateAiResponse(messageId, currentText)
    await new Promise(resolve => setTimeout(resolve, speed))

    // Smart auto-scrolling for AI response
    await nextTick(scrollToBottomSmart)
  }
}

async function sendMessage() {
  if (userMessage.value.trim() && !isProcessing.value) {
    const userMsg = userMessage.value
    userMessage.value = ""

    // Add user message to store immdiately
    const newMessage = chatStore.addMessage(userMsg, '')
    const messageId = newMessage.id // Get the ID from the returned message

    isProcessing.value = true

    await scrollToBottom()
    
    try {
      // Call backend API
      const response = await apiClient.post('/chat', {
        message: userMsg
      })
      const aiFullText = response.data.response
      await typeWriter(messageId, aiFullText)

    }catch (error) {
      console.error('Error calling chat API:', error)
      // Update with error message
      chatStore.updateAiResponse(messageId, 'Sorry, there was an error processing your message.')
    } finally {
      isProcessing.value = false
    }
  }
}
</script>

<template>
  <div class="chat-container">
    <!-- Message display area -->
    <div ref="chatMessagesRef" class="chat-messages">
      <div v-for="(message, index) in chatStore.messages" :key="index" class="message">
        <div v-if="message.user" class="user-message">
          <div class="message-bubble">
            <p>{{ message.user }}</p>
          </div>
        </div>
        <div v-if="message.ai" class="ai-message">
          <div class="message-bubble markdown-bubble">
            <div v-html="renderMarkdown(message.ai)"></div>  
          </div>
        </div>
      </div>
    </div>

    <!-- Input area -->
    <div class="chat-input">
      <el-input
        placeholder="Type your message..."
        v-model="userMessage"
        type="textarea"
        :autosize="{ minRows:1, maxRows:4 }"
        @keyup.enter="sendMessage"
      />
      <el-button type="primary" @click="sendMessage" :disabled="isProcessing">
        {{ isProcessing ? "Thinking..." : "Send" }}
      </el-button>
    </div>
  </div>
</template>

<style>
:root {
  --chat-bg: #f5f5f5;
  --bubble-padding: 10px 15px;
  --bubble-margin: 5px;
  --bubble-max-inner-width: 75%;
}

/* Add basic styling for layout */
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Arial', sans-serif;
}
.chat-messages {
  flex: 1;
  overflow-wrap: break-word;
  overflow-y: auto;
  padding: 10px;
  background-color: var(--chat-bg);
}
.chat-input {
  display: flex;
  gap: 10px;
  padding: 15px 20px;
  background-color: var(--chat-bg);
  align-items: flex-end;
}

.message-bubble {
  padding: var(--bubble-padding);
  margin: var(--bubble-margin);
  display: inline-block;
  width: auto;
  max-width: var(--bubble-max-inner-width);
  font-size: 14px;
  word-break: break-word;
}

.user-message {
  display: flex;
  justify-content: flex-end;
  text-align: start;
}
.user-message .message-bubble {
  background-color: #007bff;
  border-radius: 18px 18px 4px 18px;
  color: white;
}

.ai-message {
  display: flex;
  justify-content: flex-start;
  text-align: start;
}
.ai-message .message-bubble {
  background-color: #e9e9eb;
  color: #333;
  border-radius: 18px 18px 18px 4px;
}

.el-textarea__inner {
  border: 1px solid #333;
  overflow-y: overlay;
  resize: none;
  box-sizing: border-box;
}
.el-button {
  min-width: 60px;
  padding: 10px;
}

.markdown-bubble {
  line-height: 1.4;
}
.markdown-bubble h1,
.markdown-bubble h2,
.markdown-bubble h3 {
  margin: 6px 0;
}
.markdown-bubble p {
  margin: 4px 0;
}
.markdown-bubble ul,
.markdown-bubble ol {
  padding-left: 22px;
  margin: 6px 0;
}
.markdown-bubble code {
  background: #222222;
  padding: 2px 4px;
  border-radius: 4px;
}
.markdown-bubble pre {
  background: #222222;
  padding: 8px;
  border-radius: 6px;
  overflow-x: auto;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}
.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.el-textarea__inner::-webkit-scrollbar {
  width: 6px;
}
.el-textarea__inner::-webkit-scrollbar-track {
  background: #f1f1f1;
  border: 1px solid #ddd; 
  border-radius: 4px;
}
.el-textarea__inner::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border: 1px solid #ddd;
  border-radius: 3px;
}
.el-textarea__inner::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

@media (max-width: 768px) {
  :root {
    --bubble-max-inner-width: 85%;
  }
}
</style>