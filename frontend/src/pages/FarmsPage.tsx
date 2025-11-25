import React from 'react';
import { Card, Table, Tag, Button, Space } from 'antd';
import { PlusOutlined, EditOutlined, EyeOutlined } from '@ant-design/icons';

const mockFarms = [
  {
    key: '1',
    id: 'F001',
    name: 'Green Valley Farm',
    owner: 'John Doe',
    location: 'Almaty Region',
    type: 'Dairy',
    status: 'Active',
    lastInspection: '2024-11-15'
  },
  {
    key: '2',
    id: 'F002',
    name: 'Sunny Acres Ranch',
    owner: 'Jane Smith',
    location: 'Nur-Sultan Region',
    type: 'Livestock',
    status: 'Active',
    lastInspection: '2024-11-10'
  },
  {
    key: '3',
    id: 'F003',
    name: 'Mountain View Farm',
    owner: 'Bob Wilson',
    location: 'Shymkent Region',
    type: 'Mixed',
    status: 'Pending',
    lastInspection: '2024-10-28'
  }
];

export default function FarmsPage() {
  const columns = [
    {
      title: 'Farm ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Farm Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Owner',
      dataIndex: 'owner',
      key: 'owner',
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
    },
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'Active' ? 'green' : 'orange'}>
          {status}
        </Tag>
      ),
    },
    {
      title: 'Last Inspection',
      dataIndex: 'lastInspection',
      key: 'lastInspection',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: () => (
        <Space size="middle">
          <Button icon={<EyeOutlined />} size="small">View</Button>
          <Button icon={<EditOutlined />} size="small">Edit</Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1>Farms Management</h1>
        <Button type="primary" icon={<PlusOutlined />}>
          Register New Farm
        </Button>
      </div>
      
      <Card>
        <Table 
          columns={columns} 
          dataSource={mockFarms}
          pagination={{
            total: mockFarms.length,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => 
              `${range[0]}-${range[1]} of ${total} farms`
          }}
        />
      </Card>
    </div>
  );
}
