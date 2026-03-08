const BASE = "http://127.0.0.1:8000";

interface Application {
  id: number;
  company: string;
  role: string;
  status: string;
  date_applied: string;
  salary_min: number | null;
  salary_max: number | null;
  notes: string | null;
}

// --- Helpers ---

function log(data: unknown) {
  const el = document.getElementById("response")!;
  el.textContent = JSON.stringify(data, null, 2);
}

function val(id: string): string {
  return (document.getElementById(id) as HTMLInputElement).value.trim();
}

function statusTag(status: string): string {
  const map: Record<string, string> = {
    "Applied": "tag-applied",
    "Phone Screen": "tag-phone",
    "Interview": "tag-interview",
    "Offer": "tag-offer",
    "Rejected": "tag-rejected",
  };
  const cls = map[status] ?? "tag-applied";
  return `<span class="tag ${cls}">${status}</span>`;
}

function renderTable(apps: Application[]) {
  const tbody = document.getElementById("apps-table-body")!;
  if (apps.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="empty">No applications found</td></tr>`;
    return;
  }
  tbody.innerHTML = apps.map(a => `
    <tr>
      <td>${a.id}</td>
      <td>${a.company}</td>
      <td>${a.role}</td>
      <td>${statusTag(a.status)}</td>
      <td>${a.date_applied}</td>
      <td>${a.salary_min != null ? `$${a.salary_min.toLocaleString()} – $${(a.salary_max ?? 0).toLocaleString()}` : "—"}</td>
      <td>${a.notes ?? "—"}</td>
    </tr>
  `).join("");
}

// --- API calls ---

async function createApplication() {
  const body = {
    company: val("c-company"),
    role: val("c-role"),
    status: val("c-status"),
    date_applied: val("c-date"),
    salary_min: val("c-sal-min") ? Number(val("c-sal-min")) : null,
    salary_max: val("c-sal-max") ? Number(val("c-sal-max")) : null,
    notes: val("c-notes") || null,
  };
  const res = await fetch(`${BASE}/applications/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  log(await res.json());
  await fetchAll();
}

async function fetchAll() {
  const res = await fetch(`${BASE}/applications/`);
  const data: Application[] = await res.json();
  log(data);
  renderTable(data);
}

async function fetchOne() {
  const id = val("r-id");
  const res = await fetch(`${BASE}/applications/${id}`);
  log(await res.json());
}

async function deleteApplication() {
  const id = val("r-id");
  const res = await fetch(`${BASE}/applications/${id}`, { method: "DELETE" });
  if (res.status === 204) {
    log({ message: `Application ${id} deleted` });
  } else {
    log(await res.json());
  }
  await fetchAll();
}

async function updateApplication() {
  const id = val("u-id");
  const status = val("u-status");
  const notes = val("u-notes");

  const body: Record<string, string> = {};
  if (status) body.status = status;
  if (notes) body.notes = notes;

  const res = await fetch(`${BASE}/applications/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  log(await res.json());
  await fetchAll();
}

// --- Wire up buttons ---

document.getElementById("btn-create")!.addEventListener("click", createApplication);
document.getElementById("btn-refresh")!.addEventListener("click", fetchAll);
document.getElementById("btn-get-one")!.addEventListener("click", fetchOne);
document.getElementById("btn-delete")!.addEventListener("click", deleteApplication);
document.getElementById("btn-update")!.addEventListener("click", updateApplication);
