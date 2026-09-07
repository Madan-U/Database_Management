/*
==============================================================================
File        : static/js/app.js
Location    : /data/database-management/static/js/app.js
Purpose     : Client-side JavaScript - dashboard interactivity, AJAX calls to the Flask API.
Author      : Madan U
Email       : madan.u@kotak.com
Created On  : 2026-09-07
Last Update : 2026-09-07
==============================================================================
*/

// ===== Demo Data (seed only — real data comes from /api/servers once backend is wired) =====
const DEMO_SERVERS = [
  { id: 1, hostname: 'mongo-prod-01', ip: '10.20.30.41', ssh_port: 22, db_port: 27017, environment: 'PROD', app_name: 'Stock Trading Platform', app_owner: 'Trading Platform Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '8.8', db_edition: 'Enterprise', db_version: '8.0.4', replica_set: 'rs0', replica_role: 'PRIMARY', cpu_cores: 8, ram_gb: 32, storage_gb: 500, status: 'online', last_check: '2026-08-26 14:32:11' },
  { id: 2, hostname: 'mongo-prod-02', ip: '10.20.30.42', ssh_port: 22, db_port: 27017, environment: 'PROD', app_name: 'Stock Trading Platform', app_owner: 'Trading Platform Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '8.8', db_edition: 'Enterprise', db_version: '8.0.4', replica_set: 'rs0', replica_role: 'SECONDARY', cpu_cores: 8, ram_gb: 32, storage_gb: 500, status: 'online', last_check: '2026-08-26 14:32:09' },
  { id: 3, hostname: 'mongo-prod-03', ip: '10.20.30.43', ssh_port: 22, db_port: 27017, environment: 'PROD', app_name: 'Stock Trading Platform', app_owner: 'Trading Platform Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '9.2', db_edition: 'Enterprise', db_version: '8.0.4', replica_set: 'rs0', replica_role: 'ARBITER', cpu_cores: 4, ram_gb: 16, storage_gb: 100, status: 'online', last_check: '2026-08-26 14:32:10' },
  { id: 4, hostname: 'mongo-uat-01', ip: '10.20.40.51', ssh_port: 22, db_port: 27017, environment: 'UAT', app_name: 'Risk Analytics', app_owner: 'Risk Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '8.6', db_edition: 'Community', db_version: '7.0.12', replica_set: 'rsUAT', replica_role: 'PRIMARY', cpu_cores: 4, ram_gb: 16, storage_gb: 200, status: 'online', last_check: '2026-08-26 14:31:55' },
  { id: 5, hostname: 'mongo-uat-02', ip: '10.20.40.52', ssh_port: 22, db_port: 27017, environment: 'UAT', app_name: 'Risk Analytics', app_owner: 'Risk Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '8.6', db_edition: 'Community', db_version: '7.0.12', replica_set: 'rsUAT', replica_role: 'SECONDARY', cpu_cores: 4, ram_gb: 16, storage_gb: 200, status: 'warning', last_check: '2026-08-26 14:31:58' },
  { id: 6, hostname: 'mongo-test-01', ip: '10.20.50.61', ssh_port: 22, db_port: 27017, environment: 'TEST', app_name: 'Payment Gateway', app_owner: 'Payments Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '9.2', db_edition: 'Community', db_version: '7.0.12', replica_set: '', replica_role: '', cpu_cores: 2, ram_gb: 8, storage_gb: 100, status: 'online', last_check: '2026-08-26 14:32:01' },
  { id: 7, hostname: 'mongo-dev-01', ip: '10.20.60.71', ssh_port: 22, db_port: 27017, environment: 'DEV', app_name: 'Customer Portal', app_owner: 'Web Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '9.2', db_edition: 'Community', db_version: '8.0.0', replica_set: '', replica_role: '', cpu_cores: 2, ram_gb: 8, storage_gb: 80, status: 'offline', last_check: '2026-08-26 14:20:33' },
  { id: 8, hostname: 'mongo-prod-04', ip: '10.20.30.44', ssh_port: 22, db_port: 27017, environment: 'PROD', app_name: 'Banking Core', app_owner: 'Core Banking Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '8.8', db_edition: 'Enterprise', db_version: '6.0.15', replica_set: 'rsBC', replica_role: 'PRIMARY', cpu_cores: 16, ram_gb: 64, storage_gb: 1000, status: 'online', last_check: '2026-08-26 14:32:05' },
  { id: 9, hostname: 'mongo-prod-05', ip: '10.20.30.45', ssh_port: 22, db_port: 27017, environment: 'PROD', app_name: 'Banking Core', app_owner: 'Core Banking Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '8.8', db_edition: 'Enterprise', db_version: '6.0.15', replica_set: 'rsBC', replica_role: 'SECONDARY', cpu_cores: 16, ram_gb: 64, storage_gb: 1000, status: 'online', last_check: '2026-08-26 14:32:07' },
  { id: 10, hostname: 'mongo-test-02', ip: '10.20.50.62', ssh_port: 22, db_port: 27017, environment: 'TEST', app_name: 'Reporting Service', app_owner: 'BI Team', server_owner: 'Infrastructure Team', os_type: 'RHEL', os_version: '8.6', db_edition: 'Community', db_version: '7.0.12', replica_set: '', replica_role: '', cpu_cores: 4, ram_gb: 16, storage_gb: 200, status: 'online', last_check: '2026-08-26 14:32:00' }
];

const DEMO_METRICS = {
  cpu_usage: 35, cpu_load: [1.25, 1.10, 0.95], ram_total: 32, ram_used: 18,
  disk_total: 500, disk_used: 280, disk_usage: 56, uptime: '42 days, 5 hrs',
  mongod_status: 'running', net_rx: '1.2 GB', net_tx: '0.8 GB'
};

const DEMO_HEALTH_CHECKS = [
  { name: 'MongoDB Service Running', status: 'pass', detail: 'mongod active (running)' },
  { name: 'Port Reachable', status: 'pass', detail: '27017/tcp open' },
  { name: 'Authentication Working', status: 'pass', detail: 'Auth enabled, keyFile valid' },
  { name: 'Replica Set Healthy', status: 'pass', detail: 'rs0: 3 members, all healthy' },
  { name: 'Primary Available', status: 'pass', detail: 'mongo-prod-01 is PRIMARY' },
  { name: 'Replication Lag', status: 'pass', detail: '0.8s (threshold: 10s)' },
  { name: 'Connections Usage', status: 'pass', detail: '832 / 2000 connections' },
  { name: 'Opcounters', status: 'pass', detail: 'insert: 1.2k/s, query: 4.5k/s' },
  { name: 'WiredTiger Cache', status: 'pass', detail: 'Used: 14.2 GB / 22.4 GB (63%)' },
  { name: 'Database Size', status: 'pass', detail: 'Total data size: 412 GB' },
  { name: 'Log Errors', status: 'pass', detail: 'No critical errors in last 24h' }
];

// ===== Session helpers =====
function getSession() {
  return JSON.parse(localStorage.getItem('dbi_session') || 'null');
}
function setSession(user) {
  localStorage.setItem('dbi_session', JSON.stringify(user));
}
function clearSession() {
  localStorage.removeItem('dbi_session');
}
function requireAuth() {
  if (!getSession()) window.location.href = './index.html';
}
function logout() {
  fetch(`${API_BASE ?? '/api'}/auth/logout`, { method: 'POST', credentials: 'same-origin' })
    .catch(() => {})
    .finally(() => {
      clearSession();
      window.location.href = './index.html';
    });
}

// ===== Role / Permission helpers =====
// Roles: Admin (full CRUD + user mgmt), DBA (view + run health checks), Viewer (read-only)
function isAdmin() {
  const u = getSession();
  return !!u && u.role === 'Admin';
}
function requireAdmin(actionLabel) {
  if (!isAdmin()) {
    showToast(`"${actionLabel}" ಮಾಡಲು Admin ಅನುಮತಿ ಬೇಕು. ನಿಮ್ಮ role: ${getSession()?.role || 'Unknown'}`, 'danger');
    return false;
  }
  return true;
}
// Call after sidebar/topbar mount on every page to hide admin-only controls for non-admins
function applyRoleVisibility() {
  const admin = isAdmin();
  document.querySelectorAll('.admin-only').forEach(el => {
    el.classList.toggle('d-none', !admin);
  });
}

// ===== Toast helper =====
function showToast(msg, type = 'success') {
  let box = document.getElementById('toastBox');
  if (!box) {
    box = document.createElement('div');
    box.id = 'toastBox';
    box.style.cssText = 'position:fixed;top:16px;right:16px;z-index:2000;display:flex;flex-direction:column;gap:8px;max-width:320px;';
    document.body.appendChild(box);
  }
  const el = document.createElement('div');
  el.className = `alert alert-${type} shadow-sm py-2 px-3 mb-0`;
  el.style.animation = 'slideUp .3s ease';
  el.textContent = msg;
  box.appendChild(el);
  setTimeout(() => el.remove(), 3200);
}

// ===== Render sidebar =====
function renderSidebar(activePage) {
  const user = getSession() || { name: 'Admin User', role: 'Admin' };
  const initials = user.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  return `
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-brand">
      <div class="brand-icon"><i class="bi bi-database-fill-gear"></i></div>
      <div>
        <div class="brand-text">DB Inventory</div>
        <div class="brand-sub">Monitoring Platform</div>
      </div>
    </div>
    <nav class="sidebar-nav">
      <div class="sidebar-section-label">Main</div>
      <a class="sidebar-link ${activePage === 'dashboard' ? 'active' : ''}" href="./dashboard.html">
        <i class="bi bi-grid-1x2-fill"></i> Dashboard
      </a>
      <div class="sidebar-section-label">Databases</div>
      <a class="sidebar-link ${activePage === 'mongodb' ? 'active' : ''}" href="./mongodb_inventory.html">
        <i class="bi bi-database-fill"></i> MongoDB
      </a>
      <a class="sidebar-link disabled" href="#" onclick="return false;">
        <i class="bi bi-database"></i> MSSQL <span class="badge bg-secondary ms-auto">Soon</span>
      </a>
      <a class="sidebar-link disabled" href="#" onclick="return false;">
        <i class="bi bi-database"></i> MySQL <span class="badge bg-secondary ms-auto">Soon</span>
      </a>
      <a class="sidebar-link disabled" href="#" onclick="return false;">
        <i class="bi bi-database"></i> MariaDB <span class="badge bg-secondary ms-auto">Soon</span>
      </a>
      <a class="sidebar-link disabled" href="#" onclick="return false;">
        <i class="bi bi-database"></i> PostgreSQL <span class="badge bg-secondary ms-auto">Soon</span>
      </a>
      <div class="sidebar-section-label admin-only d-none">System (Admin)</div>
      <a class="sidebar-link admin-only d-none ${activePage === 'users' ? 'active' : ''}" href="#" onclick="return false;">
        <i class="bi bi-people-fill"></i> Users
      </a>
      <a class="sidebar-link admin-only d-none ${activePage === 'settings' ? 'active' : ''}" href="#" onclick="return false;">
        <i class="bi bi-gear-fill"></i> Settings
      </a>
    </nav>
    <div class="sidebar-footer">
      <div class="sidebar-user">
        <div class="avatar">${initials}</div>
        <div class="user-info">
          <div class="user-name">${user.name}</div>
          <div class="user-role">${user.role}</div>
        </div>
        <button class="icon-btn" style="border:none;background:transparent;color:#94a3b8;" onclick="logout()" title="Logout">
          <i class="bi bi-box-arrow-right"></i>
        </button>
      </div>
    </div>
  </aside>`;
}

// ===== Render topbar =====
function renderTopbar(title) {
  const user = getSession() || {};
  return `
  <header class="topbar">
    <div class="d-flex align-items-center gap-2">
      <button class="icon-btn d-lg-none" onclick="document.getElementById('sidebar').classList.toggle('open')">
        <i class="bi bi-list"></i>
      </button>
      <div class="topbar-title">${title}</div>
    </div>
    <div class="topbar-actions">
      <span class="badge ${user.role === 'Admin' ? 'text-bg-success' : 'text-bg-secondary'}">${user.role || ''}</span>
      <button class="icon-btn" title="Notifications">
        <i class="bi bi-bell"></i>
        <span class="badge-dot"></span>
      </button>
      <button class="icon-btn" title="Refresh">
        <i class="bi bi-arrow-clockwise"></i>
      </button>
    </div>
  </header>`;
}

// ===== Status badge =====
function statusBadge(status) {
  const label = status.charAt(0).toUpperCase() + status.slice(1);
  return `<span class="status-badge status-${status}"><span class="dot"></span>${label}</span>`;
}
function envBadge(env) {
  return `<span class="env-badge env-${env}">${env}</span>`;
}
function roleBadge(role) {
  if (!role) return '<span class="text-muted">—</span>';
  return `<span class="role-badge role-${role}">${role}</span>`;
}

// ===== Export CSV =====
function exportCSV(filename, rows) {
  const csv = rows.map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

/* =========================================================================
   SERVER CRUD — calls the Flask backend REST API first
   (GET/POST/PUT/DELETE /api/servers) which is backed by PostgreSQL via
   services/inventory_service.py. If the API is not reachable (e.g. static
   preview / backend not running), it transparently falls back to
   localStorage so the frontend stays fully demo-able on its own.
   ========================================================================= */
const API_BASE = '/api';

function loadLocalServers() {
  const raw = localStorage.getItem('dbi_servers');
  if (raw) return JSON.parse(raw);
  localStorage.setItem('dbi_servers', JSON.stringify(DEMO_SERVERS));
  return JSON.parse(JSON.stringify(DEMO_SERVERS));
}
function saveLocalServers(list) {
  localStorage.setItem('dbi_servers', JSON.stringify(list));
}

async function apiGetServers() {
  try {
    const res = await fetch(`${API_BASE}/servers`, { credentials: 'same-origin' });
    if (!res.ok) throw new Error('api-fail');
    return await res.json();
  } catch (e) {
    return loadLocalServers();
  }
}

async function apiAddServer(payload) {
  try {
    const res = await fetch(`${API_BASE}/servers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify(payload)
    });
    if (res.status === 403) throw new Error('forbidden');
    if (!res.ok) throw new Error('api-fail');
    return await res.json();
  } catch (e) {
    if (e.message === 'forbidden') { showToast('Server ಸೇರಿಸಲು ಅನುಮತಿ ಇಲ್ಲ (Admin only).', 'danger'); throw e; }
    const list = loadLocalServers();
    const newId = list.length ? Math.max(...list.map(s => s.id)) + 1 : 1;
    const newServer = {
      id: newId,
      status: 'online',
      last_check: new Date().toISOString().replace('T', ' ').substring(0, 19),
      ...payload
    };
    list.push(newServer);
    saveLocalServers(list);
    return newServer;
  }
}

async function apiUpdateServer(id, payload) {
  try {
    const res = await fetch(`${API_BASE}/servers/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify(payload)
    });
    if (res.status === 403) throw new Error('forbidden');
    if (!res.ok) throw new Error('api-fail');
    return await res.json();
  } catch (e) {
    if (e.message === 'forbidden') { showToast('Server edit ಮಾಡಲು ಅನುಮತಿ ಇಲ್ಲ (Admin only).', 'danger'); throw e; }
    const list = loadLocalServers();
    const idx = list.findIndex(s => s.id === id);
    if (idx !== -1) list[idx] = { ...list[idx], ...payload };
    saveLocalServers(list);
    return list[idx];
  }
}

async function apiDeleteServer(id) {
  try {
    const res = await fetch(`${API_BASE}/servers/${id}`, { method: 'DELETE', credentials: 'same-origin' });
    if (res.status === 403) throw new Error('forbidden');
    if (!res.ok) throw new Error('api-fail');
    return true;
  } catch (e) {
    if (e.message === 'forbidden') { showToast('Server delete ಮಾಡಲು ಅನುಮತಿ ಇಲ್ಲ (Admin only).', 'danger'); throw e; }
    const list = loadLocalServers().filter(s => s.id !== id);
    saveLocalServers(list);
    return true;
  }
}

/* =========================================================================
   Add / Edit Server modal — shared across mongodb_inventory.html and
   server_detail.html. Call injectServerModals() once per page (into a
   mount div), then openServerModal(server) / confirmDeleteServer(id,name).
   ========================================================================= */
function injectServerModals(mountId) {
  document.getElementById(mountId).innerHTML = `
  <div class="modal fade" id="serverModal" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="serverModalTitle">Add Server</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <form id="serverForm" onsubmit="return false;">
            <input type="hidden" id="f_id" />
            <div class="row g-3">
              <div class="col-md-6"><label class="form-label">Hostname *</label><input class="form-control" id="f_hostname" required /></div>
              <div class="col-md-6"><label class="form-label">IP Address *</label><input class="form-control" id="f_ip" required /></div>
              <div class="col-md-4"><label class="form-label">SSH Port</label><input type="number" class="form-control" id="f_ssh_port" value="22" /></div>
              <div class="col-md-4"><label class="form-label">MongoDB Port</label><input type="number" class="form-control" id="f_db_port" value="27017" /></div>
              <div class="col-md-4"><label class="form-label">Environment</label>
                <select class="form-select" id="f_environment">
                  <option>PROD</option><option>UAT</option><option>TEST</option><option>DEV</option>
                </select>
              </div>
              <div class="col-md-6"><label class="form-label">Application Name *</label><input class="form-control" id="f_app_name" required /></div>
              <div class="col-md-6"><label class="form-label">Application Owner</label><input class="form-control" id="f_app_owner" /></div>
              <div class="col-md-6"><label class="form-label">Server Owner</label><input class="form-control" id="f_server_owner" /></div>
              <div class="col-md-3"><label class="form-label">OS Version</label><input class="form-control" id="f_os_version" placeholder="8.8" /></div>
              <div class="col-md-3"><label class="form-label">DB Edition</label>
                <select class="form-select" id="f_db_edition"><option>Community</option><option>Enterprise</option></select>
              </div>
              <div class="col-md-6"><label class="form-label">MongoDB Version</label><input class="form-control" id="f_db_version" placeholder="7.0.12" /></div>
              <div class="col-md-6"><label class="form-label">Replica Set Name</label><input class="form-control" id="f_replica_set" placeholder="rs0 (optional)" /></div>
              <div class="col-md-6"><label class="form-label">Replica Role</label>
                <select class="form-select" id="f_replica_role"><option value="">—</option><option>PRIMARY</option><option>SECONDARY</option><option>ARBITER</option></select>
              </div>
              <div class="col-md-4"><label class="form-label">CPU Cores</label><input type="number" class="form-control" id="f_cpu_cores" /></div>
              <div class="col-md-4"><label class="form-label">RAM (GB)</label><input type="number" class="form-control" id="f_ram_gb" /></div>
              <div class="col-md-4"><label class="form-label">Storage (GB)</label><input type="number" class="form-control" id="f_storage_gb" /></div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
          <button class="btn btn-primary" id="serverFormSave">Save</button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="deleteConfirmModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete Server</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <p><strong id="delServerName"></strong> ಅನ್ನು ಡಿಲೀಟ್ ಮಾಡಬೇಕೆ? ಈ ಕ್ರಿಯೆಯನ್ನು ಹಿಂತಿರುಗಿಸಲಾಗುವುದಿಲ್ಲ.</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
          <button class="btn btn-danger" id="confirmDeleteBtn">Delete</button>
        </div>
      </div>
    </div>
  </div>`;
}

const SERVER_FORM_FIELDS = ['id', 'hostname', 'ip', 'ssh_port', 'db_port', 'environment', 'app_name', 'app_owner', 'server_owner', 'os_version', 'db_edition', 'db_version', 'replica_set', 'replica_role', 'cpu_cores', 'ram_gb', 'storage_gb'];

function openServerModal(server = null) {
  if (!requireAdmin(server ? 'Edit Server' : 'Add Server')) return;
  document.getElementById('serverModalTitle').textContent = server ? `Edit Server — ${server.hostname}` : 'Add Server';
  SERVER_FORM_FIELDS.forEach(f => {
    const el = document.getElementById('f_' + f);
    if (!el) return;
    if (server) {
      el.value = server[f] ?? '';
    } else {
      el.value = f === 'ssh_port' ? 22 : f === 'db_port' ? 27017 : '';
    }
  });
  new bootstrap.Modal(document.getElementById('serverModal')).show();
}

async function saveServerForm(onSaved) {
  if (!requireAdmin(document.getElementById('f_id').value ? 'Edit Server' : 'Add Server')) return;
  const id = document.getElementById('f_id').value;
  const payload = {
    hostname: document.getElementById('f_hostname').value.trim(),
    ip: document.getElementById('f_ip').value.trim(),
    ssh_port: parseInt(document.getElementById('f_ssh_port').value) || 22,
    db_port: parseInt(document.getElementById('f_db_port').value) || 27017,
    environment: document.getElementById('f_environment').value,
    app_name: document.getElementById('f_app_name').value.trim(),
    app_owner: document.getElementById('f_app_owner').value.trim(),
    server_owner: document.getElementById('f_server_owner').value.trim(),
    os_type: 'RHEL',
    os_version: document.getElementById('f_os_version').value.trim(),
    db_edition: document.getElementById('f_db_edition').value,
    db_version: document.getElementById('f_db_version').value.trim(),
    replica_set: document.getElementById('f_replica_set').value.trim(),
    replica_role: document.getElementById('f_replica_role').value,
    cpu_cores: parseInt(document.getElementById('f_cpu_cores').value) || 0,
    ram_gb: parseInt(document.getElementById('f_ram_gb').value) || 0,
    storage_gb: parseInt(document.getElementById('f_storage_gb').value) || 0
  };
  if (!payload.hostname || !payload.ip || !payload.app_name) {
    showToast('Hostname, IP ಮತ್ತು Application Name ಅಗತ್ಯ.', 'danger');
    return;
  }
  try {
    if (id) {
      await apiUpdateServer(parseInt(id), payload);
      showToast(`${payload.hostname} ಯಶಸ್ವಿಯಾಗಿ update ಆಯಿತು.`);
    } else {
      await apiAddServer(payload);
      showToast(`${payload.hostname} ಯಶಸ್ವಿಯಾಗಿ ಸೇರಿಸಲಾಯಿತು.`);
    }
  } catch (e) {
    return; // permission error already toasted
  }
  bootstrap.Modal.getInstance(document.getElementById('serverModal')).hide();
  if (onSaved) onSaved();
}

let pendingDeleteId = null;
function confirmDeleteServer(id, name, onDeleted) {
  if (!requireAdmin('Delete Server')) return;
  pendingDeleteId = id;
  document.getElementById('delServerName').textContent = name;
  new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show();
  document.getElementById('confirmDeleteBtn').onclick = async () => {
    try {
      await apiDeleteServer(pendingDeleteId);
      showToast(`${name} ಡಿಲೀಟ್ ಆಯಿತು.`);
    } catch (e) {
      return;
    }
    bootstrap.Modal.getInstance(document.getElementById('deleteConfirmModal')).hide();
    if (onDeleted) onDeleted();
  };
}
