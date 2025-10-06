let token = null;

async function api(path, opts = {}) {
  const headers = opts.headers || {};
  if (token) headers["Authorization"] = "Bearer " + token;
  const res = await fetch("/api" + path, { ...opts, headers });
  if (res.status === 401) {
    alert("unauthorized");
  }
  return res.json();
}

document.getElementById("btnLogin").addEventListener("click", async () => {
  const u = document.getElementById("username").value;
  const p = document.getElementById("password").value;
  const r = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: u, password: p }),
  });
  const j = await r.json();
  if (r.ok) {
    token = j.token;
    alert("logged");
    loadTables();
  } else {
    alert(JSON.stringify(j));
  }
});

document.getElementById("startVision").addEventListener("click", async () => {
  await api("/vision/start", { method: "POST" });
});
document.getElementById("stopVision").addEventListener("click", async () => {
  await api("/vision/stop", { method: "POST" });
});
document.getElementById("connectRobot").addEventListener("click", async () => {
  await api("/robot/connect", { method: "POST" });
});

async function loadTables() {
  const r = await api("/tables");
  const grid = document.getElementById("tablesGrid");
  grid.innerHTML = "";
  r.tables.forEach((t) => {
    const d = document.createElement("div");
    d.className = "tableCard";
    d.innerHTML = `<strong>${t.table_number}</strong><div>${
      t.status || "unknown"
    }</div><div>${t.confidence_score || ""}</div>`;
    grid.appendChild(d);
  });
}
