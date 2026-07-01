import { useEffect, useState } from 'react'
import { searchIocs, ingestRaw, enrichIoc } from '../lib/api'

type SearchResult = {
  id: string
  type: string
  value: string
  risk_score: number
  confidence: number
  first_seen: string
  last_seen: string
}

export default function IOCs() {
  const [q, setQ] = useState('')
  const [type, setType] = useState('')
  const [items, setItems] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    searchIocs({ q, type, limit: 50 })
      .then((data) => setItems(data))
      .finally(() => setLoading(false))
  }, [q, type])

  async function handleSeed() {
    await ingestRaw([
      { type: 'ipv4', value: '198.51.100.10', confidence: 0.8, sources: [{ source_name: 'demo' }] },
      { type: 'domain', value: 'malicious.example', confidence: 0.9, sources: [{ source_name: 'demo' }] },
    ])
    window.alert('Seeded demo IOCs.')
  }

  async function handleEnrich(id: string) {
    await enrichIoc(id)
    window.alert('Enrichment simulated.')
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">IOCs</h1>
        <button onClick={handleSeed} className="rounded bg-blue-600 px-3 py-2 text-white hover:bg-blue-700">Seed Demo IOCs</button>
      </div>
      <div className="flex gap-2">
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search indicators" className="flex-1 rounded border border-gray-300 p-2" />
        <select value={type} onChange={(e) => setType(e.target.value)} className="rounded border border-gray-300 p-2">
          <option value="">All Types</option>
          <option value="ipv4">IPv4</option>
          <option value="domain">Domain</option>
          <option value="url">URL</option>
          <option value="hash">Hash</option>
        </select>
      </div>
      <div className="overflow-x-auto border border-gray-200 bg-white">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left">
              <th className="p-2">Type</th>
              <th className="p-2">Value</th>
              <th className="p-2">Risk</th>
              <th className="p-2">Confidence</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} className="border-t">
                <td className="p-2 capitalize">{item.type}</td>
                <td className="p-2 font-mono">{item.value}</td>
                <td className="p-2">{item.risk_score}</td>
                <td className="p-2">{item.confidence}</td>
                <td className="p-2">
                  <button onClick={() => handleEnrich(item.id)} className="text-blue-600 hover:underline">Enrich</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {loading && <p className="text-sm text-gray-600">Searching...</p>}
    </div>
  )
}
