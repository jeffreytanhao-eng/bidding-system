
import { Form, InputNumber, Input, Select, Button, Space } from 'antd'

const { Option } = Select
const { TextArea } = Input

interface ReviewFormProps {
  form: any
  onSubmit: (values: any) =&gt; void
}

export default function ReviewForm({ form, onSubmit }: ReviewFormProps) {
  return (
    &lt;Form
      form={form}
      layout="vertical"
      onFinish={onSubmit}
    &gt;
      &lt;Form.Item label="价格评分" name="price_score"&gt;
        &lt;InputNumber
          style={{ width: '100%' }}
          min={0}
          max={100}
          placeholder="0-100"
        /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="资质评分" name="qualification_score"&gt;
        &lt;InputNumber
          style={{ width: '100%' }}
          min={0}
          max={100}
          placeholder="0-100"
        /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="经验评分" name="experience_score"&gt;
        &lt;InputNumber
          style={{ width: '100%' }}
          min={0}
          max={100}
          placeholder="0-100"
        /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="服务评分" name="service_score"&gt;
        &lt;InputNumber
          style={{ width: '100%' }}
          min={0}
          max={100}
          placeholder="0-100"
        /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="评审意见" name="comment"&gt;
        &lt;TextArea placeholder="请输入评审意见" rows={4} /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="推荐意见" name="recommendation"&gt;
        &lt;Select placeholder="请选择推荐意见"&gt;
          &lt;Option value="recommend"&gt;推荐&lt;/Option&gt;
          &lt;Option value="neutral"&gt;中立&lt;/Option&gt;
          &lt;Option value="not_recommend"&gt;不推荐&lt;/Option&gt;
        &lt;/Select&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item&gt;
        &lt;Space style={{ width: '100%', justifyContent: 'flex-end' }}&gt;
          &lt;Button type="primary" htmlType="submit"&gt;
            提交评分
          &lt;/Button&gt;
        &lt;/Space&gt;
      &lt;/Form.Item&gt;
    &lt;/Form&gt;
  )
}
