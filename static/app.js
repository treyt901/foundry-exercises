// Front-end logic for the Foundry Prompt Lab.
// Loads the challenge definitions from the Flask back end, lets the student
// write prompts, and renders the grade + feedback that /api/grade returns.

const bannerEl = document.getElementById("config-banner");
const statusEl = document.getElementById("status");
const gradeBtn = document.getElementById("grade-btn");

const systemEditor = document.getElementById("editor-system");
const systemInput = document.getElementById("system-prompt");
const userEditor = document.getElementById("editor-user");
const userInput = document.getElementById("user-prompt");
const fixedSystemBox = document.getElementById("fixed-system");
const fixedTestsBox = document.getElementById("fixed-tests");
const resultsEl = document.getElementById("results");

let passScore = 70;
let challenges = [];
let current = null;

// --- Small helpers -----------------------------------------------------------

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function setList(id, items) {
  const list = document.getElementById(id);
  list.innerHTML = "";
  for (const item of items) list.appendChild(el("li", "", item));
}

function setBusy(busy) {
  gradeBtn.disabled = busy;
  statusEl.textContent = busy
    ? "Running your prompts and grading… this takes a little while."
    : "";
}

// Each challenge lives at its own URL (/challenge/1, /2, /3) and there is no
// in-app navigation: the Codio guide opens the right page for each challenge.

function selectChallenge(id) {
  current = challenges.find((c) => c.id === id) || challenges[0];

  document.getElementById("challenge-title").textContent =
    `Challenge ${current.id} — ${current.title}`;
  document.getElementById("challenge-goal").textContent = current.goal;
  document.getElementById("challenge-scenario").textContent = current.scenario;
  setList("requirements", current.requirements);

  // Rubric.
  const rubricEl = document.getElementById("rubric");
  rubricEl.innerHTML = "";
  for (const item of current.rubric) {
    const li = el("li");
    li.appendChild(el("strong", "", `${item.name} (${item.max} pts): `));
    li.appendChild(document.createTextNode(item.description));
    rubricEl.appendChild(li);
  }

  // Attachment (challenge 3's customer message).
  const attachmentBox = document.getElementById("attachment-box");
  if (current.attachment) {
    document.getElementById("attachment-label").textContent =
      current.attachment_label || "Provided text";
    document.getElementById("attachment-text").textContent = current.attachment;
    attachmentBox.classList.remove("hidden");
  } else {
    attachmentBox.classList.add("hidden");
  }

  // Which editors does this challenge use?
  const writesSystem = current.write.includes("system");
  const writesUser = current.write.includes("user");
  systemEditor.classList.toggle("hidden", !writesSystem);
  userEditor.classList.toggle("hidden", !writesUser);

  // The side the student doesn't write is shown read-only.
  if (!writesSystem && current.fixed_system_prompt) {
    document.getElementById("fixed-system-text").textContent =
      current.fixed_system_prompt;
    fixedSystemBox.classList.remove("hidden");
  } else {
    fixedSystemBox.classList.add("hidden");
  }
  if (!writesUser && current.test_messages) {
    const list = document.getElementById("fixed-tests-list");
    list.innerHTML = "";
    for (const message of current.test_messages) {
      list.appendChild(el("li", "", message));
    }
    fixedTestsBox.classList.remove("hidden");
  } else {
    fixedTestsBox.classList.add("hidden");
  }

  userInput.placeholder = current.weak_prompt
    ? `Improve on: "${current.weak_prompt}"`
    : "Type the message you want to send to the model…";

  // Restore the draft for this challenge. Each challenge is its own page and
  // Codio reloads the preview when students move through the guide, so drafts
  // are kept in localStorage to survive the navigation.
  const draft = loadDraft(current.id);
  systemInput.value = draft.system;
  userInput.value = draft.user;

  resultsEl.classList.add("hidden");
  statusEl.textContent = "";
}

function draftKey(id) {
  return `prompt-lab-draft-${id}`;
}

function loadDraft(id) {
  try {
    const raw = localStorage.getItem(draftKey(id));
    if (raw) return { system: "", user: "", ...JSON.parse(raw) };
  } catch (err) {
    /* private windows etc. — start blank */
  }
  return { system: "", user: "" };
}

function saveDraft() {
  if (!current) return;
  try {
    localStorage.setItem(
      draftKey(current.id),
      JSON.stringify({ system: systemInput.value, user: userInput.value })
    );
  } catch (err) {
    /* storage unavailable — drafts just won't persist */
  }
}

systemInput.addEventListener("input", saveDraft);
userInput.addEventListener("input", saveDraft);

// --- Rendering a grade -------------------------------------------------------

