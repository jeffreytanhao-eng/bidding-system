
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export interface Supplier {
  id: string
  name: string
  contact_person?: string
  contact_phone?: string
  contact_email?: string
  address?: string
  business_scope?: string
  rating: string
  status: string
  created_at: string
  updated_at: string
}

export interface SupplierCreate {
  name: string
  contact_person?: string
  contact_phone?: string
  contact_email?: string
  address?: string
  business_scope?: string
}

export interface SupplierUpdate {
  name?: string
  contact_person?: string
  contact_phone?: string
  contact_email?: string
  address?: string
  business_scope?: string
  rating?: string
  status?: string
}

export const supplierService = {
  async getSuppliers(filters?: { rating?: string; status?: string; name?: string }) {
    const response = await api.get('/suppliers', { params: filters })
    return response.data
  },

  async getSupplier(id: string) {
    const response = await api.get(`/suppliers/${id}`)
    return response.data
  },

  async createSupplier(data: SupplierCreate) {
    const response = await api.post('/suppliers', data)
    return response.data
  },

  async updateSupplier(id: string, data: SupplierUpdate) {
    const response = await api.put(`/suppliers/${id}`, data)
    return response.data
  },

  async addTag(id: string, tag_name: string) {
    const response = await api.post(`/suppliers/${id}/tags`, null, { params: { tag_name } })
    return response.data
  },

  async removeTag(id: string, tag_id: string) {
    const response = await api.delete(`/suppliers/${id}/tags/${tag_id}`)
    return response.data
  },

  async updateRating(id: string, rating: string) {
    const response = await api.put(`/suppliers/${id}/rating`, null, { params: { rating } })
    return response.data
  }
}
