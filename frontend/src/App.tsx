import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Iocs from './pages/Iocs'

export default function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh' }}>
        <header style={{ borderBottom: '1px solid #e5e7eb', background: '#ffffff' }}>
          <div style={{ maxWidth: 1200, margin: '0 auto', padding: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Link to="/" style={{ fontWeight: 700, color: '#0f172a', textDecoration: 'none', fontSize: 18 }}>ThreatScope</Link>
            <nav style={{ fontSize: 14, color: '#374151' }}>
              <Link to="/" style={{ marginRight: 16, textDecoration: 'none', color: '#2563eb' }}>Dashboard</Link>
              <Link to="/iocs" style={{ textDecoration: 'none', color: '#2563eb' }}>IOCs</Link>
            </nav>
          </div>
        </header>
        <main style={{ maxWidth: 1200, margin: '0 auto', padding: 16 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/iocs" element={<Iocs />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}
