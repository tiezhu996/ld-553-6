export interface MaintenanceRecord {
  id: number;
  vehicle: number;
  plate_number: string;
  type: string;
  description: string;
  cost: string;
  start_date: string;
  end_date?: string;
  status: 'IN_PROGRESS' | 'COMPLETED';
}
