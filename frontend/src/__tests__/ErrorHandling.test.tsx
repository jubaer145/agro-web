/**
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import FarmsPage from '../pages/FarmsPage';

const mockFetch = jest.fn();
global.fetch = mockFetch as any;

describe('Error Handling', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('displays error alert when API request fails', async () => {
    // Mock failed API requests
    mockFetch
      .mockRejectedValueOnce(new Error('Network error'))
      .mockRejectedValueOnce(new Error('Network error'));

    render(<FarmsPage />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to load/i)).toBeTruthy();
    });
  });
});
