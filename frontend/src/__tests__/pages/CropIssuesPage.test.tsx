import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import CropIssuesPage from '../../pages/CropIssuesPage';
import { api } from '../../lib/api';

// Mock the API module
jest.mock('../../lib/api', () => ({
  api: {
    districts: jest.fn(),
    cropIssues: jest.fn(),
    updateCropIssueStatus: jest.fn(),
  },
  APIError: class APIError extends Error {
    constructor(public status: number, message: string) {
      super(message);
      this.name = 'APIError';
    }
  },
}));

const mockDistricts = [
  { id: 1, name: 'Almaty Region', code: 'ALM' },
  { id: 2, name: 'Nur-Sultan Region', code: 'NUR' },
];

const mockCropIssues = [
  {
    id: 1,
    farm: 1,
    crop_type: 'wheat',
    problem_type: 'disease',
    problem_type_display: 'Disease',
    title: 'Rust disease on wheat',
    description: 'Severe rust disease affecting wheat crops',
    severity: 'high',
    severity_display: 'High',
    area_affected_ha: 5.5,
    status: 'new',
    status_display: 'New',
    reported_via: 'mobile',
    created_at: '2025-11-01T10:00:00Z',
    updated_at: '2025-11-01T10:00:00Z',
    farm_summary: {
      farm_id: 1,
      farmer_name: 'John Doe',
      village: 'Test Village',
      district_name: 'Almaty Region',
    },
  },
  {
    id: 2,
    farm: 2,
    crop_type: 'barley',
    problem_type: 'pest',
    problem_type_display: 'Pest',
    title: 'Aphid infestation',
    description: 'Aphids spreading across barley field',
    severity: 'medium',
    severity_display: 'Medium',
    area_affected_ha: 2.0,
    status: 'in_progress',
    status_display: 'In Progress',
    reported_via: 'mobile',
    created_at: '2025-11-02T10:00:00Z',
    updated_at: '2025-11-02T10:00:00Z',
    farm_summary: {
      farm_id: 2,
      farmer_name: 'Jane Smith',
      village: 'Another Village',
      district_name: 'Nur-Sultan Region',
    },
  },
];

describe('CropIssuesPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render page title and data on initial load', async () => {
    // Mock API responses
    (api.districts as jest.Mock).mockResolvedValue(mockDistricts);
    (api.cropIssues as jest.Mock).mockResolvedValue(mockCropIssues);

    render(
      <BrowserRouter>
        <CropIssuesPage />
      </BrowserRouter>
    );

    // Check page title
    expect(screen.getByText('Crop Issues')).toBeInTheDocument();

    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('wheat')).toBeInTheDocument();
    });

    // Check that farmer names are displayed
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();

    // Check that crop types are displayed
    expect(screen.getByText('wheat')).toBeInTheDocument();
    expect(screen.getByText('barley')).toBeInTheDocument();
  });

  it('should call API with filters when district and problem type are selected', async () => {
    // Mock API responses
    (api.districts as jest.Mock).mockResolvedValue(mockDistricts);
    (api.cropIssues as jest.Mock).mockResolvedValue(mockCropIssues);

    render(
      <BrowserRouter>
        <CropIssuesPage />
      </BrowserRouter>
    );

    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('wheat')).toBeInTheDocument();
    });

    // Clear the mock to check new calls
    (api.cropIssues as jest.Mock).mockClear();
    (api.cropIssues as jest.Mock).mockResolvedValue([mockCropIssues[0]]);

    // Find and click district filter
    const districtSelect = screen.getByPlaceholderText('All Districts');
    fireEvent.mouseDown(districtSelect);
    
    await waitFor(() => {
      const almOption = screen.getByText('Almaty Region');
      fireEvent.click(almOption);
    });

    // Verify API was called with district filter
    await waitFor(() => {
      expect(api.cropIssues).toHaveBeenCalledWith({ district: 'ALM' });
    });

    // Find and click problem type filter
    const problemTypeSelect = screen.getByPlaceholderText('All Problem Types');
    fireEvent.mouseDown(problemTypeSelect);
    
    await waitFor(() => {
      const diseaseOption = screen.getByText('Disease');
      fireEvent.click(diseaseOption);
    });

    // Verify API was called with both filters
    await waitFor(() => {
      expect(api.cropIssues).toHaveBeenCalledWith({ 
        district: 'ALM', 
        problem_type: 'disease' 
      });
    });
  });

  it('should update status when changed in the table', async () => {
    // Mock API responses
    (api.districts as jest.Mock).mockResolvedValue(mockDistricts);
    (api.cropIssues as jest.Mock).mockResolvedValue(mockCropIssues);
    (api.updateCropIssueStatus as jest.Mock).mockResolvedValue({
      ...mockCropIssues[0],
      status: 'in_progress',
      status_display: 'In Progress',
    });

    render(
      <BrowserRouter>
        <CropIssuesPage />
      </BrowserRouter>
    );

    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('wheat')).toBeInTheDocument();
    });

    // Find the status select for the first issue (wheat)
    const statusSelects = screen.getAllByRole('combobox');
    const firstStatusSelect = statusSelects.find((select) => 
      select.getAttribute('aria-activedescendant')?.includes('new') ||
      select.textContent?.includes('New')
    );

    if (firstStatusSelect) {
      // Click to open the select
      fireEvent.mouseDown(firstStatusSelect);
      
      // Wait for dropdown and click "In Progress"
      await waitFor(() => {
        const inProgressOptions = screen.getAllByText('In Progress');
        // Click the one in the dropdown (not in the table)
        fireEvent.click(inProgressOptions[inProgressOptions.length - 1]);
      });

      // Verify API was called
      await waitFor(() => {
        expect(api.updateCropIssueStatus).toHaveBeenCalledWith(1, 'in_progress');
      });
    }
  });

  it('should display error alert when API fails', async () => {
    // Mock API to reject
    (api.districts as jest.Mock).mockRejectedValue(new Error('Network error'));
    (api.cropIssues as jest.Mock).mockRejectedValue(new Error('Network error'));

    render(
      <BrowserRouter>
        <CropIssuesPage />
      </BrowserRouter>
    );

    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
    });

    // Check that error message is displayed
    expect(screen.getByText(/Failed to load data/i)).toBeInTheDocument();
  });

  it('should clear filters when Clear Filters button is clicked', async () => {
    // Mock API responses
    (api.districts as jest.Mock).mockResolvedValue(mockDistricts);
    (api.cropIssues as jest.Mock).mockResolvedValue(mockCropIssues);

    render(
      <BrowserRouter>
        <CropIssuesPage />
      </BrowserRouter>
    );

    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('wheat')).toBeInTheDocument();
    });

    // Clear the mock to check new calls
    (api.cropIssues as jest.Mock).mockClear();

    // Click "Clear Filters" button
    const clearButton = screen.getByText('Clear Filters');
    fireEvent.click(clearButton);

    // Verify API was called with no filters
    await waitFor(() => {
      expect(api.cropIssues).toHaveBeenCalledWith({});
    });
  });
});
