
import { Table, Checkbox, Select } from 'antd'

const { Option } = Select

interface ReviewerSelectorProps {
  users: any[]
  selected: any[]
  onSelectionChange: (selected: any[]) =&gt; void
}

export default function ReviewerSelector({ users, selected, onSelectionChange }: ReviewerSelectorProps) {
  const columns = [
    {
      title: '姓名',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '部门',
      dataIndex: 'department',
      key: 'department',
    },
    {
      title: '评审类型',
      key: 'review_type',
      render: (_: any, record: any) =&gt; {
        const current = selected.find(s =&gt; s.user_id === record.id)
        return (
          &lt;Select
            placeholder="请选择"
            value={current?.review_type}
            style={{ width: 150 }}
            onChange={(value) =&gt; {
              if (value) {
                const newSelected = selected.filter(s =&gt; s.user_id !== record.id)
                newSelected.push({ user_id: record.id, review_type: value })
                onSelectionChange(newSelected)
              } else {
                onSelectionChange(selected.filter(s =&gt; s.user_id !== record.id))
              }
            }}
          &gt;
            &lt;Option value="business"&gt;商务评审&lt;/Option&gt;
            &lt;Option value="technical"&gt;技术评审&lt;/Option&gt;
          &lt;/Select&gt;
        )
      },
    },
  ]

  return &lt;Table columns={columns} dataSource={users} rowKey="id" pagination={false} /&gt;
}
