import { useState, useEffect } from 'react';
import { Card, Table, Tag, Select, Input, Button, Alert, Spin, Space, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { api, APIError } from '../lib/api';
import type { CropIssue, CropIssueStatus } from '../types/cropIssue';

interface District {
  id: number;
  name: string;
  code: string;
}

interface Filters {
  district?: string;
  crop_type?: string;
  problem_type?: string;
  severity?: string;
  status?: string;
}

export default function CropIssuesPage() {
  const [cropIssues, setCropIssues] = useState<CropIssue[]>([]);
  const [districts, setDistricts] = useState<District[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<Filters>({});
  const [updatingStatus, setUpdatingStatus] = useState<Record<number, boolean>>({});

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [districtsData, cropIssuesData] = await Promise.all([
        api.districts(),
        api.cropIssues()
      ]);
      setDistricts(districtsData);
      setCropIssues(cropIssuesData);
    } catch (err) {
      const errorMessage = err instanceof APIError 
        ? err.message 
        : 'Failed to load data';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const loadCropIssues = async (newFilters: Filters) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.cropIssues(newFilters);
      setCropIssues(data);
    } catch (err) {
      const errorMessage = err instanceof APIError 
        ? err.message 
        : 'Failed to load crop issues';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: keyof Filters, value: string | undefined) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    loadCropIssues(newFilters);
  };

  const handleClearFilters = () => {
    setFilters({});
    loadCropIssues({});
  };

  const handleStatusChange = async (cropIssue: CropIssue, newStatus: CropIssueStatus) => {
    const previousStatus = cropIssue.status;
    setUpdatingStatus(prev => ({ ...prev, [cropIssue.id]: true }));
    
    // Optimistically update UI
    setCropIssues(prev => 
      prev.map(issue => 
        issue.id === cropIssue.id 
          ? { ...issue, status: newStatus, status_display: getStatusDisplay(newStatus) }
          : issue
      )
    );

    try {
      await api.updateCropIssueStatus(cropIssue.id, newStatus);
      message.success('Status updated successfully');
    } catch (err) {
      // Revert on error
      setCropIssues(prev => 
        prev.map(issue => 
          issue.id === cropIssue.id 
            ? { ...issue, status: previousStatus, status_display: getStatusDisplay(previousStatus) }
            : issue
        )
      );
      message.error('Failed to update status');
    } finally {
      setUpdatingStatus(prev => ({ ...prev, [cropIssue.id]: false }));
    }
  };

  const getStatusDisplay = (status: CropIssueStatus): string => {
    const displays: Record<CropIssueStatus, string> = {
      'new': 'New',
      'in_progress': 'In Progress',
      'resolved': 'Resolved'
    };
    return displays[status];
  };

  const getSeverityColor = (severity: string): string => {
    const colors: Record<string, string> = {
      'high': 'red',
      'medium': 'orange',
      'low': 'blue'
    };
    return colors[severity] || 'default';
  };

  const getProblemTypeColor = (problemType: string): string => {
    const colors: Record<string, string> = {
      'pest': 'volcano',
      'disease': 'red',
      'nutrient_deficiency': 'orange',
      'water_stress': 'blue',
      'weed': 'green',
      'other': 'default'
    };
    return colors[problemType] || 'default';
  };

  const getStatusColor = (status: string): string => {
    const colors: Record<string, string> = {
      'new': 'red',
      'in_progress': 'orange',
      'resolved': 'green'
    };
    return colors[status] || 'default';
  };

  const columns: ColumnsType<CropIssue> = [
    {
      title: 'Date',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      render: (date: string) => new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }),
    },
    {
      title: 'Crop',
      dataIndex: 'crop_type',
      key: 'crop_type',
      width: 100,
      render: (crop: string) => (
        <Tag color="green">{crop}</Tag>
      ),
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
    },
    {
      title: 'Problem Type',
      dataIndex: 'problem_type',
      key: 'problem_type',
      width: 150,
      render: (problemType: string, record: CropIssue) => (
        <Tag color={getProblemTypeColor(problemType)}>
          {record.problem_type_display}
        </Tag>
      ),
    },
    {
      title: 'Severity',
      dataIndex: 'severity',
      key: 'severity',
      width: 100,
      render: (severity: string, record: CropIssue) => (
        <Tag color={getSeverityColor(severity)}>
          {record.severity_display}
        </Tag>
      ),
    },
    {
      title: 'Farm',
      key: 'farm',
      width: 200,
      render: (_: any, record: CropIssue) => (
        <div>
          <div style={{ fontWeight: 500 }}>{record.farm_summary.farmer_name}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            {record.farm_summary.village}, {record.farm_summary.district_name}
          </div>
        </div>
      ),
    },
    {
      title: 'Area (ha)',
      dataIndex: 'area_affected_ha',
      key: 'area_affected_ha',
      width: 100,
      align: 'right',
      render: (area: number | null) => area !== null ? area.toFixed(2) : '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 150,
      render: (status: CropIssueStatus, record: CropIssue) => (
        <Select
          value={status}
          onChange={(newStatus) => handleStatusChange(record, newStatus)}
          loading={updatingStatus[record.id]}
          disabled={updatingStatus[record.id]}
          style={{ width: '100%' }}
          size="small"
        >
          <Select.Option value="new">
            <Tag color={getStatusColor('new')}>New</Tag>
          </Select.Option>
          <Select.Option value="in_progress">
            <Tag color={getStatusColor('in_progress')}>In Progress</Tag>
          </Select.Option>
          <Select.Option value="resolved">
            <Tag color={getStatusColor('resolved')}>Resolved</Tag>
          </Select.Option>
        </Select>
      ),
    },
  ];

  return (
    <div>
      <h1 style={{ marginBottom: 24, fontSize: 28, fontWeight: 600, color: '#2d5016' }}>
        Crop Issues
      </h1>

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

      <Card style={{ marginBottom: 24 }}>
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
            <Select
              placeholder="All Districts"
              allowClear
              style={{ minWidth: 180 }}
              value={filters.district}
              onChange={(value) => handleFilterChange('district', value)}
            >
              {districts.map(d => (
                <Select.Option key={d.code} value={d.code}>
                  {d.name}
                </Select.Option>
              ))}
            </Select>

            <Input
              placeholder="Search crop type..."
              allowClear
              style={{ width: 200 }}
              value={filters.crop_type}
              onChange={(e) => handleFilterChange('crop_type', e.target.value || undefined)}
            />

            <Select
              placeholder="All Problem Types"
              allowClear
              style={{ minWidth: 180 }}
              value={filters.problem_type}
              onChange={(value) => handleFilterChange('problem_type', value)}
            >
              <Select.Option value="pest">Pest</Select.Option>
              <Select.Option value="disease">Disease</Select.Option>
              <Select.Option value="nutrient_deficiency">Nutrient Deficiency</Select.Option>
              <Select.Option value="water_stress">Water Stress</Select.Option>
              <Select.Option value="weed">Weed</Select.Option>
              <Select.Option value="other">Other</Select.Option>
            </Select>

            <Select
              placeholder="All Severities"
              allowClear
              style={{ minWidth: 150 }}
              value={filters.severity}
              onChange={(value) => handleFilterChange('severity', value)}
            >
              <Select.Option value="high">High</Select.Option>
              <Select.Option value="medium">Medium</Select.Option>
              <Select.Option value="low">Low</Select.Option>
            </Select>

            <Select
              placeholder="All Statuses"
              allowClear
              style={{ minWidth: 150 }}
              value={filters.status}
              onChange={(value) => handleFilterChange('status', value)}
            >
              <Select.Option value="new">New</Select.Option>
              <Select.Option value="in_progress">In Progress</Select.Option>
              <Select.Option value="resolved">Resolved</Select.Option>
            </Select>

            <Button onClick={handleClearFilters}>
              Clear Filters
            </Button>
          </div>
        </Space>
      </Card>

      <Card>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px 0' }}>
            <Spin size="large" />
            <div style={{ marginTop: 16, color: '#666' }}>Loading crop issues...</div>
          </div>
        ) : (
          <Table<CropIssue>
            columns={columns}
            dataSource={cropIssues}
            rowKey="id"
            pagination={{
              pageSize: 15,
              showSizeChanger: true,
              showTotal: (total) => `Total ${total} issues`,
            }}
            scroll={{ x: 1200 }}
          />
        )}
      </Card>
    </div>
  );
}
