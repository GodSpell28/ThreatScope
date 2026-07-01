import { useEffect, useState } from 'react'
import { mitreTechniques } from '../lib/api'

type Technique = { id: string; name: string; tactic: string; description: string | null }

export default function MITRE() {
  const [q, setQ] = useState('')
  const [tactic, setTactic] = useState('')
  const [items, setItems] = useState<Technique[]>([])

  useEffect(() => {
    mitreTechniques({ q, tactic }).then((data) => setItems(data))
  }, [q, tactic])

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-gray-900">MITRE ATT&CK</h1>
      <div className="flex gap-2">
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search techniques" className="flex-1 rounded border border-gray-300 p-2" />
        <input value={tactic} onChange={(e) => setTactic(e.target.value)} placeholder="Tactic" className="w-48 rounded border border-gray-300 p-2" />
      </div>
      <div className="space-y-2">
        {items.map((item) => (
          <div key={item.id} className="rounded border border-gray-200 bg-white p-3 shadow-sm">
            <p className="font-semibold text-gray-900">{item.id} — {item.name}</p>
            <p className="text-xs text-gray-600">{item.tactic}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
