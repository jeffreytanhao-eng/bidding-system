
import { Card, Table, Tag } from 'antd'

interface ScoreSummaryProps {
  summary: any[]
}

export default function ScoreSummary({ summary }: ScoreSummaryProps) {
  const columns = [
    {
      title: '排名',
      dataIndex: 'rank',
      key: 'rank',
      width: 80,
      render: (rank: number) =&gt; {
        if (rank === 1) return &lt;Tag color="gold"&gt;第1名&lt;/Tag&gt;
        if (rank === 2) return &lt;Tag color="silver"&gt;第2名&lt;/Tag&gt;
        if (rank === 3) return &lt;Tag color="bronze"&gt;第3名&lt;/Tag&gt;
        return `第${rank}名`
      }
    },
    { title: '供应商', dataIndex: 'supplier_name', key: 'supplier_name' },
    { title: '报价', dataIndex: 'quote_amount', key: 'quote_amount', render: (v: number) =&gt; v ? `¥${v.toLocaleString()}` : '-' },
    { title: '商务得分', dataIndex: 'business_score', key: 'business_score', render: (v: number) =&gt; v?.toFixed(2) },
    { title: '技术得分', dataIndex: 'technical_score', key: 'technical_score', render: (v: number) =&gt; v?.toFixed(2) },
    { title: '综合得分', dataIndex: 'weighted_score', key: 'weighted_score', render: (v: number) =&gt; v?.toFixed(2) },
  ]

  return (
    &lt;Card title="评分汇总"&gt;
      &lt;Table
        columns={columns}
        dataSource={summary}
        rowKey="bid_id"
        pagination={false}
      /&gt;
    &lt;/Card&gt;
  )
}
