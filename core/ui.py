import streamlit.components.v1 as components
import html
import uuid

def copy_button(text: str, label: str = "Копіювати"):
    safe = html.escape(text)
    bid = f"copy_{uuid.uuid4().hex}"
    components.html(
        f"""
        <div style="display:flex; gap:10px; align-items:center;">
          <div style="
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
            padding:8px 10px;
            border-radius:10px;
            background:#f2f4f7;
            color:#111827;
            border:1px solid #e5e7eb;
            flex:1;
            overflow:auto;
            white-space:nowrap;
          ">{safe}</div>

          <button id="{bid}" style="
            padding:8px 12px;
            border-radius:10px;
            border:1px solid #d1d5db;
            background:#ffffff;
            color:#111827;
            cursor:pointer;
            font-weight:600;
          ">
            {label}
          </button>
        </div>

        <script>
          const btn = document.getElementById("{bid}");
          btn.addEventListener("click", async () => {{
            try {{
              await navigator.clipboard.writeText("{safe}");
              const old = btn.textContent;
              btn.textContent = "Скопійовано ✅";
              btn.style.background = "#ecfdf5";
              btn.style.borderColor = "#10b981";
              setTimeout(() => {{
                btn.textContent = old;
                btn.style.background = "#ffffff";
                btn.style.borderColor = "#d1d5db";
              }}, 1200);
            }} catch (e) {{
              const old = btn.textContent;
              btn.textContent = "Не вдалось ⚠️";
              btn.style.background = "#fff7ed";
              btn.style.borderColor = "#fb923c";
              setTimeout(() => {{
                btn.textContent = old;
                btn.style.background = "#ffffff";
                btn.style.borderColor = "#d1d5db";
              }}, 1200);
            }}
          }});
        </script>
        """,
        height=62,
    )
