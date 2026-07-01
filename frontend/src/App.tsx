import { useState } from 'react'
import { NavLink, Route, Routes } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import IOCs from './pages/IOCs'
import MITRE from './pages/MITRE'

const nav = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/iocs', label: 'IOCs' },
  { to: '/mitre', label: 'MITRE' },
]

export default function App() {
  const [open, setOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3">
            <span className="text-lg font-bold text-gray-900">ThreatScope</span>
          </div>
          <button onClick={() => setOpen((v) => !v)} className="md:hidden rounded border border-gray-300 px-3 py-1">Menu</button>
          <nav className="hidden gap-4 text-sm font-medium text-gray-700 md:flex">
            {nav.map((item) => (
              <NavLink key={item.to} to={item.to} end={item.end} className={({ isActive }) => (isActive ? 'text-blue-700' : 'hover:text-blue-600')}>
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/iocs" element={<IOCs />} />
          <Route path="/mitre" element={<MITRE />} />
        </Routes>
      </main>
    </div>
  )
}
