
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export interface Tender {
  id: string
  title: string
  description?: string
  requirements?: string
  budget?: number
  deadline: string
  status: string
  business_weight: number
  technical_weight: number
  created_at: string
  updated_at: string
  published_at?: string
  completed_at?: string
}

export interface TenderCreate {
  title: string
  description?: string
  requirements?: string
  budget?: number
  deadline: string
  business_weight?: number
  technical_weight?: number
}

export interface TenderUpdate {
  title?: string
  description?: string
  requirements?: string
  budget?: number
  deadline?: string
  business_weight?: number
  technical_weight?: number
  status?: string
}

export const tenderService = {
  async getTenders(status?: string) {
    const response = await api.get('/tenders', { params: { status } })
    return response.data
  },

  async getTender(id: string) {
    const response = await api.get(`/tenders/${id}`)
    return response.data
  },

  async createTender(data: TenderCreate) {
    const response = await api.post('/tenders', data)
    return response.data
  },

  async updateTender(id: string, data: TenderUpdate) {
    const response = await api.put(`/tenders/${id}`, data)
    return response.data
  },

  async uploadAttachment(id: string, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post(`/tenders/${id}/attachments`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async selectInvitees(id: string, supplier_ids: string[]) {
    const response = await api.post(`/tenders/${id}/invitees`, supplier_ids)
    return response.data
  },

  async publishTender(id: string, email_config: any) {
    const response = await api.post(`/tenders/${id}/publish`, email_config)
    return response.data
  }
}
