import { apiPost } from './client';
import type { ConversationTurn, StructuredQueryResult } from '../types/query';

export function postStructuredQuery(
  question: string,
  history: ConversationTurn[],
): Promise<StructuredQueryResult> {
  return apiPost<StructuredQueryResult>('/query/structured', { question, history });
}
