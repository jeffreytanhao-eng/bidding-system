
import { Descriptions, Card, Tag } from 'antd'
import { Supplier } from '../../services/supplierService'

interface SupplierDetailProps {
  supplier: Supplier
}

export default function SupplierDetail({ supplier }: SupplierDetailProps) {
  const ratingColors: Record&lt;string, string&gt; = {
    A: 'green',
    B: 'blue',
    C: 'orange',
    D: 'red'
  }

  return (
    &lt;Card title="供应商详情"&gt;
      &lt;Descriptions bordered column={2}&gt;
        &lt;Descriptions.Item label="供应商名称" span={2}&gt;
          {supplier.name}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="联系人"&gt;
          {supplier.contact_person || '-'}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="联系电话"&gt;
          {supplier.contact_phone || '-'}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="邮箱"&gt;
          {supplier.contact_email || '-'}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="评级"&gt;
          &lt;Tag color={ratingColors[supplier.rating]}&gt;{supplier.rating}级&lt;/Tag&gt;
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="状态"&gt;
          {supplier.status}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="地址" span={2}&gt;
          {supplier.address || '-'}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="业务范围" span={2}&gt;
          {supplier.business_scope || '-'}
        &lt;/Descriptions.Item&gt;
      &lt;/Descriptions&gt;
    &lt;/Card&gt;
  )
}
