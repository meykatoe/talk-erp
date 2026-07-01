export interface Order {
  salesorderid: number;
  customerid: number;
  orderdate: string;
  duedate: string;
  shipdate: string | null;
  status: number;
  subtotal: string;
  taxamt: string;
  freight: string;
  totaldue: string | null;
}
