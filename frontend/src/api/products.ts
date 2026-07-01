import { apiGet } from './client';
import type { Product } from '../types/product';

export function fetchProducts(params: { skip?: number; limit?: number }): Promise<Product[]> {
  return apiGet<Product[]>('/products', params);
}
