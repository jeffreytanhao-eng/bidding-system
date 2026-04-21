
import { useState } from 'react'
import { Card, Table, Button, Space, message } from 'antd'
import { TrophyOutlined } from '@ant-design/icons'

export default function Results() {
  return (
    &lt;div&gt;
      &lt;div style={{ marginBottom: 16 }}&gt;
        &lt;h2&gt;中标管理&lt;/h2&gt;
      &lt;/div&gt;

      &lt;Card title="中标结果"&gt;
        &lt;p&gt;暂无中标结果&lt;/p&gt;
      &lt;/Card&gt;
    &lt;/div&gt;
  )
}