function renderGrade(data) {
  resultsEl.classList.remove("hidden");

  document.getElementById("total-score").textContent = data.total;
  const chip = document.getElementById("pass-chip");
  chip.textContent = data.passed ? "PASSED" : "KEEP REFINING";
  chip.className = "chip " + (data.passed ? "chip-pass" : "chip-fail");
  document.getElementById("pass-note").textContent = data.passed
    ? "Nice — this challenge is done. Your best score is saved and counts toward your grade when you mark the assignment complete."
    : `You need ${data.pass_score} or more to pass. Use the feedback below, edit, and run again.`;

  // Per-criterion bars.
  const barsEl = document.getElementById("score-bars");
  barsEl.innerHTML = "";
  for (const item of data.scores) {
    const row = el("div", "bar-row");
    row.appendChild(el("span", "bar-label", item.name));
    const track = el("div", "bar-track");
    const fill = el("div", "bar-fill");
    const pct = item.max ? Math.round((item.score / item.max) * 100) : 0;
    fill.style.width = pct + "%";
    fill.classList.add(pct >= 80 ? "good" : pct >= 50 ? "ok" : "low");
    track.appendChild(fill);
    row.appendChild(track);
    row.appendChild(el("span", "bar-score", `${item.score}/${item.max}`));
    barsEl.appendChild(row);
  }

  const noteEl = document.getElementById("note");
  if (data.note) {
    noteEl.textContent = data.note;
    noteEl.classList.remove("hidden");
  } else {
    noteEl.classList.add("hidden");
  }

  setList("strengths", data.strengths.length ? data.strengths : ["—"]);
  setList("improvements", data.improvements.length ? data.improvements : ["—"]);

  // Transcripts.
  const transcriptsEl = document.getElementById("transcripts");
  transcriptsEl.innerHTML = "";
  for (const t of data.transcripts) {
    const convo = el("div", "convo");
    const userMsg = el("div", "msg user");
    userMsg.appendChild(el("div", "bubble", t.user));
    const botMsg = el("div", "msg assistant");
    botMsg.appendChild(el("div", "bubble", t.assistant));
    convo.appendChild(userMsg);
    convo.appendChild(botMsg);
    transcriptsEl.appendChild(convo);
  }

  // Format check (challenge 3).
  const fcEl = document.getElementById("format-check");
  if (data.format_check) {
    const fc = data.format_check;
    const parts = [];
    parts.push(fc.reply_is_valid_json ? "✔ reply parses as JSON" : "✘ reply is not valid JSON");
    parts.push(
      fc.reply_is_json_only
        ? "✔ nothing but JSON in the reply"
        : "✘ extra text or a code fence surrounds the JSON"
    );
    parts.push(
      fc.missing_keys.length === 0
        ? "✔ all required keys present"
        : "✘ missing keys: " + fc.missing_keys.join(", ")
    );
    if (fc.extra_keys.length) parts.push("⚠ unexpected keys: " + fc.extra_keys.join(", "));
    fcEl.textContent = "Automatic format check — " + parts.join("  ·  ");
    fcEl.classList.remove("hidden");
  } else {
    fcEl.classList.add("hidden");
  }

  resultsEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// --- Grading -----------------------------------------------------------------

gradeBtn.addEventListener("click", async () => {
  if (!current) return;
  saveDraft();
  setBusy(true);
  try {
    const res = await fetch("/api/grade", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        challenge_id: current.id,
        system_prompt: systemInput.value,
        user_prompt: userInput.value,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      statusEl.textContent = data.error || "Something went wrong.";
      return;
    }
    renderGrade(data);
  } catch (err) {
    statusEl.textContent = "Could not reach the server: " + err.message;
  } finally {
    gradeBtn.disabled = false;
    // Clear the "Running…" message, but keep any error we just showed.
    if (statusEl.textContent.startsWith("Running")) statusEl.textContent = "";
  }
});

// --- Boot --------------------------------------------------------------------

async function boot() {
  try {
    const health = await (await fetch("/api/health")).json();
    passScore = health.pass_score || passScore;
    if (!health.configured) {
      bannerEl.textContent =
        "Not configured yet. Add these to your .env file and restart the app: " +
        health.missing.join(", ");
      bannerEl.classList.remove("hidden");
    }
  } catch (err) {
    /* the first grade attempt will surface the real error */
  }

  try {
    const challengeData = await (await fetch("/api/challenges")).json();
    passScore = challengeData.pass_score || passScore;
    challenges = challengeData.challenges;
    // The Flask route tells the page which challenge it serves.
    selectChallenge(Number(window.CHALLENGE_ID) || challenges[0].id);
  } catch (err) {
    bannerEl.textContent = "Could not load the challenges: " + err.message;
    bannerEl.classList.remove("hidden");
  }
}

boot();
