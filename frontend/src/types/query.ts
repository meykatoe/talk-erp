export interface ConversationTurn {
  question: string;
  answer: string;
}

export interface StructuredQueryResult {
  question: string;
  sql: string;
  columns: string[];
  rows: Record<string, unknown>[];
  answer: string;
  is_relevant: boolean;
}
