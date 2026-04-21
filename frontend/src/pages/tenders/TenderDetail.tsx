
import { Descriptions, Card, Tag } from 'antd'
import { Tender } from '../../services/tenderService'
import dayjs from 'dayjs'

interface TenderDetailProps {
  tender: Tender
}

export default function TenderDetail({ tender }: TenderDetailProps) {
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

  const statusText: Record&lt;string, string&gt; = {
    draft: '草稿',
    published: '已发布',
    reviewing: '评审中',
    completed: '已完成',
    cancelled: '已取消'
  }

  return (
    &lt;Card title="标书详情"&gt;
      &lt;Descriptions bordered column={2}&gt;
        &lt;Descriptions.Item label="标书标题" span={2}&gt;
          {tender.title}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="状态"&gt;
          &lt;Tag color={getStatusColor(tender.status)}&gt;{statusText[tender.status]}&lt;/Tag&gt;
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="预算"&gt;
          {tender.budget ? `¥${tender.budget.toLocaleString()}` : '-'}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="截止时间"&gt;
          {dayjs(tender.deadline).format('YYYY-MM-DD HH:mm')}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="商务权重"&gt;
          {(tender.business_weight * 100).toFixed(0)}%
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="技术权重"&gt;
          {(tender.technical_weight * 100).toFixed(0)}%
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="标书描述" span={2}&gt;
          {tender.description || '-'}
        &lt;/Descriptions.Item&gt;
        &lt;Descriptions.Item label="招标要求" span={2}&gt;
          {tender.requirements || '-'}
        &lt;/Descriptions.Item&gt;
      &lt;/Descriptions&gt;
    &lt;/Card&gt;
  )
}
