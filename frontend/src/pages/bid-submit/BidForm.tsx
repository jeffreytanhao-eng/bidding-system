
import { useState } from 'react'
import { Form, Input, InputNumber, Button, Space, message } from 'antd'
import FileUpload from './FileUpload'

const { TextArea } = Input

interface BidFormProps {
  inviteToken: string
  onSubmitSuccess: () =&gt; void
}

export default function BidForm({ inviteToken, onSubmitSuccess }: BidFormProps) {
  const [form] = Form.useForm()
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (values: any) =&gt; {
    setSubmitting(true)
    try {
      const response = await fetch('/api/bids', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...values,
          invite_token: inviteToken
        })
      })
      
      const data = await response.json()
      if (data.code === 0) {
        message.success('应标提交成功')
        onSubmitSuccess()
      } else {
        message.error(data.message || '提交失败')
      }
    } catch (error) {
      message.error('提交失败')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    &lt;Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
    &gt;
      &lt;Form.Item
        label="报价金额"
        name="quote_amount"
        rules={[{ required: true, message: '请输入报价金额' }]}
      &gt;
        &lt;InputNumber
          style={{ width: '100%' }}
          placeholder="请输入报价金额"
          min={0}
          precision={2}
          addonBefore="¥"
        /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item
        label="交货/工期"
        name="delivery_period"
        rules={[{ required: true, message: '请输入交货/工期' }]}
      &gt;
        &lt;Input placeholder="例如：30天" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item
        label="联系人"
        name="contact_person"
        rules={[{ required: true, message: '请输入联系人' }]}
      &gt;
        &lt;Input placeholder="请输入联系人" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item
        label="联系电话"
        name="contact_phone"
        rules={[{ required: true, message: '请输入联系电话' }]}
      &gt;
        &lt;Input placeholder="请输入联系电话" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="技术说明" name="technical_summary"&gt;
        &lt;TextArea placeholder="请输入技术说明" rows={4} /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="商务文件"&gt;
        &lt;FileUpload type="business" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="技术文件"&gt;
        &lt;FileUpload type="technical" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item&gt;
        &lt;Space style={{ width: '100%', justifyContent: 'flex-end' }}&gt;
          &lt;Button type="primary" htmlType="submit" loading={submitting}&gt;
            提交应标
          &lt;/Button&gt;
        &lt;/Space&gt;
      &lt;/Form.Item&gt;
    &lt;/Form&gt;
  )
}
