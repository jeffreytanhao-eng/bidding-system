
import { useEffect } from 'react'

function App() {
  useEffect(() =&gt; {
    document.body.innerHTML = `
      &lt;div style="padding: 50px; text-align: center; font-family: Arial;"&gt;
        &lt;h1 style="color: #1890ff;"&gt;招标管理系统&lt;/h1&gt;
        &lt;h2 style="color: #52c41a;"&gt;🎉 系统运行正常！&lt;/h2&gt;
        &lt;p style="font-size: 18px; margin-top: 20px;"&gt;前端应用已成功启动！&lt;/p&gt;
      &lt;/div&gt;
    `
  }, [])

  return null
}

export default App
