
import { Card, List, Button, Space, Tag } from 'antd'
import { TrophyOutlined } from '@ant-design/icons'

interface RecommendationListProps {
  recommendations: any[]
  onApprove: (id: string) =&gt; void
}

export default function RecommendationList({ recommendations, onApprove }: RecommendationListProps) {
  return (
    &lt;Card title="推荐中标名单"&gt;
      &lt;List
        dataSource={recommendations}
        renderItem={(item) =&gt; (
          &lt;List.Item
            actions={[
              &lt;Button type="primary" onClick={() =&gt; onApprove(item.bid_id)}&gt;
                审核通过
              &lt;/Button&gt;
            ]}
          &gt;
            &lt;List.Item.Meta
              avatar={item.rank === 1 ? &lt;TrophyOutlined style={{ color: '#faad14', fontSize: 24 }} /&gt; : null}
              title={
                &lt;Space&gt;
                  &lt;span&gt;{item.supplier_name}&lt;/span&gt;
                  &lt;Tag color="blue"&gt;综合得分: {item.weighted_score.toFixed(2)}&lt;/Tag&gt;
                &lt;/Space&gt;
              }
              description={
                &lt;Space&gt;
                  &lt;span&gt;商务: {item.business_score.toFixed(2)}&lt;/span&gt;
                  &lt;span&gt;技术: {item.technical_score.toFixed(2)}&lt;/span&gt;
                  &lt;span&gt;报价: ¥{item.quote_amount?.toLocaleString()}&lt;/span&gt;
                &lt;/Space&gt;
              }
            /&gt;
          &lt;/List.Item&gt;
        )}
      /&gt;
    &lt;/Card&gt;
  )
}
