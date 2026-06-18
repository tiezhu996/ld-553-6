import { PileStatus, PileType } from '../constants/enums';

export interface ChargingPile {
  id: number;
  code: string;
  location: string;
  lat: string;
  lng: string;
  type: PileType;
  power: string;
  status: PileStatus;
  price_per_kwh: string;
  installed_at: string;
}
