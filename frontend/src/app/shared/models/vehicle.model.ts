import { VehicleStatus, VehicleType } from '../constants/enums';

export interface Vehicle {
  id: number;
  plate_number: string;
  type: VehicleType;
  brand: string;
  model: string;
  year: number;
  status: VehicleStatus;
  driver?: number;
  driver_detail?: { id: number; username: string; role: string };
  insurance_expiry: string;
  lat: string;
  lng: string;
}
