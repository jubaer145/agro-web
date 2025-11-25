import React from 'react';
import { Layout, Menu } from 'antd';
import { Link, Routes, Route, useLocation } from 'react-router-dom';
import { DashboardOutlined, HomeOutlined, CalendarOutlined } from '@ant-design/icons';
import DashboardPage from './pages/DashboardPage';
import FarmsPage from './pages/FarmsPage';
import EventsPage from './pages/EventsPage';
import './App.css';

const { Header, Sider, Content } = Layout;

export default function App() {
  const location = useLocation();
  const getSelectedKey = () => {
    if (location.pathname.startsWith('/farms')) return '2';
    if (location.pathname.startsWith('/events')) return '3';
    return '1';
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={240}>
        <div style={{ 
          color: 'white', 
          padding: '16px', 
          fontSize: '18px', 
          fontWeight: 'bold',
          textAlign: 'center',
          borderBottom: '1px solid #303030'
        }}>
          Akyl Jer
        </div>
        <Menu theme="dark" mode="inline" selectedKeys={[getSelectedKey()]}>
          <Menu.Item key="1" icon={<DashboardOutlined />}>
            <Link to="/dashboard">Dashboard</Link>
          </Menu.Item>
          <Menu.Item key="2" icon={<HomeOutlined />}>
            <Link to="/farms">Farms</Link>
          </Menu.Item>
          <Menu.Item key="3" icon={<CalendarOutlined />}>
            <Link to="/events">Events</Link>
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Header style={{ 
          background: '#fff', 
          paddingLeft: '24px',
          borderBottom: '1px solid #f0f0f0'
        }}>
          <h2 style={{ margin: 0, color: '#001529' }}>
            Akyl Jer Government Portal
          </h2>
        </Header>
        <Content style={{ margin: '24px', padding: '24px', background: '#fff' }}>
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
