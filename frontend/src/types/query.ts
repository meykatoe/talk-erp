export interface StructuredQueryResult {
  question: string;
  sql: string;
  columns: string[];
  rows: Record<string, unknown>[];
  answer: string;
}
