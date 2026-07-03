function escapeCsvValue(value: unknown): string {
  const text = value === null || value === undefined ? '' : String(value);
  if (/[",\n]/.test(text)) {
    return `"${text.replace(/"/g, '""')}"`;
  }
  return text;
}

// BOM 讓 Excel 正確辨識 UTF-8，避免中文亂碼
export function downloadCsv(filename: string, columns: string[], rows: Record<string, unknown>[]): void {
  const lines = [columns, ...rows.map((row) => columns.map((col) => row[col]))].map((line) =>
    line.map(escapeCsvValue).join(','),
  );
  const blob = new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
