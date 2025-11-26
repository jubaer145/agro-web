import { useEffect, useState } from 'react';
import { Card, Spin, Alert, Row, Col, Statistic } from 'antd';
import { CheckCircleOutlined, ExclamationCircleOutlined } from '@ant-design/icons';

export default function DashboardPage() {
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/health/')
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        return res.json();
      })
      .then(data => {
        setStatus(data?.status ?? 'unknown');
        setError(null);
      })
      .catch(err => {
        setStatus('error');
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, []);

  const isHealthy = status === 'ok';

  return (
    <div>
      <h1>Dashboard</h1>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="API Status"
              value={loading ? 'Checking...' : status || 'Unknown'}
              prefix={loading ? <Spin size="small" /> : 
                     isHealthy ? <CheckCircleOutlined style={{ color: '#52c41a' }} /> : 
                     <ExclamationCircleOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ 
                color: loading ? '#1890ff' : 
                       isHealthy ? '#52c41a' : '#ff4d4f' 
              }}
            />
            <div data-testid="api-status" style={{ display: 'none' }}>
              {status}
            </div>
          </Card>
        </Col>
        
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="Total Farms"
              value={1234}
              suffix="registered"
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={12} md={8}>
          <Card>
            <Statistic
              title="Active Events"
              value={42}
              suffix="ongoing"
            />
          </Card>
        </Col>
      </Row>

      {error && (
        <Alert
          message="API Connection Error"
          description={error}
          type="error"
          showIcon
          style={{ marginTop: 16 }}
        />
      )}

      <Card title="System Overview" style={{ marginTop: 24 }}>
        <p>
          Welcome to the Akyl Jer Government Portal. This dashboard provides
          an overview of the agricultural and veterinary management system.
        </p>
        <ul>
          <li><strong>Farms:</strong> Manage farm registrations, inspections, and compliance</li>
          <li><strong>Events:</strong> Track veterinary visits, treatments, and health monitoring</li>
          <li><strong>API Status:</strong> Monitor backend service connectivity</li>
        </ul>
      </Card>
    </div>
  );
}
