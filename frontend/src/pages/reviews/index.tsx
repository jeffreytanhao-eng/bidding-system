
import { useState } from 'react'
import { Card, Tabs, Button, Space, message } from 'antd'
import { SyncOutlined, UserOutlined } from '@ant-design/icons'
import { reviewService } from '../../services/reviewService'

const { TabPane } = Tabs

export default function Reviews() {
  const [loading, setLoading] = useState(false)

  const handleSyncDingtalk = async () =&gt; {
    setLoading(true)
    try {
      await reviewService.syncDingtalk()
      message.success('钉钉同步成功')
    } catch (error) {
      message.error('钉钉同步失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    &lt;div&gt;
      &lt;div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}&gt;
        &lt;h2&gt;评审中心&lt;/h2&gt;
        &lt;Button icon={&lt;SyncOutlined /&gt;} onClick={handleSyncDingtalk} loading={loading}&gt;
          同步钉钉组织架构
        &lt;/Button&gt;
      &lt;/div&gt;

      &lt;Tabs defaultActiveKey="1"&gt;
        &lt;TabPane tab="我的评审任务" key="1"&gt;
          &lt;Card&gt;
            &lt;p&gt;暂无评审任务&lt;/p&gt;
          &lt;/Card&gt;
        &lt;/TabPane&gt;
        &lt;TabPane tab="评审进度管理" key="2"&gt;
          &lt;Card&gt;
            &lt;p&gt;暂无数据&lt;/p&gt;
          &lt;/Card&gt;
        &lt;/TabPane&gt;
      &lt;/Tabs&gt;
    &lt;/div&gt;
  )
}
