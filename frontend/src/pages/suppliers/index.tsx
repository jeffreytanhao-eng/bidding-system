
import { useState, useEffect } from 'react'
import { Table, Button, Space, Modal, Form, Input, Select, message } from 'antd'
import { PlusOutlined, EditOutlined } from '@ant-design/icons'
import { supplierService, Supplier, SupplierCreate, SupplierUpdate } from '../../services/supplierService'
import SupplierForm from './SupplierForm'

const { Option } = Select

export default function Suppliers() {
  const [suppliers, setSuppliers] = useState&lt;Supplier[]&gt;([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingSupplier, setEditingSupplier] = useState&lt;Supplier | null&gt;(null)
  const [form] = Form.useForm()

  useEffect(() =&gt; {
    fetchSuppliers()
  }, [])

  const fetchSuppliers = async () =&gt; {
    setLoading(true)
    try {
      const result = await supplierService.getSuppliers()
      if (result.code === 0) {
        setSuppliers(result.data)
      }
    } catch (error) {
      message.error('获取供应商列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () =&gt; {
    setEditingSupplier(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (supplier: Supplier) =&gt; {
    setEditingSupplier(supplier)
    form.setFieldsValue(supplier)
    setModalVisible(true)
  }

  const handleSubmit = async (values: any) =&gt; {
    try {
      if (editingSupplier) {
        await supplierService.updateSupplier(editingSupplier.id, values as SupplierUpdate)
        message.success('供应商更新成功')
      } else {
        await supplierService.createSupplier(values as SupplierCreate)
        message.success('供应商创建成功')
      }
      setModalVisible(false)
      fetchSuppliers()
    } catch (error) {
      message.error('操作失败')
    }
  }

  const columns = [
    { title: '供应商名称', dataIndex: 'name', key: 'name' },
    { title: '联系人', dataIndex: 'contact_person', key: 'contact_person' },
    { title: '联系电话', dataIndex: 'contact_phone', key: 'contact_phone' },
    { title: '邮箱', dataIndex: 'contact_email', key: 'contact_email' },
    { title: '评级', dataIndex: 'rating', key: 'rating',
      render: (rating: string) =&gt; {
        const colors: Record&lt;string, string&gt; = { A: 'green', B: 'blue', C: 'orange', D: 'red' }
        return &lt;span style={{ color: colors[rating] }}&gt;{rating}级&lt;/span&gt;
      }
    },
    { title: '状态', dataIndex: 'status', key: 'status' },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Supplier) =&gt; (
        &lt;Space&gt;
          &lt;Button type="link" icon={&lt;EditOutlined /&gt;} onClick={() =&gt; handleEdit(record)}&gt;编辑&lt;/Button&gt;
        &lt;/Space&gt;
      ),
    },
  ]

  return (
    &lt;div&gt;
      &lt;div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}&gt;
        &lt;h2&gt;供应商管理&lt;/h2&gt;
        &lt;Button type="primary" icon={&lt;PlusOutlined /&gt;} onClick={handleCreate}&gt;
          新增供应商
        &lt;/Button&gt;
      &lt;/div&gt;
      
      &lt;Table
        columns={columns}
        dataSource={suppliers}
        rowKey="id"
        loading={loading}
      /&gt;

      &lt;Modal
        title={editingSupplier ? '编辑供应商' : '新增供应商'}
        open={modalVisible}
        onCancel={() =&gt; setModalVisible(false)}
        footer={null}
        width={600}
      &gt;
        &lt;SupplierForm
          form={form}
          onSubmit={handleSubmit}
          initialValues={editingSupplier || {}}
        /&gt;
      &lt;/Modal&gt;
    &lt;/div&gt;
  )
}
