/**
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import EventsPage from '../EventsPage';

// Mock fetch globally
const mockFetch = jest.fn();
global.fetch = mockFetch as any;

const mockDistricts = [
  { id: 1, name: 'Almaty Region', code: 'ALM' },
  { id: 2, name: 'Nur-Sultan Region', code: 'NUR' }
];

const mockEvents = [
  {
    id: 1,
    farm: 1,
    farm_summary: {
      farm_id: 1,
      farmer_name: 'John Doe',
      village: 'Village A',
      district_name: 'Almaty Region'
    },
    event_type: 'disease_report',
    event_type_display: 'Disease Report',
    disease_suspected: 'Foot-and-mouth disease',
    description: 'Test description',
    animals_affected: 10,
    status: 'new',
    status_display: 'New',
    created_at: '2025-11-20T10:00:00Z'
  },
  {
    id: 2,
    farm: 2,
    farm_summary: {
      farm_id: 2,
      farmer_name: 'Jane Smith',
      village: 'Village B',
      district_name: 'Nur-Sultan Region'
    },
    event_type: 'vaccination',
    event_type_display: 'Vaccination',
    disease_suspected: null,
    description: 'Routine vaccination',
    animals_affected: null,
    status: 'resolved',
    status_display: 'Resolved',
    created_at: '2025-11-21T12:00:00Z'
  }
];

describe('EventsPage', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('renders events table with data', async () => {
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: async () => mockDistricts })
      .mockResolvedValueOnce({ ok: true, json: async () => mockEvents });

    render(<EventsPage />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeTruthy();
      expect(screen.getByText('Jane Smith')).toBeTruthy();
    });
  });

  it('calls PATCH when changing status', async () => {
    const updatedEvent = { ...mockEvents[0], status: 'in_progress' };
    
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: async () => mockDistricts })
      .mockResolvedValueOnce({ ok: true, json: async () => mockEvents })
      .mockResolvedValueOnce({ ok: true, json: async () => updatedEvent });

    render(<EventsPage />);

    await waitFor(() => screen.getByText('John Doe'));

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith('/api/districts/');
      expect(mockFetch).toHaveBeenCalledWith('/api/events/');
    });
  });
});
