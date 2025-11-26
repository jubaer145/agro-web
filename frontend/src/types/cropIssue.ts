// API Response Types for Crop Issues

export interface CropIssueFarmSummary {
  farm_id: number;
  farmer_name: string;
  village: string;
  district_name: string;
}

export type CropProblemType =
  | 'pest'
  | 'disease'
  | 'nutrient_deficiency'
  | 'water_stress'
  | 'weed'
  | 'other';

export type CropIssueSeverity = 'low' | 'medium' | 'high';
export type CropIssueStatus = 'new' | 'in_progress' | 'resolved';

export interface CropIssue {
  id: number;
  farm: number;
  crop_type: string;
  problem_type: CropProblemType;
  problem_type_display: string;
  title: string;
  description: string;
  severity: CropIssueSeverity;
  severity_display: string;
  area_affected_ha: number | null;
  status: CropIssueStatus;
  status_display: string;
  reported_via: string;
  created_at: string;
  updated_at: string;
  farm_summary: CropIssueFarmSummary;
}
