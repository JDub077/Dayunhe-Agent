import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'
import type { Character } from '../types'

export default function HomePage() {
  const [characters, setCharacters] = useState<Character[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    client.get('/characters').then((res: any) => {
      setCharacters(res.data || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen flex flex-col items-center px-4 py-8">
      <header className="text-center mb-8">
        <h1 className="text-3xl font-bold text-wood tracking-widest mb-2">明舟北渡</h1>
        <p className="text-sm text-gray-500">永乐十九年 · 运河悬案</p>
      </header>

      {loading ? (
        <div className="text-gray-400 mt-20">载入中……</div>
      ) : (
        <div className="w-full max-w-md grid grid-cols-1 gap-4">
          {characters.map((c) => (
            <button
              key={c.id}
              onClick={() => navigate(`/chat/${c.id}`)}
              className="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm border border-stone-200 active:scale-[0.98] transition-transform text-left"
            >
              <div className="w-14 h-14 rounded-full bg-stone-200 flex items-center justify-center text-2xl shrink-0">
                {c.avatar_url ? (
                  <img src={c.avatar_url} alt={c.name} className="w-full h-full rounded-full object-cover" />
                ) : (
                  <span>{c.name[0]}</span>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-baseline gap-2">
                  <h2 className="text-lg font-bold text-ink">{c.name}</h2>
                  <span className="text-xs text-gray-400">{c.title}</span>
                </div>
                <p className="text-sm text-gray-500 truncate">{c.tagline}</p>
                <div className="flex gap-1 mt-1">
                  {(c.tags || []).slice(0, 3).map((tag) => (
                    <span key={tag} className="text-[10px] px-1.5 py-0.5 bg-stone-100 text-stone-500 rounded">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </button>
          ))}
        </div>
      )}

      <footer className="mt-auto pt-8 text-xs text-gray-400 text-center">
        选择一个角色，进入永乐十九年的运河往事
      </footer>
    </div>
  )
}
