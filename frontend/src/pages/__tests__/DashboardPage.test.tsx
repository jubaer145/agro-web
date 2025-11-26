/**
 * @jest-environment jsdom
 */

import { render, screen, waitFor } from '@testing-library/react';
import DashboardPage from '../DashboardPage';

// Mock fetch globally
beforeEach(() => {
  (global as any).fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ status: 'ok' })
    } as Response)
  );
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('DashboardPage', () => {
  test('renders Dashboard title', () => {
    render(<DashboardPage />);
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  });

  test('calls /api/health/ and displays status', async () => {
    render(<DashboardPage />);
    
    // Wait for the API call to complete
    await waitFor(() => {
      const statusElement = screen.getByTestId('api-status');
      expect(statusElement).toBeInTheDocument();
    });
    
    // Check that the status is displayed
    const statusElement = screen.getByTestId('api-status');
    expect(statusElement.textContent).toBe('ok');
  });

  test('handles API error gracefully', async () => {
    // Mock a failed fetch
    (global as any).fetch = jest.fn(() =>
      Promise.reject(new Error('Network error'))
    );

    render(<DashboardPage />);
    
    await waitFor(() => {
      const statusElement = screen.getByTestId('api-status');
      expect(statusElement.textContent).toBe('error');
    });
  });

  test('displays system overview card', () => {
    render(<DashboardPage />);
    expect(screen.getByText(/System Overview/i)).toBeInTheDocument();
    expect(screen.getByText(/Akyl Jer Government Portal/i)).toBeInTheDocument();
  });
});
