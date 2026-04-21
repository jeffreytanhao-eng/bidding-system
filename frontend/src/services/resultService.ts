
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const resultService = {
  async calculateSummary(tender_id: string) {
    const response = await api.post(`/tender/${tender_id}/summary`)
    return response.data
  },

  async setWeights(tender_id: string, business_weight: number, technical_weight: number) {
    const response = await api.put(`/tender/${tender_id}/weights`, null, {
      params: { business_weight, technical_weight }
    })
    return response.data
  },

  async getRecommendation(tender_id: string) {
    const response = await api.get(`/tender/${tender_id}/recommendation`)
    return response.data
  },

  async approveResult(tender_id: string, winner_bid_id: string, approver_id: string) {
    const response = await api.post(`/tender/${tender_id}/approve`, null, {
      params: { winner_bid_id, approver_id }
    })
    return response.data
  },

  async announceResult(tender_id: string) {
    const response = await api.post(`/tender/${tender_id}/announce`)
    return response.data
  }
}
