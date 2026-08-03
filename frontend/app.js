const API_BASE = "http://127.0.0.1:8000";

// ---------- Token helpers ----------
function getToken() { return localStorage.getItem("token"); }
function setToken(t) { localStorage.setItem("token", t); }
function clearToken() { localStorage.removeItem("token"); }

function requireAuth() {
  if (!getToken()) window.location.href = "index.html";
}

function logout() {
  clearToken();
  window.location.href = "index.html";
}

// ---------- Generic API call ----------
async function apiFetch(path, options = {}) {
  const headers = options.headers || {};
  if (getToken()) headers["Authorization"] = `Bearer ${getToken()}`;
  if (options.body && !(options.body instanceof URLSearchParams)) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    clearToken();
    window.location.href = "index.html";
    return null;
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Request failed");
  }
  if (res.status === 204) return null;
  return res.json();
}

// ---------- Auth actions ----------
async function registerUser(name, email, password) {
  return apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ name, email, password }),
  });
}

async function loginUser(email, password) {
  // OAuth2PasswordRequestForm expects x-www-form-urlencoded with 'username' + 'password'
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const res = await fetch(`${API_BASE}/auth/login`, { method: "POST", body });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Login failed" }));
    throw new Error(err.detail || "Login failed");
  }
  const data = await res.json();
  setToken(data.access_token);
  return data;
}

// ---------- Project actions ----------
const getProjects = () => apiFetch("/projects");
const createProject = (name, description) =>
  apiFetch("/projects", { method: "POST", body: JSON.stringify({ name, description }) });
const updateProject = (id, updates) =>
  apiFetch(`/projects/${id}`, { method: "PUT", body: JSON.stringify(updates) });
const deleteProject = (id) => apiFetch(`/projects/${id}`, { method: "DELETE" });

// ---------- Task actions ----------
const getTasks = (projectId) => apiFetch(`/projects/${projectId}/tasks`);
const createTask = (projectId, task) =>
  apiFetch(`/projects/${projectId}/tasks`, { method: "POST", body: JSON.stringify(task) });
const updateTask = (id, updates) =>
  apiFetch(`/tasks/${id}`, { method: "PUT", body: JSON.stringify(updates) });
const deleteTask = (id) => apiFetch(`/tasks/${id}`, { method: "DELETE" });
const filterTasks = (status, priority) => {
  const params = new URLSearchParams();
  if (status) params.append("status", status);
  if (priority) params.append("priority", priority);
  return apiFetch(`/tasks/filter?${params.toString()}`);
};

// ---------- Dashboard ----------
const getDashboard = () => apiFetch("/dashboard");
