import { Layout, Menu } from 'antd';
import { Link, Routes, Route, useLocation } from 'react-router-dom';
import { DashboardOutlined, HomeOutlined, AlertOutlined, EnvironmentOutlined } from '@ant-design/icons';
import DashboardPage from './pages/DashboardPage';
import FarmsPage from './pages/FarmsPage';
import EventsPage from './pages/EventsPage';
import './App.css';

const { Header, Sider, Content } = Layout;

export default function App() {
  const location = useLocation();
  const getSelectedKey = () => {
    if (location.pathname.startsWith('/farms')) return 'farms';
    if (location.pathname.startsWith('/events')) return 'events';
    return 'dashboard';
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider 
        width={240}
        style={{
          background: '#2d5016',
        }}
      >
        <div style={{ 
          color: '#fff', 
          padding: '20px 16px',
          fontSize: '20px', 
          fontWeight: 'bold',
          textAlign: 'center',
          borderBottom: '1px solid #3d6826',
          background: '#234012',
        }}>
          <EnvironmentOutlined style={{ marginRight: 8, fontSize: 24 }} />
          Акыл Жер
        </div>
        <div style={{ 
          padding: '12px 16px',
          fontSize: '12px',
          color: '#9fbd87',
          textAlign: 'center',
          borderBottom: '1px solid #3d6826'
        }}>
          Agricultural Management System
        </div>
        <Menu 
          theme="dark" 
          mode="inline" 
          selectedKeys={[getSelectedKey()]}
          style={{ 
            background: '#2d5016',
            borderRight: 'none'
          }}
          items={[
            {
              key: 'dashboard',
              icon: <DashboardOutlined />,
              label: <Link to="/dashboard">Dashboard</Link>,
            },
            {
              key: 'farms',
              icon: <HomeOutlined />,
              label: <Link to="/farms">Farms Registry</Link>,
            },
            {
              key: 'events',
              icon: <AlertOutlined />,
              label: <Link to="/events">Events & Outbreaks</Link>,
            },
          ]}
        />
      </Sider>
      <Layout>
        <Header style={{ 
          background: '#f7f9f5', 
          padding: '0 24px',
          borderBottom: '2px solid #52c41a',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <h2 style={{ margin: 0, color: '#2d5016', fontWeight: 600 }}>
              Акыл Жер Government Portal
            </h2>
          </div>
          <div style={{ color: '#52c41a', fontSize: 12 }}>
            🌾 Agricultural & Veterinary Management
          </div>
        </Header>
        <Content style={{ 
          margin: '24px', 
          padding: '24px', 
          background: '#fff',
          borderRadius: '8px',
          boxShadow: '0 1px 2px rgba(0,0,0,0.06)'
        }}>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/farms" element={<FarmsPage />} />
            <Route path="/events" element={<EventsPage />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
}
