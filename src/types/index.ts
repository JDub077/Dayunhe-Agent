export interface Character {
  id: string
  name: string
  title?: string
  era?: string
  avatar_url?: string
  tagline?: string
  tags?: string[]
  knowledge_nodes?: string[]
}

export interface Session {
  session_id: string
  character_id: string
  status: string
  created_at: string
}

export interface ChatMessage {
  message_id: string
  role: 'user' | 'assistant'
  content: string
  character_id?: string
  emotion_tag?: string
  created_at: string
}
