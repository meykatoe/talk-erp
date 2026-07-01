import { apiGet } from './client';
import type { LowStockItem } from '../types/inventory';

export function fetchLowStock(params: { limit?: number }): Promise<LowStockItem[]> {
  return apiGet<LowStockItem[]>('/inventory/low-stock', params);
}
