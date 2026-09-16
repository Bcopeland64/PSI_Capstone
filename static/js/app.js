const API = "/api/tasks";
const listEl = document.getElementById("task-list");
const formEl = document.getElementById("task-form");

async function loadTasks() {
  const res = await fetch(API);
  const tasks = await res.json();
  listEl.innerHTML = "";
  tasks.forEach(t => {
    const li = document.createElement("li");
    li.className = t.done ? "done" : "";
    li.innerHTML =
      '<span>[' + t.priority + '] ' + t.title + '</span>' +
      '<button data-id="' + t.id + '" data-action="complete">done</button>' +
      '<button data-id="' + t.id + '" data-action="delete">x</button>';
    listEl.appendChild(li);
  });
}

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value.trim();
  const priority = document.getElementById("priority").value;
  if (!title) return;
  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: title, priority: priority })
  });
  formEl.reset();
  loadTasks();
});

listEl.addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;
  const id = btn.dataset.id;
  const action = btn.dataset.action;
  if (action === "complete") {
    await fetch(API + "/" + id + "/complete", { method: "POST" });
  } else if (action === "delete") {
    await fetch(API + "/" + id, { method: "DELETE" });
  }
  loadTasks();
});

loadTasks();
