
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Card, message, Spin, Result } from 'antd'
import BidForm from './BidForm'

export default function BidSubmit() {
  const { token } = useParams&lt;{ token: string }&gt;()
  const [loading, setLoading] = useState(true)
  const [valid, setValid] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  useEffect(() =&gt; {
    validateToken()
  }, [token])

  const validateToken = async () =&gt; {
    setLoading(true)
    try {
      const response = await fetch(`/api/bids/submit/${token}`)
      const data = await response.json()
      setValid(data.code === 0)
    } catch (error) {
      setValid(false)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitSuccess = () =&gt; {
    setSubmitted(true)
  }

  if (loading) {
    return (
      &lt;div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}&gt;
        &lt;Spin size="large" /&gt;
      &lt;/div&gt;
    )
  }

  if (!valid) {
    return (
      &lt;div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}&gt;
        &lt;Result
          status="error"
          title="无效的链接"
          subTitle="该应标链接无效或已过期，请联系招标负责人。"
        /&gt;
      &lt;/div&gt;
    )
  }

  if (submitted) {
    return (
      &lt;div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}&gt;
        &lt;Result
          status="success"
          title="应标提交成功"
          subTitle="您的应标文件已成功提交，请等待评审结果。"
        /&gt;
      &lt;/div&gt;
    )
  }

  return (
    &lt;div style={{ padding: '24px', maxWidth: 800, margin: '0 auto' }}&gt;
      &lt;Card title="提交应标"&gt;
        &lt;BidForm inviteToken={token!} onSubmitSuccess={handleSubmitSuccess} /&gt;
      &lt;/Card&gt;
    &lt;/div&gt;
  )
}
