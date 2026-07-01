import { useEffect, useState } from 'react'
import { reportsIocSummary, correlationRun } from '../lib/api'

type Summary = {
  ioc_count: number
  avg_risk_score: number
  high_risk_count: number
  medium_risk_count: number
  low_risk_count: number
  type_distribution: Record<string, number>
  source_frequency: Record<string, number>
}

export default function Dashboard() {
  const [data, setData] = useState<Summary | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([reportsIocSummary(), correlationRun()])
      .then(([summary]) => {
        setData(summary)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
      {loading && <p className="text-sm text-gray-600">Loading...</p>}
      {!loading && !data && <p className="text-sm text-red-600">Unable to load summary.</p>}
      {!loading && data && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Kpi title="Total IOCs" value={data.ioc_count} />
          <Kpi title="Average Risk" value={data.avg_risk_score} />
          <Kpi title="High Risk" value={data.high_risk_count} />
          <Kpi title="Medium Risk" value={data.medium_risk_count} />
          <Kpi title="Low Risk" value={data.low_risk_count} />
        </div>
      )}
    </div>
  )
}

function Kpi({ title, value }: { title: string; value: number | string }) {
  return (
    <div className="rounded border border-gray-200 bg-white p-4 shadow-sm">
      <p className="text-xs uppercase text-gray-500">{title}</p>
      <p className="text-2xl font-semibold text-gray-900">{value as number}</p>
    </div>
  )
}
