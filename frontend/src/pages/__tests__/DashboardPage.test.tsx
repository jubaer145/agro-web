/**
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import DashboardPage from '../DashboardPage';

const mockDistricts = [
  { id: 1, name: 'Almaty Region', code: 'ALM' },
  { id: 2, name: 'Nur-Sultan Region', code: 'NUR' }
];

const mockSummary = {
  total_farms: 10,
  total_animals: 1414,
  open_outbreaks: 2,
  farms_by_district: [
    { district_code: 'ALM', district_name: 'Almaty Region', farm_count: 5 },
    { district_code: 'NUR', district_name: 'Nur-Sultan Region', farm_count: 5 }
  ],
  outbreaks_by_disease: [
    { disease_suspected: 'Foot-and-mouth disease', count: 1 },
    { disease_suspected: 'Avian influenza', count: 1 }
  ]
};

const mockFetch = jest.fn();
global.fetch = mockFetch as any;

describe('DashboardPage', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('displays KPI cards with data', async () => {
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: async () => mockDistricts })
      .mockResolvedValueOnce({ ok: true, json: async () => mockSummary });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText('10')).toBeTruthy();
      expect(screen.getByText('1414')).toBeTruthy();
      expect(screen.getByText('2')).toBeTruthy();
    });
  });

  it('fetches summary with district filter', async () => {
    const filteredSummary = { ...mockSummary, total_farms: 5 };
    
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: async () => mockDistricts })
      .mockResolvedValueOnce({ ok: true, json: async () => mockSummary })
      .mockResolvedValueOnce({ ok: true, json: async () => filteredSummary });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith('/api/districts/');
      expect(mockFetch).toHaveBeenCalledWith('/api/dashboard/summary/');
    });
  });
});
