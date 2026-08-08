import { describe, it, expect } from 'vitest'
import { useChatStore } from './chat'

describe('Chat Store', () => {
    it('should add messages to the store', () => {
        const chatStore = useChatStore()

        // Initial state should be empty
        expect(chatStore.messages).toEqual([])

        // Add message
        chatStore.addMessage('Hello','Hi there!')

        // Check the message was added
        expect(chatStore.messages).toHaveLength(1)
        expect(chatStore.messages[0]).toEqual({
            user: 'Hello',
            ai: 'Hi there!',
            timestamp: expect.any(Date)
        })
    })

    it('should clear messages', () => {
        const chatStore = useChatStore()
        chatStore.addMessage('Test', 'Response')
        expect(chatStore.messages).toHaveLength(1)

        // Clear messages
        chatStore.clearMessages()
        expect(chatStore.messages).toHaveLength(0)
    })
})