import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import ChatPage from './pages/ChatPage'

function App() {
  return (
    <div className="min-h-screen bg-paper text-ink">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat/:characterId" element={<ChatPage />} />
      </Routes>
    </div>
  )
}

export default App
