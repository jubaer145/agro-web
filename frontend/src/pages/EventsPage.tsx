import { Card, Table, Tag, Button, Space, DatePicker } from 'antd';
import { PlusOutlined, EditOutlined, EyeOutlined, CalendarOutlined } from '@ant-design/icons';

const mockEvents = [
  {
    key: '1',
    id: 'E001',
    farmId: 'F001',
    farmName: 'Green Valley Farm',
    eventType: 'Vaccination',
    date: '2024-11-20',
    veterinarian: 'Dr. Sarah Johnson',
    status: 'Scheduled',
    priority: 'High'
  },
  {
    key: '2',
    id: 'E002',
    farmId: 'F002',
    farmName: 'Sunny Acres Ranch',
    eventType: 'Health Inspection',
    date: '2024-11-18',
    veterinarian: 'Dr. Mike Brown',
    status: 'Completed',
    priority: 'Medium'
  },
  {
    key: '3',
    id: 'E003',
    farmId: 'F001',
    farmName: 'Green Valley Farm',
    eventType: 'Treatment',
    date: '2024-11-25',
    veterinarian: 'Dr. Lisa Chen',
    status: 'Scheduled',
    priority: 'Low'
  }
];

export default function EventsPage() {
  const columns = [
    {
      title: 'Event ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Farm',
      dataIndex: 'farmName',
      key: 'farmName',
    },
    {
      title: 'Event Type',
      dataIndex: 'eventType',
      key: 'eventType',
    },
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
    },
    {
      title: 'Veterinarian',
      dataIndex: 'veterinarian',
      key: 'veterinarian',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'Completed' ? 'green' : status === 'Scheduled' ? 'blue' : 'orange'}>
          {status}
        </Tag>
      ),
    },
    {
      title: 'Priority',
      dataIndex: 'priority',
      key: 'priority',
      render: (priority: string) => (
        <Tag color={priority === 'High' ? 'red' : priority === 'Medium' ? 'orange' : 'green'}>
          {priority}
        </Tag>
      ),
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
        <h1>Events Management</h1>
        <Space>
          <DatePicker placeholder="Filter by date" />
          <Button type="primary" icon={<PlusOutlined />}>
            Schedule Event
          </Button>
        </Space>
      </div>
      
      <Card>
        <div style={{ marginBottom: 16 }}>
          <Space>
            <CalendarOutlined />
            <span>Veterinary Events & Scheduling</span>
          </Space>
        </div>
        
        <Table 
          columns={columns} 
          dataSource={mockEvents}
          pagination={{
            total: mockEvents.length,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => 
              `${range[0]}-${range[1]} of ${total} events`
          }}
        />
      </Card>
    </div>
  );
}
