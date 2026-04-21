
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export interface Reviewer {
  id: string
  tender_id: string
  user_id: string
  dingtalk_user_id?: string
  review_type: string
  status: string
  created_at: string
}

export interface ScoreCreate {
  price_score?: number
  qualification_score?: number
  experience_score?: number
  service_score?: number
  comment?: string
  recommendation?: string
}

export const reviewService = {
  async syncDingtalk() {
    const response = await api.post('/dingtalk/sync')
    return response.data
  },

  async getDepartments() {
    const response = await api.get('/dingtalk/departments')
    return response.data
  },

  async getUsers() {
    const response = await api.get('/dingtalk/users')
    return response.data
  },

  async assignReviewers(tender_id: string, reviewers: any[]) {
    const response = await api.post(`/tender/${tender_id}/reviewers`, reviewers)
    return response.data
  },

  async startReview(tender_id: string) {
    const response = await api.post(`/tender/${tender_id}/start-review`)
    return response.data
  },

  async getMyReviews() {
    const response = await api.get('/my')
    return response.data
  },

  async submitScore(reviewer_id: string, bid_id: string, score_data: ScoreCreate) {
    const response = await api.post(`/${reviewer_id}/score`, null, {
      params: { bid_id },
      data: score_data
    })
    return response.data
  },

  async getProgress(tender_id: string) {
    const response = await api.get(`/tender/${tender_id}/progress`)
    return response.data
  },

  async remindReviewers(tender_id: string) {
    const response = await api.post(`/tender/${tender_id}/remind`)
    return response.data
  }
}
