import { apiGet } from './client';
import type { Order } from '../types/order';

export function fetchOrders(params: {
  customerId?: number;
  skip?: number;
  limit?: number;
}): Promise<Order[]> {
  return apiGet<Order[]>('/orders', {
    customer_id: params.customerId,
    skip: params.skip,
    limit: params.limit,
  });
}
