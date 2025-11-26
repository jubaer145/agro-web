// API Response Types for Events

export interface FarmSummary {
  farm_id: number;
  farmer_name: string;
  village: string;
  district_name: string;
}

export interface Event {
  id: number;
  farm: number;
  farm_summary: FarmSummary;
  event_type: 'vet_visit' | 'vaccination' | 'disease_report' | 'mortality';
  event_type_display: string;
  disease_suspected: string | null;
  description: string;
  animals_affected: number | null;
  status: 'new' | 'in_progress' | 'resolved';
  status_display: string;
  created_at: string;
}
