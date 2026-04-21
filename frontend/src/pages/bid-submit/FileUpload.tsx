
import { Upload, Button, message } from 'antd'
import { UploadOutlined } from '@ant-design/icons'
import type { UploadProps } from 'antd'

interface FileUploadProps {
  type: 'business' | 'technical'
}

export default function FileUpload({ type }: FileUploadProps) {
  const props: UploadProps = {
    name: 'file',
    action: '/api/upload',
    headers: {
      authorization: 'Bearer token',
    },
    onChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList)
      }
      if (info.file.status === 'done') {
        message.success(`${info.file.name} 上传成功`)
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name} 上传失败`)
      }
    },
  }

  const label = type === 'business' ? '商务文件' : '技术文件'

  return (
    &lt;Upload {...props}&gt;
      &lt;Button icon={&lt;UploadOutlined /&gt;}&gt;上传{label}&lt;/Button&gt;
    &lt;/Upload&gt;
  )
}
