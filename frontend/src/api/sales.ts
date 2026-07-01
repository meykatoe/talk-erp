import { apiGet } from './client';
import type { SalesSummary } from '../types/sales';

export function fetchSalesSummary(month: string): Promise<SalesSummary> {
  return apiGet<SalesSummary>('/sales/summary', { month });
}
