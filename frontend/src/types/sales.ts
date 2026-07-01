export interface CategorySales {
  category: string;
  revenue: string;
}

export interface SalesSummary {
  month: string;
  total_orders: number;
  total_revenue: string;
  by_category: CategorySales[];
}
