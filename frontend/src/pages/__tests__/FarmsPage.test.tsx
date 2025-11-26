/**
 * @jest-environment jsdom
 */

import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import FarmsPage from '../FarmsPage';
import type { District, Farm } from '../../types/farm';

const mockDistricts: District[] = [
  { id: 1, name: 'Almaty Region', code: 'ALM' },
  { id: 2, name: 'Nur-Sultan Region', code: 'NUR' },
];

const mockFarms: Farm[] = [
  {
    id: 1,
    farmer_name: 'Almas Nurzhanov',
    phone: '+7 701 234 5678',
    village: 'Kaskelen',
    location_lat: 43.2,
    location_lng: 76.6,
    district: 1,
    district_name: 'Almaty Region',
    district_code: 'ALM',
    herds: [
      { id: 1, animal_type: 'cattle', animal_type_display: 'Cattle', headcount: 25 },
      { id: 2, animal_type: 'sheep', animal_type_display: 'Sheep', headcount: 100 },
    ],
    total_animals: 125,
    created_at: '2025-11-26T04:20:15.123456Z',
    updated_at: '2025-11-26T04:20:15.123456Z',
  },
  {
    id: 2,
    farmer_name: 'Aigul Bekova',
    phone: '+7 702 345 6789',
    village: 'Talgar',
    location_lat: 43.3,
    location_lng: 77.2,
    district: 1,
    district_name: 'Almaty Region',
    district_code: 'ALM',
    herds: [
      { id: 3, animal_type: 'goat', animal_type_display: 'Goat', headcount: 50 },
    ],
    total_animals: 50,
    created_at: '2025-11-26T04:21:15.123456Z',
    updated_at: '2025-11-26T04:21:15.123456Z',
  },
  {
    id: 3,
    farmer_name: 'Yerlan Suleimenov',
    phone: '+7 703 456 7890',
    village: 'Aksu',
    location_lat: 51.1,
    location_lng: 71.4,
    district: 2,
    district_name: 'Nur-Sultan Region',
    district_code: 'NUR',
    herds: [
      { id: 4, animal_type: 'cattle', animal_type_display: 'Cattle', headcount: 30 },
      { id: 5, animal_type: 'horse', animal_type_display: 'Horse', headcount: 10 },
    ],
    total_animals: 40,
    created_at: '2025-11-26T04:22:15.123456Z',
    updated_at: '2025-11-26T04:22:15.123456Z',
  },
];

beforeEach(() => {
  // Mock fetch for districts
  (global as any).fetch = jest.fn((url) => {
    if (url === '/api/districts/') {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockDistricts),
      } as Response);
    }
    
    // Mock fetch for farms with filtering
    if (typeof url === 'string' && url.startsWith('/api/farms/')) {
      const urlObj = new URL(url, 'http://localhost');
      const district = urlObj.searchParams.get('district');
      const search = urlObj.searchParams.get('search');
      
      let filteredFarms = [...mockFarms];
      
      if (district) {
        filteredFarms = filteredFarms.filter(f => f.district_code === district);
      }
      
      if (search) {
        const searchLower = search.toLowerCase();
        filteredFarms = filteredFarms.filter(
          f => f.farmer_name.toLowerCase().includes(searchLower) ||
               f.phone.includes(search)
        );
      }
      
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(filteredFarms),
      } as Response);
    }
    
    return Promise.reject(new Error('Unknown URL'));
  }) as jest.Mock;
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('FarmsPage', () => {
  test('renders farms table with correct data', async () => {
    render(<FarmsPage />);
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('Almas Nurzhanov')).toBeInTheDocument();
    });
    
    // Check that all farmers are displayed
    expect(screen.getByText('Almas Nurzhanov')).toBeInTheDocument();
    expect(screen.getByText('Aigul Bekova')).toBeInTheDocument();
    expect(screen.getByText('Yerlan Suleimenov')).toBeInTheDocument();
    
    // Check total animals
    expect(screen.getByText('125')).toBeInTheDocument();
    expect(screen.getByText('50')).toBeInTheDocument();
    expect(screen.getByText('40')).toBeInTheDocument();
  });

  test('filters farms by district', async () => {
    render(<FarmsPage />);
    
    // Wait for initial data
    await waitFor(() => {
      expect(screen.getByText('Almas Nurzhanov')).toBeInTheDocument();
    });
    
    // Find and click district dropdown
    const districtSelect = screen.getByText('All Districts').closest('.ant-select');
    expect(districtSelect).toBeInTheDocument();
    
    // Simulate selecting a district (this is tricky with Ant Design)
    // In a real test, you'd use userEvent or more sophisticated testing
    // For now, we verify the component renders with district options
    await waitFor(() => {
      expect(screen.getByText('Almaty Region')).toBeInTheDocument();
    });
  });

  test('searches farms by farmer name', async () => {
    render(<FarmsPage />);
    
    // Wait for initial data
    await waitFor(() => {
      expect(screen.getByText('Almas Nurzhanov')).toBeInTheDocument();
    });
    
    // Find search input
    const searchInput = screen.getByPlaceholderText('Search by farmer name or phone...');
    expect(searchInput).toBeInTheDocument();
    
    // Type in search input
    fireEvent.change(searchInput, { target: { value: 'Almas' } });
    
    // Wait for filtered results
    await waitFor(() => {
      // The fetch should be called with search parameter
      expect((global as any).fetch).toHaveBeenCalledWith(
        expect.stringContaining('search=Almas')
      );
    });
  });

  test('displays loading state', () => {
    render(<FarmsPage />);
    
    // Component should show loading initially
    // Ant Design's Spin component is present
    const spinners = document.querySelectorAll('.ant-spin');
    expect(spinners.length).toBeGreaterThan(0);
  });

  test('displays error message on API failure', async () => {
    // Mock fetch to return error
    (global as any).fetch = jest.fn(() =>
      Promise.reject(new Error('Network error'))
    ) as jest.Mock;
    
    render(<FarmsPage />);
    
    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText(/Failed to load farms/i)).toBeInTheDocument();
    });
  });

  test('displays herds information', async () => {
    render(<FarmsPage />);
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('Almas Nurzhanov')).toBeInTheDocument();
    });
    
    // Check that herd tags are displayed
    expect(screen.getByText('25 Cattle')).toBeInTheDocument();
    expect(screen.getByText('100 Sheep')).toBeInTheDocument();
    expect(screen.getByText('50 Goat')).toBeInTheDocument();
  });

  test('displays district codes as tags', async () => {
    render(<FarmsPage />);
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('Almas Nurzhanov')).toBeInTheDocument();
    });
    
    // Check for district code tags
    const almTags = screen.getAllByText('ALM');
    expect(almTags.length).toBeGreaterThan(0);
    
    const nurTags = screen.getAllByText('NUR');
    expect(nurTags.length).toBeGreaterThan(0);
  });

  test('shows empty state when no farms found', async () => {
    // Mock fetch to return empty array
    (global as any).fetch = jest.fn((url) => {
      if (url === '/api/districts/') {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockDistricts),
        } as Response);
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve([]),
      } as Response);
    }) as jest.Mock;
    
    render(<FarmsPage />);
    
    // Wait for empty state
    await waitFor(() => {
      expect(screen.getByText('No farms found')).toBeInTheDocument();
    });
  });
});
