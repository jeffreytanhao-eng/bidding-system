
import { Card, Progress, List, Tag } from 'antd'

interface ReviewProgressProps {
  progress: any
}

export default function ReviewProgress({ progress }: ReviewProgressProps) {
  const percentage = progress.total_reviewers &gt; 0
    ? (progress.completed_count / progress.total_reviewers) * 100
    : 0

  return (
    &lt;Card&gt;
      &lt;div style={{ marginBottom: 24 }}&gt;
        &lt;Progress
          type="circle"
          percent={Math.round(percentage)}
          format={(percent) =&gt; `${percent}%`}
        /&gt;
        &lt;div style={{ marginTop: 16, textAlign: 'center' }}&gt;
          &lt;span&gt;{progress.completed_count}/{progress.total_reviewers} 已完成&lt;/span&gt;
        &lt;/div&gt;
      &lt;/div&gt;

      &lt;List
        dataSource={[
          { status: 'completed', label: '已完成', count: progress.completed_count, color: 'green' },
          { status: 'in_progress', label: '进行中', count: progress.in_progress_count, color: 'blue' },
          { status: 'pending', label: '待评审', count: progress.pending_count, color: 'orange' }
        ]}
        renderItem={(item) =&gt; (
          &lt;List.Item&gt;
            &lt;div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}&gt;
              &lt;span&gt;
                &lt;Tag color={item.color}&gt;{item.label}&lt;/Tag&gt;
              &lt;/span&gt;
              &lt;span&gt;{item.count} 人&lt;/span&gt;
            &lt;/div&gt;
          &lt;/List.Item&gt;
        )}
      /&gt;
    &lt;/Card&gt;
  )
}
