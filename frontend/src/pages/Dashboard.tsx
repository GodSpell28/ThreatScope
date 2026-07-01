import { useEffect, useState } from 'react'

type Summary = {
  ioc_count?: number
  high_risk_count?: number
  medium_risk_count?: number
  low_risk_count?: number
  avg_risk_score?: number
  type_distribution?: Record<string, number>
}

export default function Dashboard() {
  const [data, setData] = useState<Summary | null>(null)
  const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetch(`${API}/api/v1/reports/ioc-summary`)
      .then(res => res.json())
      .then(setData)
      .catch(() => setData(null))
  }, [API])

  return (
    <div>
      <h1 style={{ fontSize: 22, fontWeight: 600 }}>Dashboard</h1>
      <p style={{ color: '#4b5563' }}>Threat intelligence at a glance.</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 16, marginTop: 16 }}>
        {[
          { label: 'IOCs', value: data?.ioc_count ?? '-' },
          { label: 'High Risk', value: data?.high_risk_count ?? '-' },
          { label: 'Medium Risk', value: data?.medium_risk_count ?? '-' },
          { label: 'Low Risk', value: data?.low_risk_count ?? '-' },
          { label: 'Avg Risk Score', value: data?.avg_risk_score ?? '-' },
        ].map(item => (
          <div key={item.label} style={{ background: '#ffffff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 16 }}>
            <div style={{ color: '#6b7280', fontSize: 12 }}>{item.label}</div>
            <div style={{ marginTop: 6, fontSize: 20, fontWeight: 700 }}>{item.value}</div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 24, background: '#ffffff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, marginTop: 0 }}>Type Distribution</h2>
        <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(data?.type_distribution ?? {}, null, 2)}</pre>
      </div>
    </div>
  )
}
