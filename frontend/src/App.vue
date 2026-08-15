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
const wantsFollow = ref(false)
const isNearBottom = ref(false)

function getGapFromBottom(): number {
  if (!chatMessagesRef.value) return 0
  const el = chatMessagesRef.value

  return el.scrollHeight - el.scrollTop - el.clientHeight
}

const scrollToBottomSmart = () => {
  const gap = getGapFromBottom()

  if (wantsFollow.value && gap < 30) {
    if(chatMessagesRef.value) chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
  }
}

function handleScroll() {
  const gap = getGapFromBottom()
  isNearBottom.value = gap < 30
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
  wantsFollow.value = true
  let currentText = ''
  let charCounter = 0
  const scrollEvery = 12  

  for (const char of fullText) {
    currentText += char
    chatStore.updateAiResponse(messageId, currentText)
    charCounter++ 

    if (charCounter >= scrollEvery) {
      await nextTick(scrollToBottomSmart)
      charCounter = 0
    }

    await new Promise(resolve => setTimeout(resolve, speed))
  }
  wantsFollow.value = false
}

async function sendMessage() {
  if (userMessage.value.trim() && !isProcessing.value) {
    const userMsg = userMessage.value
    userMessage.value = ""

    wantsFollow.value = true

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

        chatStore.updateAiResponse(messageId, ' ')
        await nextTick()
        await scrollToBottom()
        await typeWriter(messageId, aiFullText)
        
    } catch (error) {
        console.error('Error calling chat API:', error)
        // Update with error message
        chatStore.updateAiResponse(messageId, 'Sorry, there was an error processing your message.')
      } finally {
        isProcessing.value = false
        wantsFollow.value = false
      }
  }
}
</script>

<template>
  <div class="chat-container">
    <!-- Message display area -->
    <div ref="chatMessagesRef" class="chat-messages" @scroll="handleScroll">
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

    <div
      v-if="wantsFollow && chatMessagesRef && !isNearBottom"
      class="scroll-btn-container"
    >
      <!-- spinning ring, inside container -->
      <div class="scroll-ring" :class="{ spinning: wantsFollow }"></div>
      <!-- static clickable button, sits on top, NO rotation -->
      <button class="scroll-down-btn" @click="scrollToBottom">↓</button>
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
  --input-area-height: 65px;
}

/* Add basic styling for layout */
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Arial', sans-serif;
  position: relative;
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

/* This single container handles all positioning */
.scroll-btn-container {
  position: absolute;
  bottom: calc(var(--input-area-height) + 12px);
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  width: 48px;
  height: 48px;
}

/* spinning ring: inside container, spins, no position offset */
.scroll-ring {
  position: absolute;
  inset: 0;
  border-radius: 999px;
  background: conic-gradient(from 180deg, transparent 0%, #2563eb 90%);
  pointer-events: none;
}
.scroll-ring.spinning {
  animation: spin-border 1s linear infinite;
}

/* white button sits perfectly centered inside container */
.scroll-down-btn {
  position: absolute;
  inset: 2px; /* 4px gap all around */
  border-radius: 999px;
  background: #ffffff;
  color: #000000;
  font-weight: 700;
  font-size: 18px;
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);

  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

@keyframes spin-border {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.message-bubble {
  padding: var(--bubble-padding);
  margin: var(--bubble-margin);
  display: inline-block;
  width: auto;
  max-width: var(--bubble-max-inner-width);
  font-size: 14px;
  word-break: break-word;
  line-height: 1.4;
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