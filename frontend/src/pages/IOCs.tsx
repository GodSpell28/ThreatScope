import { useEffect, useState } from 'react'

type Row = { id: string; type: string; value: string; risk_score: number }

export default function Iocs() {
  const [rows, setRows] = useState<Row[]>([])
  const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetch(`${API}/api/v1/iocs/search?limit=10`)
      .then(res => res.ok ? res.json() : [])
      .then(setRows)
  }, [API])

  return (
    <div>
      <h1 style={{ fontSize: 22, fontWeight: 600 }}>IOC Investigation</h1>
      <p style={{ color: '#4b5563' }}>Search and review indicators.</p>

      <div style={{ marginTop: 16, background: '#ffffff', border: '1px solid #e5e7eb', borderRadius: 12, overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
          <thead>
            <tr style={{ background: '#f9fafb', textAlign: 'left' }}>
              <th style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>ID</th>
              <th style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>Type</th>
              <th style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>Value</th>
              <th style={{ padding: 12, borderBottom: '1px solid #e5e7eb', textAlign: 'right' }}>Risk Score</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(row => (
              <tr key={row.id}>
                <td style={{ padding: 12, borderBottom: '1px solid #f3f4f6', fontFamily: 'monospace' }}>{row.id}</td>
                <td style={{ padding: 12, borderBottom: '1px solid #f3f4f6' }}>{row.type}</td>
                <td style={{ padding: 12, borderBottom: '1px solid #f3f4f6' }}>{row.value}</td>
                <td style={{ padding: 12, borderBottom: '1px solid #f3f4f6', textAlign: 'right' }}>{row.risk_score}</td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td colSpan={4} style={{ padding: 12, color: '#6b7280' }}>No IOCs found. Seed data or ingest IOCs to populate.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
