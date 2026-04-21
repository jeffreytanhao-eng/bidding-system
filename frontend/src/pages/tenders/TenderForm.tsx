
import { Form, Input, InputNumber, DatePicker, Select, Button, Space } from 'antd'
import dayjs from 'dayjs'

const { Option } = Select
const { TextArea } = Input

interface TenderFormProps {
  form: any
  onSubmit: (values: any) =&gt; void
  initialValues?: any
}

export default function TenderForm({ form, onSubmit, initialValues }: TenderFormProps) {
  return (
    &lt;Form
      form={form}
      layout="vertical"
      onFinish={onSubmit}
      initialValues={{
        ...initialValues,
        deadline: initialValues?.deadline ? dayjs(initialValues.deadline) : undefined
      }}
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
  )
}
