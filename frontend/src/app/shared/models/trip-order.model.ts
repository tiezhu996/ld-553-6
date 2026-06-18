import { OrderStatus, PaymentStatus } from '../constants/enums';
import { Vehicle } from './vehicle.model';

export interface TripOrder {
  id: number;
  order_no: string;
  user: number;
  vehicle?: number;
  vehicle_detail?: Vehicle;
  start_location: string;
  end_location: string;
  start_lat: string;
  start_lng: string;
  end_lat: string;
  end_lng: string;
  distance: string;
  duration: number;
  fare: string;
  status: OrderStatus;
  payment_status: PaymentStatus;
}
