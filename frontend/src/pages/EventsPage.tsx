import { useEffect, useState } from 'react';
import { Card, Table, Select, Space, Alert, Spin, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import type { Event } from '../types/event';
import type { District } from '../types/farm';

const { Option } = Select;

export default function EventsPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [districts, setDistricts] = useState<District[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingEventId, setUpdatingEventId] = useState<number | null>(null);
  
  // Filter states
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [selectedEventType, setSelectedEventType] = useState<string>('');
  const [selectedStatus, setSelectedStatus] = useState<string>('');

  // Fetch districts on mount
  useEffect(() => {
    fetchDistricts();
  }, []);

  // Fetch events when filters change
  useEffect(() => {
    fetchEvents();
  }, [selectedDistrict, selectedEventType, selectedStatus]);

  const fetchDistricts = async () => {
    try {
      const response = await fetch('/api/districts/');
      if (!response.ok) throw new Error('Failed to fetch districts');
      const data = await response.json();
      setDistricts(data);
    } catch (err) {
      console.error('Error fetching districts:', err);
      setError('Failed to load districts');
    }
  };

  const fetchEvents = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams();
      if (selectedDistrict) params.append('district', selectedDistrict);
      if (selectedEventType) params.append('event_type', selectedEventType);
      if (selectedStatus) params.append('status', selectedStatus);
      
      const url = `/api/events/${params.toString() ? '?' + params.toString() : ''}`;
      const response = await fetch(url);
      
      if (!response.ok) throw new Error('Failed to fetch events');
      
      const data = await response.json();
      setEvents(data);
    } catch (err) {
      console.error('Error fetching events:', err);
      setError(err instanceof Error ? err.message : 'Failed to load events');
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (eventId: number, newStatus: string) => {
    setUpdatingEventId(eventId);
    
    try {
      const response = await fetch(`/api/events/${eventId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });
      
      if (!response.ok) throw new Error('Failed to update status');
      
      const updatedEvent = await response.json();
      
      // Update the event in the local state
      setEvents(events.map(event => 
        event.id === eventId ? updatedEvent : event
      ));
    } catch (err) {
      console.error('Error updating status:', err);
      setError(err instanceof Error ? err.message : 'Failed to update status');
    } finally {
      setUpdatingEventId(null);
    }
  };

  const getEventTypeColor = (eventType: string) => {
    switch (eventType) {
      case 'vet_visit': return 'blue';
      case 'vaccination': return 'green';
      case 'disease_report': return 'red';
      case 'mortality': return 'magenta';
      default: return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'new': return 'orange';
      case 'in_progress': return 'blue';
      case 'resolved': return 'green';
      default: return 'default';
    }
  };

  const columns: ColumnsType<Event> = [
    {
      title: 'Date',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      render: (date: string) => new Date(date).toLocaleDateString(),
      sorter: (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
    },
    {
      title: 'Event Type',
      dataIndex: 'event_type_display',
      key: 'event_type',
      width: 150,
      render: (_: string, record: Event) => (
        <Tag color={getEventTypeColor(record.event_type)}>
          {record.event_type_display}
        </Tag>
      ),
    },
    {
      title: 'Disease',
      dataIndex: 'disease_suspected',
      key: 'disease_suspected',
      width: 180,
      render: (disease: string | null) => disease || '-',
    },
    {
      title: 'Farm',
      key: 'farm',
      width: 220,
      render: (_: any, record: Event) => (
        <div>
          <div style={{ fontWeight: 500 }}>{record.farm_summary.farmer_name}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            {record.farm_summary.village}, {record.farm_summary.district_name}
          </div>
        </div>
      ),
    },
    {
      title: 'Animals Affected',
      dataIndex: 'animals_affected',
      key: 'animals_affected',
      width: 130,
      align: 'center',
      render: (count: number | null) => count !== null ? count : '-',
    },
    {
      title: 'Status',
      key: 'status',
      width: 180,
      render: (_: any, record: Event) => {
        const isEditable = record.event_type === 'disease_report' || record.event_type === 'mortality';
        const isUpdating = updatingEventId === record.id;
        
        if (isEditable) {
          return (
            <Select
              value={record.status}
              style={{ width: '100%' }}
              onChange={(value) => handleStatusChange(record.id, value)}
              loading={isUpdating}
              disabled={isUpdating}
              size="small"
            >
              <Option value="new">New</Option>
              <Option value="in_progress">In Progress</Option>
              <Option value="resolved">Resolved</Option>
            </Select>
          );
        }
        
        return (
          <Tag color={getStatusColor(record.status)}>
            {record.status_display}
          </Tag>
        );
      },
    },
  ];

  return (
    <div>
      <h1 style={{ marginBottom: 24 }}>Events & Outbreaks</h1>
      
      {/* Filter Bar */}
      <Card style={{ marginBottom: 16 }}>
        <Space size="large" style={{ width: '100%' }} wrap>
          <div>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
              District
            </label>
            <Select
              style={{ width: 200 }}
              placeholder="All Districts"
              value={selectedDistrict || undefined}
              onChange={(value) => setSelectedDistrict(value || '')}
              allowClear
            >
              {districts.map((district) => (
                <Option key={district.code} value={district.code}>
                  {district.name}
                </Option>
              ))}
            </Select>
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
              Event Type
            </label>
            <Select
              style={{ width: 200 }}
              placeholder="All Types"
              value={selectedEventType || undefined}
              onChange={(value) => setSelectedEventType(value || '')}
              allowClear
            >
              <Option value="vet_visit">Veterinary Visit</Option>
              <Option value="vaccination">Vaccination</Option>
              <Option value="disease_report">Disease Report</Option>
              <Option value="mortality">Mortality</Option>
            </Select>
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
              Status
            </label>
            <Select
              style={{ width: 200 }}
              placeholder="All Statuses"
              value={selectedStatus || undefined}
              onChange={(value) => setSelectedStatus(value || '')}
              allowClear
            >
              <Option value="new">New</Option>
              <Option value="in_progress">In Progress</Option>
              <Option value="resolved">Resolved</Option>
            </Select>
          </div>
        </Space>
      </Card>

      {error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          closable
          onClose={() => setError(null)}
          style={{ marginBottom: 16 }}
        />
      )}

      <Card>
        <Spin spinning={loading}>
          <Table 
            columns={columns} 
            dataSource={events}
            rowKey="id"
            pagination={{ 
              pageSize: 10,
              showSizeChanger: true,
              showTotal: (total) => `Total ${total} events`
            }}
          />
        </Spin>
      </Card>
    </div>
  );
}
