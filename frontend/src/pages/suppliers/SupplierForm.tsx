
import { Form, Input, Select, Button, Space } from 'antd'

const { Option } = Select

interface SupplierFormProps {
  form: any
  onSubmit: (values: any) =&gt; void
  initialValues?: any
}

export default function SupplierForm({ form, onSubmit, initialValues }: SupplierFormProps) {
  return (
    &lt;Form
      form={form}
      layout="vertical"
      onFinish={onSubmit}
      initialValues={initialValues}
    &gt;
      &lt;Form.Item
        label="供应商名称"
        name="name"
        rules={[{ required: true, message: '请输入供应商名称' }]}
      &gt;
        &lt;Input placeholder="请输入供应商名称" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="联系人" name="contact_person"&gt;
        &lt;Input placeholder="请输入联系人" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="联系电话" name="contact_phone"&gt;
        &lt;Input placeholder="请输入联系电话" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="邮箱" name="contact_email"&gt;
        &lt;Input placeholder="请输入邮箱" /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="地址" name="address"&gt;
        &lt;Input.TextArea placeholder="请输入地址" rows={2} /&gt;
      &lt;/Form.Item&gt;

      &lt;Form.Item label="业务范围" name="business_scope"&gt;
        &lt;Input.TextArea placeholder="请输入业务范围" rows={3} /&gt;
      &lt;/Form.Item&gt;

      {initialValues?.id &amp;&amp; (
        &lt;Form.Item label="评级" name="rating"&gt;
          &lt;Select placeholder="请选择评级"&gt;
            &lt;Option value="A"&gt;A级&lt;/Option&gt;
            &lt;Option value="B"&gt;B级&lt;/Option&gt;
            &lt;Option value="C"&gt;C级&lt;/Option&gt;
            &lt;Option value="D"&gt;D级&lt;/Option&gt;
          &lt;/Select&gt;
        &lt;/Form.Item&gt;
      )}

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
