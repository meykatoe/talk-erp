import { NavLink } from 'react-router-dom';

const NAV_ITEMS = [
  { to: '/products', label: '產品' },
  { to: '/orders', label: '訂單' },
  { to: '/inventory', label: '庫存' },
  { to: '/sales', label: '銷售彙總' },
  { to: '/query', label: '智能查詢' },
];

export function NavBar() {
  return (
    <nav className="navbar">
      <span className="navbar-brand">TalkERP</span>
      <ul className="navbar-links">
        {NAV_ITEMS.map((item) => (
          <li key={item.to}>
            <NavLink to={item.to} className={({ isActive }) => (isActive ? 'active' : undefined)}>
              {item.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
