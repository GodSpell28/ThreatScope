import axios from 'axios'

export const api = axios.create({ baseURL: '/api/v1' })

export async function ingestRaw(items: Array<Record<string, unknown>>) {
  const { data } = await api.post('/ingest/raw', items)
  return data
}

export async function searchIocs(params: Record<string, unknown>) {
  const { data } = await api.get('/iocs/search', { params })
  return data
}

export async function enrichIoc(id: string) {
  const { data } = await api.post(`/enrich/${id}/enrich`)
  return data
}

export async function correlationRun() {
  const { data } = await api.get('/correlation/run')
  return data
}

export async function scoreIocs() {
  const { data } = await api.get('/score/')
  return data
}

export async function mitreTechniques(params: Record<string, unknown>) {
  const { data } = await api.get('/mitre/search', { params })
  return data
}

export async function reportsIocSummary() {
  const { data } = await api.get('/reports/ioc-summary')
  return data
}
