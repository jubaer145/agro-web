import { useEffect, useState } from 'react';
import { Card, Spin, Alert, Row, Col, Statistic, Select, Table } from 'antd';
import { HomeOutlined, TeamOutlined, WarningOutlined } from '@ant-design/icons';
import type { District } from '../types/farm';
import { api } from '../lib/api';

const { Option } = Select;

interface DashboardSummary {
  total_farms: number;
  total_animals: number;
  open_outbreaks: number;
  farms_by_district: Array<{
    district_code: string;
    district_name: string;
    farm_count: number;
  }>;
  outbreaks_by_disease: Array<{
    disease_suspected: string;
    count: number;
  }>;
}

export default function DashboardPage() {
  const [districts, setDistricts] = useState<District[]>([]);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDistricts();
  }, []);

  useEffect(() => {
    fetchSummary();
  }, [selectedDistrict]);

  const fetchDistricts = async () => {
    try {
      const data = await api.districts();
      setDistricts(data);
    } catch (err) {
      console.error('Error fetching districts:', err);
    }
  };

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.dashboardSummary(selectedDistrict);
      setSummary(data);
    } catch (err) {
      console.error('Error fetching summary:', err);
      setError(err instanceof Error ? err.message : 'Failed to load dashboard summary');
    } finally {
      setLoading(false);
    }
  };

  const farmsByDistrictColumns = [
    {
      title: 'District',
      dataIndex: 'district_name',
      key: 'district_name',
    },
    {
      title: 'Code',
      dataIndex: 'district_code',
      key: 'district_code',
    },
    {
      title: 'Farms',
      dataIndex: 'farm_count',
      key: 'farm_count',
      align: 'right' as const,
    },
  ];

  const outbreaksByDiseaseColumns = [
    {
      title: 'Disease',
      dataIndex: 'disease_suspected',
      key: 'disease_suspected',
    },
    {
      title: 'Count',
      dataIndex: 'count',
      key: 'count',
      align: 'right' as const,
    },
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1>Dashboard</h1>
        
        <div>
          <label style={{ marginRight: 8, fontWeight: 500 }}>District:</label>
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
      </div>

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

      <Spin spinning={loading}>
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col xs={24} sm={8}>
            <Card>
              <Statistic
                title="Total Farms"
                value={summary?.total_farms ?? 0}
                prefix={<HomeOutlined />}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={8}>
            <Card>
              <Statistic
                title="Total Animals"
                value={summary?.total_animals ?? 0}
                prefix={<TeamOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={8}>
            <Card>
              <Statistic
                title="Open Outbreaks"
                value={summary?.open_outbreaks ?? 0}
                prefix={<WarningOutlined />}
                valueStyle={{ color: summary?.open_outbreaks ? '#cf1322' : '#3f8600' }}
              />
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <Card title="Farms by District">
              <Table
                dataSource={summary?.farms_by_district ?? []}
                columns={farmsByDistrictColumns}
                rowKey="district_code"
                pagination={false}
                size="small"
              />
            </Card>
          </Col>
          
          <Col xs={24} lg={12}>
            <Card title="Outbreaks by Disease">
              <Table
                dataSource={summary?.outbreaks_by_disease ?? []}
                columns={outbreaksByDiseaseColumns}
                rowKey="disease_suspected"
                pagination={false}
                size="small"
              />
            </Card>
          </Col>
        </Row>
      </Spin>
    </div>
  );
}
