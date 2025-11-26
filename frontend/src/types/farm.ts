// API Response Types for Farm Registry

export interface District {
  id: number;
  name: string;
  code: string;
}

export interface Herd {
  id: number;
  animal_type: string;
  animal_type_display: string;
  headcount: number;
}

export interface Farm {
  id: number;
  farmer_name: string;
  phone: string;
  village: string;
  location_lat: number | null;
  location_lng: number | null;
  district: number;
  district_name: string;
  district_code: string;
  herds: Herd[];
  total_animals: number;
  created_at: string;
  updated_at: string;
}
