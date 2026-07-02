import { apiPost } from './client';
import type { StructuredQueryResult } from '../types/query';

export function postStructuredQuery(question: string): Promise<StructuredQueryResult> {
  return apiPost<StructuredQueryResult>('/query/structured', { question });
}
