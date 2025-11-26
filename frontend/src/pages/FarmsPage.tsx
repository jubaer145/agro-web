import { useEffect, useState } from 'react';
import { Card, Table, Select, Input, Space, Alert, Spin, Tag, Tooltip } from 'antd';
import { SearchOutlined, EnvironmentOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { Farm, District } from '../types/farm';

const { Option } = Select;

export default function FarmsPage() {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [districts, setDistricts] = useState<District[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filter states
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [searchText, setSearchText] = useState<string>('');

  // Fetch districts on mount
  useEffect(() => {
    fetchDistricts();
  }, []);

  // Fetch farms when filters change
  useEffect(() => {
    fetchFarms();
  }, [selectedDistrict, searchText]);

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

  const fetchFarms = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams();
      if (selectedDistrict) params.append('district', selectedDistrict);
      if (searchText) params.append('search', searchText);
      
      const url = `/api/farms/${params.toString() ? '?' + params.toString() : ''}`;
      const response = await fetch(url);
      
      if (!response.ok) throw new Error('Failed to fetch farms');
      
      const data = await response.json();
      setFarms(data);
    } catch (err) {
      console.error('Error fetching farms:', err);
      setError(err instanceof Error ? err.message : 'Failed to load farms');
      setFarms([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDistrictChange = (value: string) => {
    setSelectedDistrict(value);
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(e.target.value);
  };

  const columns: ColumnsType<Farm> = [
    {
      title: 'Farmer Name',
      dataIndex: 'farmer_name',
      key: 'farmer_name',
      width: 200,
      sorter: (a, b) => a.farmer_name.localeCompare(b.farmer_name),
    },
    {
      title: 'Phone',
      dataIndex: 'phone',
      key: 'phone',
      width: 150,
    },
    {
      title: 'Village',
      dataIndex: 'village',
      key: 'village',
      width: 150,
      render: (village: string, record: Farm) => (
        <Space>
          {record.location_lat && record.location_lng && (
            <Tooltip title={`${record.location_lat.toFixed(4)}, ${record.location_lng.toFixed(4)}`}>
              <EnvironmentOutlined style={{ color: '#1890ff' }} />
            </Tooltip>
          )}
          {village}
        </Space>
      ),
    },
    {
      title: 'District',
      dataIndex: 'district_name',
      key: 'district_name',
      width: 180,
      render: (_: string, record: Farm) => (
        <Tag color="blue">{record.district_code}</Tag>
      ),
    },
    {
      title: 'Total Animals',
      dataIndex: 'total_animals',
      key: 'total_animals',
      width: 120,
      align: 'right',
      sorter: (a, b) => a.total_animals - b.total_animals,
      render: (total: number) => (
        <span style={{ fontWeight: 'bold', color: '#52c41a' }}>
          {total.toLocaleString()}
        </span>
      ),
    },
    {
      title: 'Herds',
      key: 'herds',
      width: 250,
      render: (_, record: Farm) => (
        <Space size="small" wrap>
          {record.herds.map((herd) => (
            <Tag key={herd.id} color="green">
              {herd.headcount} {herd.animal_type_display}
            </Tag>
          ))}
        </Space>
      ),
    },
  ];

  return (
    <div>
      <h1 style={{ marginBottom: 24 }}>Farms Registry</h1>
      
      {/* Filter Bar */}
      <Card style={{ marginBottom: 16 }}>
        <Space size="large" style={{ width: '100%' }} wrap>
          <div>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
              District:
            </label>
            <Select
              placeholder="All Districts"
              style={{ width: 200 }}
              onChange={handleDistrictChange}
              value={selectedDistrict || undefined}
              allowClear
            >
              {districts.map((district) => (
                <Option key={district.code} value={district.code}>
                  {district.name}
                </Option>
              ))}
            </Select>
          </div>
          
          <div style={{ flex: 1, minWidth: 300 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
              Search:
            </label>
            <Input
              placeholder="Search by farmer name or phone..."
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={handleSearchChange}
              allowClear
            />
          </div>
        </Space>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          showIcon
          closable
          onClose={() => setError(null)}
          style={{ marginBottom: 16 }}
        />
      )}

      {/* Farms Table */}
      <Card>
        <Spin spinning={loading}>
          <Table
            columns={columns}
            dataSource={farms}
            rowKey="id"
            pagination={{
              pageSize: 10,
              showSizeChanger: true,
              pageSizeOptions: ['10', '20', '50', '100'],
              showTotal: (total, range) => 
                `${range[0]}-${range[1]} of ${total} farms`,
            }}
            locale={{
              emptyText: loading ? 'Loading...' : 'No farms found'
            }}
          />
        </Spin>
      </Card>
    </div>
  );
}
