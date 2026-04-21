
import { useState, useEffect } from 'react'
import { Table, Button, Space, Modal, Form, Input, InputNumber, DatePicker, Select, message } from 'antd'
import { PlusOutlined, EditOutlined, EyeOutlined } from '@ant-design/icons'
import { tenderService, Tender, TenderCreate, TenderUpdate } from '../../services/tenderService'
import dayjs from 'dayjs'

const { Option } = Select
const { TextArea } = Input

export default function Tenders() {
  const [tenders, setTenders] = useState&lt;Tender[]&gt;([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingTender, setEditingTender] = useState&lt;Tender | null&gt;(null)
  const [form] = Form.useForm()

  useEffect(() =&gt; {
    fetchTenders()
  }, [])

  const fetchTenders = async () =&gt; {
    setLoading(true)
    try {
      const result = await tenderService.getTenders()
      if (result.code === 0) {
        setTenders(result.data)
      }
    } catch (error) {
      message.error('获取标书列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () =&gt; {
    setEditingTender(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (tender: Tender) =&gt; {
    setEditingTender(tender)
    form.setFieldsValue({
      ...tender,
      deadline: dayjs(tender.deadline)
    })
    setModalVisible(true)
  }

  const handleSubmit = async (values: any) =&gt; {
    try {
      const data = {
        ...values,
        deadline: values.deadline.toISOString()
      }
      
      if (editingTender) {
        await tenderService.updateTender(editingTender.id, data as TenderUpdate)
        message.success('标书更新成功')
      } else {
        await tenderService.createTender(data as TenderCreate)
        message.success('标书创建成功')
      }
      setModalVisible(false)
      fetchTenders()
    } catch (error) {
      message.error('操作失败')
    }
  }

  const getStatusColor = (status: string) =&gt; {
    const colors: Record&lt;string, string&gt; = {
      draft: 'default',
      published: 'blue',
      reviewing: 'orange',
      completed: 'green',
      cancelled: 'red'
    }
    return colors[status] || 'default'
  }

  const columns = [
    { title: '标书标题', dataIndex: 'title', key: 'title' },
    { title: '预算', dataIndex: 'budget', key: 'budget', render: (v: number) =&gt; v ? `¥${v.toLocaleString()}` : '-' },
    { title: '截止时间', dataIndex: 'deadline', key: 'deadline', render: (v: string) =&gt; dayjs(v).format('YYYY-MM-DD HH:mm') },
    { title: '状态', dataIndex: 'status', key: 'status',
      render: (status: string) =&gt; {
        const statusText: Record&lt;string, string&gt; = {
          draft: '草稿',
          published: '已发布',
          reviewing: '评审中',
          completed: '已完成',
          cancelled: '已取消'
        }
        return &lt;span style={{ color: getStatusColor(status) }}&gt;{statusText[status] || status}&lt;/span&gt;
      }
    },
    { title: '商务权重', dataIndex: 'business_weight', key: 'business_weight', render: (v: number) =&gt; `${(v * 100).toFixed(0)}%` },
    { title: '技术权重', dataIndex: 'technical_weight', key: 'technical_weight', render: (v: number) =&gt; `${(v * 100).toFixed(0)}%` },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Tender) =&gt; (
        &lt;Space&gt;
          &lt;Button type="link" icon={&lt;EyeOutlined /&gt;}&gt;查看&lt;/Button&gt;
          &lt;Button type="link" icon={&lt;EditOutlined /&gt;} onClick={() =&gt; handleEdit(record)}&gt;编辑&lt;/Button&gt;
        &lt;/Space&gt;
      ),
    },
  ]

  return (
    &lt;div&gt;
      &lt;div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}&gt;
        &lt;h2&gt;标书管理&lt;/h2&gt;
        &lt;Button type="primary" icon={&lt;PlusOutlined /&gt;} onClick={handleCreate}&gt;
          新增标书
        &lt;/Button&gt;
      &lt;/div&gt;
      
      &lt;Table
        columns={columns}
        dataSource={tenders}
        rowKey="id"
        loading={loading}
      /&gt;

      &lt;Modal
        title={editingTender ? '编辑标书' : '新增标书'}
        open={modalVisible}
        onCancel={() =&gt; setModalVisible(false)}
        footer={null}
        width={700}
      &gt;
        &lt;Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        &gt;
          &lt;Form.Item
            label="标书标题"
            name="title"
            rules={[{ required: true, message: '请输入标书标题' }]}
          &gt;
            &lt;Input placeholder="请输入标书标题" /&gt;
          &lt;/Form.Item&gt;

          &lt;Form.Item label="标书描述" name="description"&gt;
            &lt;TextArea placeholder="请输入标书描述" rows={3} /&gt;
          &lt;/Form.Item&gt;

          &lt;Form.Item label="招标要求" name="requirements"&gt;
            &lt;TextArea placeholder="请输入招标要求" rows={4} /&gt;
          &lt;/Form.Item&gt;

          &lt;Form.Item label="预算" name="budget"&gt;
            &lt;InputNumber
              style={{ width: '100%' }}
              placeholder="请输入预算"
              min={0}
              precision={2}
            /&gt;
          &lt;/Form.Item&gt;

          &lt;Form.Item
            label="截止时间"
            name="deadline"
            rules={[{ required: true, message: '请选择截止时间' }]}
          &gt;
            &lt;DatePicker
              showTime
              style={{ width: '100%' }}
              placeholder="请选择截止时间"
            /&gt;
          &lt;/Form.Item&gt;

          &lt;Form.Item label="商务评分权重" name="business_weight" initialValue={0.4}&gt;
            &lt;InputNumber
              style={{ width: '100%' }}
              min={0}
              max={1}
              step={0.1}
              precision={2}
            /&gt;
          &lt;/Form.Item&gt;

          &lt;Form.Item label="技术评分权重" name="technical_weight" initialValue={0.6}&gt;
            &lt;InputNumber
              style={{ width: '100%' }}
              min={0}
              max={1}
              step={0.1}
              precision={2}
            /&gt;
          &lt;/Form.Item&gt;

          &lt;Form.Item&gt;
            &lt;Space style={{ width: '100%', justifyContent: 'flex-end' }}&gt;
              &lt;Button type="primary" htmlType="submit"&gt;
                保存
              &lt;/Button&gt;
            &lt;/Space&gt;
          &lt;/Form.Item&gt;
        &lt;/Form&gt;
      &lt;/Modal&gt;
    &lt;/div&gt;
  )
}
