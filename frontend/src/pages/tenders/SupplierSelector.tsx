
import { Table, Checkbox, Button, Space } from 'antd'
import { Supplier } from '../../services/supplierService'

interface SupplierSelectorProps {
  suppliers: Supplier[]
  selectedIds: string[]
  onSelectionChange: (ids: string[]) =&gt; void
}

export default function SupplierSelector({ suppliers, selectedIds, onSelectionChange }: SupplierSelectorProps) {
  const handleCheck = (id: string, checked: boolean) =&gt; {
    const newSelected = checked
      ? [...selectedIds, id]
      : selectedIds.filter(sid =&gt; sid !== id)
    onSelectionChange(newSelected)
  }

  const columns = [
    {
      title: (
        &lt;Checkbox
          checked={selectedIds.length === suppliers.length &amp;&amp; suppliers.length &gt; 0}
          indeterminate={selectedIds.length &gt; 0 &amp;&amp; selectedIds.length &lt; suppliers.length}
          onChange={(e) =&gt; {
            onSelectionChange(e.target.checked ? suppliers.map(s =&gt; s.id) : [])
          }}
        /&gt;
      ),
      key: 'checkbox',
      width: 60,
      render: (_: any, record: Supplier) =&gt; (
        &lt;Checkbox
          checked={selectedIds.includes(record.id)}
          onChange={(e) =&gt; handleCheck(record.id, e.target.checked)}
        /&gt;
      ),
    },
    { title: '供应商名称', dataIndex: 'name', key: 'name' },
    { title: '联系人', dataIndex: 'contact_person', key: 'contact_person' },
    { title: '联系电话', dataIndex: 'contact_phone', key: 'contact_phone' },
    { title: '评级', dataIndex: 'rating', key: 'rating' },
  ]

  return (
    &lt;div&gt;
      &lt;Table
        columns={columns}
        dataSource={suppliers}
        rowKey="id"
        pagination={false}
        size="small"
      /&gt;
    &lt;/div&gt;
  )
}
