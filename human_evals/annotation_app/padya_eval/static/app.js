// Padya-eval: progressive enhancements only. Every page works without this file.
(function () {
  "use strict";

  function store(op, key, value) {
    try {
      if (op === "get") return window.localStorage.getItem(key);
      if (op === "set") window.localStorage.setItem(key, value);
      if (op === "del") window.localStorage.removeItem(key);
    } catch (e) { /* private mode or storage blocked: features degrade silently */ }
    return null;
  }

  // ---------- light / dark mode ----------
  function setTheme(dark) {
    if (dark) document.documentElement.dataset.theme = "dark"; else delete document.documentElement.dataset.theme;
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", dark ? "#16130f" : "#f7f3ec");
    store("set", "padya-theme", dark ? "dark" : "light");
  }
  if (document.documentElement.dataset.theme === "dark") setTheme(true);
  document.addEventListener("click", function (ev) {
    if (ev.target.closest("[data-theme-toggle]")) setTheme(document.documentElement.dataset.theme !== "dark");
  });

  // ---------- ruleset reference in a dialog ----------
  var dialog = document.getElementById("ref-dialog");
  var body = document.getElementById("ref-dialog-body");
  var loaded = {};

  function openReference(src) {
    if (!dialog || typeof dialog.showModal !== "function") return false;
    dialog.showModal();
    if (loaded[src]) { body.innerHTML = loaded[src]; return true; }
    body.innerHTML = '<p class="muted">Loading…</p>';
    fetch(src, { credentials: "same-origin" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (html) { loaded[src] = html; body.innerHTML = html; body.scrollTop = 0; })
      .catch(function () { body.innerHTML = '<p class="alert">Could not load the ruleset. Use the "Full page" link above.</p>'; });
    return true;
  }

  document.addEventListener("click", function (ev) {
    var opener = ev.target.closest("[data-ref-open]");
    if (opener && opener.dataset.refSrc && openReference(opener.dataset.refSrc)) { ev.preventDefault(); return; }
    if (ev.target.closest("[data-ref-close]") && dialog) { dialog.close(); return; }
    var toc = ev.target.closest(".ref-dialog .ref-toc a");
    if (toc) {
      var target = body.querySelector(toc.getAttribute("href"));
      if (target) { ev.preventDefault(); target.scrollIntoView({ behavior: "smooth", block: "start" }); }
      return;
    }
    // touch screens have no hover tooltips: show the cell's note in a toast instead
    var cell = ev.target.closest(".gana-table [data-tip]");
    if (cell && !(window.matchMedia && window.matchMedia("(hover: hover)").matches)) { showTip(cell.dataset.tip); }
  });
  if (dialog) {
    dialog.addEventListener("click", function (ev) { if (ev.target === dialog) dialog.close(); });   // backdrop
  }

  // ---------- akshara tips (tap on phones, where title tooltips don't show) ----------
  var tip = document.getElementById("tip");
  var tipTimer = null;
  function showTip(text) {
    if (!tip) return;
    tip.textContent = text;
    tip.hidden = false;
    clearTimeout(tipTimer);
    tipTimer = setTimeout(function () { tip.hidden = true; }, 4000);
  }

  // ---------- copy the poem's lines (the button's data-copy) ----------
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {     // plain http: the old way, through a hidden textarea
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { /* unsupported */ }
      document.body.removeChild(ta);
      if (ok) resolve(); else reject();
    });
  }
  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-copy]");
    if (!btn) return;
    copyText(btn.dataset.copy).then(
      function () { showTip("పద్యం కాపీ అయింది · Poem copied"); },
      function () { showTip("కాపీ కాలేదు: పద్యాన్ని ఎంచుకుని కాపీ చేయండి · Could not copy: select the poem and copy it"); });
  });

  // ---------- look up the selected word in the Andhrabharati dictionary (the link's data-dict-lookup) ----------
  // On phones a tap on the button can clear the selection first, so the last selection made is remembered.
  var DICT_URL = "https://andhrabharati.com/dictionary/index.php?w=";
  var lastSelection = "";
  function selectedWord() {
    var s = window.getSelection ? String(window.getSelection()).trim() : "";
    s = (s || lastSelection).replace(/[\s​]+/g, " ").trim();
    try { s = s.replace(/^[\p{P}\p{S}\p{N}\s]+|[\p{P}\p{S}\p{N}\s]+$/gu, ""); }   // !, ?, dandas, digits at the ends
    catch (e) { s = s.replace(/^[\s!?,.;:'"()\-–—।॥|0-9]+|[\s!?,.;:'"()\-–—।॥|0-9]+$/g, ""); }
    return s;
  }
  document.addEventListener("selectionchange", function () {
    var s = window.getSelection ? String(window.getSelection()).trim() : "";
    if (s) lastSelection = s;
  });
  document.addEventListener("click", function (ev) {
    var link = ev.target.closest("[data-dict-lookup]");
    if (!link) return;
    var word = selectedWord();
    if (!word) {
      ev.preventDefault();
      showTip("ముందు పద్యంలో ఒక పదాన్ని ఎంచుకోండి · Select a word in the poem first");
      return;
    }
    link.href = DICT_URL + encodeURIComponent(word);   // the link then opens it in a new tab
    showTip("ఆంధ్రభారతిలో · Looking up: " + word);
  });

  // ---------- remember whether the gaṇa panel is open ----------
  var gana = document.getElementById("gana-details");
  if (gana) {
    if (store("get", "padya-gana-open") === "0") gana.open = false;
    gana.addEventListener("toggle", function () { store("set", "padya-gana-open", gana.open ? "1" : "0"); });
  }

  // ---------- the evaluation form: draft autosave and unanswered highlighting ----------
  var form = document.getElementById("eval-form");
  if (!form) return;
  var draftKey = "padya-draft:" + form.dataset.draftKey;

  function snapshot() {
    var data = {};
    Array.prototype.forEach.call(form.querySelectorAll("input[type=radio]:checked"), function (el) { data[el.name] = el.value; });
    var c = form.querySelector("textarea[name=comments]");
    if (c && c.value) data.comments = c.value;
    return data;
  }

  function restore() {
    // a saved annotation supersedes the draft; the draft is kept until then, so a failed submit loses nothing
    if (form.dataset.hasSaved === "1") { store("del", draftKey); return; }
    if (form.querySelector("input[type=radio]:checked")) return;
    var raw = store("get", draftKey);
    if (!raw) return;
    var data;
    try { data = JSON.parse(raw); } catch (e) { return; }
    var any = false;
    Object.keys(data).forEach(function (name) {
      if (name === "comments") {
        var c = form.querySelector("textarea[name=comments]");
        if (c && !c.value) { c.value = data.comments; any = true; }
        return;
      }
      var el = form.querySelector('input[type=radio][name="' + name + '"][value="' + data[name] + '"]');
      if (el) { el.checked = true; any = true; }
    });
    var note = document.getElementById("draft-note");
    if (any && note) note.hidden = false;
  }

  restore();
  form.addEventListener("change", function (ev) {
    store("set", draftKey, JSON.stringify(snapshot()));
    var fs = ev.target.closest(".q");
    if (fs) { fs.classList.remove("q-error"); fs.removeAttribute("aria-invalid"); }
  });
  form.addEventListener("input", function (ev) {
    if (ev.target.name === "comments") store("set", draftKey, JSON.stringify(snapshot()));
  });
  form.addEventListener("invalid", function (ev) {
    var fs = ev.target.closest(".q");
    if (fs) { fs.classList.add("q-error"); fs.setAttribute("aria-invalid", "true"); }
  }, true);
})();
