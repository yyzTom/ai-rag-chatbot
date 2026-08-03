import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
    // State: array of chat messages
    const messages = ref<Array<{ user: string; ai: string; timestamp: Date }>>([])

    // Action: add a message to the chat history
    function addMessage(userMessage: string, aiResponse: string) {
        messages.value.push({
            user: userMessage,
            ai: aiResponse,
            timestamp: new Date()
        })
    }

    return {
        messages,
        addMessage
    }
})