import { useEffect, useRef, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import client from '../api/client'
import type { ChatMessage } from '../types'

export default function ChatPage() {
  const { characterId } = useParams<{ characterId: string }>()
  const navigate = useNavigate()
  const [sessionId, setSessionId] = useState<string>('')
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [characterName, setCharacterName] = useState('')
  const scrollRef = useRef<HTMLDivElement>(null)

  // 创建会话
  useEffect(() => {
    if (!characterId) return
    client.post('/sessions', { character_id: characterId, user_id: 'anonymous' })
      .then((res: any) => {
        const sid = res.data?.session_id
        setSessionId(sid)
        // 拉取历史（新会话为空）
        return client.get(`/chat/history?session_id=${sid}&limit=50`)
      })
      .then((res: any) => {
        setMessages(res.data?.messages || [])
      })
      .catch(() => {})

    // 获取角色名
    client.get(`/characters/${characterId}`)
      .then((res: any) => {
        setCharacterName(res.data?.name || '')
      })
      .catch(() => {})
  }, [characterId])

  // 自动滚动到底部
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || !sessionId || sending) return

    const userContent = input.trim()
    setInput('')
    setSending(true)

    // 先本地追加用户消息
    const userMsg: ChatMessage = {
      message_id: `tmp-${Date.now()}`,
      role: 'user',
      content: userContent,
      created_at: new Date().toISOString(),
    }
    setMessages(prev => [...prev, userMsg])

    try {
      const res: any = await client.post('/chat', {
        session_id: sessionId,
        message: userContent,
        client_timestamp: Math.floor(Date.now() / 1000),
      })

      if (res.data) {
        setMessages(prev => [...prev, res.data])
      }
    } catch (e) {
      setMessages(prev => [...prev, {
        message_id: `err-${Date.now()}`,
        role: 'assistant',
        content: '（角色望着河水，一时陷入沉思……）',
        created_at: new Date().toISOString(),
      }])
    } finally {
      setSending(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="h-screen flex flex-col bg-paper">
      {/* 顶部栏 */}
      <div className="shrink-0 flex items-center gap-3 px-4 py-3 bg-white/80 backdrop-blur border-b border-stone-200">
        <button
          onClick={() => navigate('/')}
          className="text-wood text-sm px-2 py-1 rounded active:bg-stone-100"
        >
          ← 返回
        </button>
        <div className="flex-1 text-center">
          <h2 className="text-base font-bold text-ink">{characterName || ' loading...'}</h2>
          <p className="text-[10px] text-gray-400">永乐十九年 · 徐州知府衙门</p>
        </div>
        <div className="w-10" /> {/* 占位保持居中 */}
      </div>

      {/* 消息列表 */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto no-scrollbar px-4 py-4 space-y-4"
      >
        {messages.length === 0 && (
          <div className="text-center text-gray-400 text-sm mt-10">
            <p>会话已开启</p>
            <p className="mt-1">试着和 {characterName} 打个招呼吧</p>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.message_id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-stone-200 flex items-center justify-center text-xs mr-2 shrink-0 mt-1">
                {characterName ? characterName[0] : '?'}
              </div>
            )}
            <div
              className={`max-w-[75%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-wood text-white rounded-br-md'
                  : 'bg-white text-ink border border-stone-200 rounded-bl-md'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {sending && (
          <div className="flex justify-start">
            <div className="w-8 h-8 rounded-full bg-stone-200 flex items-center justify-center text-xs mr-2 shrink-0">
              {characterName ? characterName[0] : '?'}
            </div>
            <div className="bg-white border border-stone-200 rounded-2xl rounded-bl-md px-4 py-2.5 text-sm text-gray-400">
              <span className="inline-block animate-pulse">……</span>
            </div>
          </div>
        )}
      </div>

      {/* 输入框 */}
      <div className="shrink-0 px-3 py-3 bg-white border-t border-stone-200 safe-area-pb">
        <div className="flex gap-2 items-end">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder={`对 ${characterName || '角色'} 说些什么……`}
            className="flex-1 min-h-[40px] max-h-[120px] px-3 py-2 bg-stone-50 rounded-xl text-sm resize-none outline-none focus:ring-1 focus:ring-wood/30"
            style={{ height: 'auto' }}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || sending}
            className="shrink-0 px-4 py-2 bg-wood text-white text-sm rounded-xl disabled:opacity-40 disabled:cursor-not-allowed active:scale-95 transition-transform"
          >
            发送
          </button>
        </div>
      </div>
    </div>
  )
}
