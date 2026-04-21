
import { Routes, Route } from 'react-router-dom'
import { Layout, Menu } from 'antd'
import {
  UserOutlined,
  FileTextOutlined,
  AuditOutlined,
  TrophyOutlined,
  FolderOpenOutlined
} from '@ant-design/icons'
import { useState } from 'react'
import Suppliers from './pages/suppliers'
import Tenders from './pages/tenders'
import Reviews from './pages/reviews'
import Results from './pages/results'
import BidSubmit from './pages/bid-submit'

const { Header, Sider, Content } = Layout

function App() {
  const [selectedKey, setSelectedKey] = useState('suppliers')

  const menuItems = [
    { key: 'suppliers', icon: &lt;UserOutlined /&gt;, label: '供应商管理' },
    { key: 'tenders', icon: &lt;FileTextOutlined /&gt;, label: '标书管理' },
    { key: 'reviews', icon: &lt;AuditOutlined /&gt;, label: '评审中心' },
    { key: 'results', icon: &lt;TrophyOutlined /&gt;, label: '中标管理' }
  ]

  return (
    &lt;Layout style={{ minHeight: '100vh' }}&gt;
      &lt;Header style={{ display: 'flex', alignItems: 'center', padding: '0 24px', background: '#001529' }}&gt;
        &lt;div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold' }}&gt;
          招标管理系统
        &lt;/div&gt;
      &lt;/Header&gt;
      &lt;Layout&gt;
        &lt;Sider width={200} theme="dark"&gt;
          &lt;Menu
            mode="inline"
            selectedKeys={[selectedKey]}
            style={{ height: '100%', borderRight: 0 }}
            items={menuItems}
            onClick={({ key }) =&gt; setSelectedKey(key)}
          /&gt;
        &lt;/Sider&gt;
        &lt;Layout style={{ padding: '24px' }}&gt;
          &lt;Content style={{ background: '#fff', padding: 24, borderRadius: 8 }}&gt;
            {selectedKey === 'suppliers' &amp;&amp; &lt;Suppliers /&gt;}
            {selectedKey === 'tenders' &amp;&amp; &lt;Tenders /&gt;}
            {selectedKey === 'reviews' &amp;&amp; &lt;Reviews /&gt;}
            {selectedKey === 'results' &amp;&amp; &lt;Results /&gt;}
          &lt;/Content&gt;
        &lt;/Layout&gt;
      &lt;/Layout&gt;
    &lt;/Layout&gt;
  )
}

export default App
