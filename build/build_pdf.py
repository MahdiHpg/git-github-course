# -*- coding: utf-8 -*-
"""Build a single RTL Persian PDF-ready HTML from the git-github course markdown files."""
import re, pathlib, markdown
from pygments.formatters import HtmlFormatter

BASE = pathlib.Path(__file__).resolve().parent.parent  # course root
BUILD = BASE / "build"

CHAPTERS = [
    ("README.md", "شروع دوره"),
    ("01-git-why.md", "فصل ۱ — گیت چیست و چرا"),
    ("02-install-config.md", "فصل ۲ — نصب، پیکربندی و SSH"),
    ("03-staging-commits.md", "فصل ۳ — سه ناحیه و کامیت بامعنا"),
    ("04-git-internals.md", "فصل ۴ — زیر پوست گیت (تور .git)"),
    ("05-git-log.md", "فصل ۵ — git log حرفه‌ای"),
    ("06-undo.md", "فصل ۶ — برگرداندن‌ها بدون ترس"),
    ("07-branches-merge.md", "فصل ۷ — شاخه‌ها، Merge و تعارض"),
    ("08-rebase.md", "فصل ۸ — Rebase و تاریخچه تمیز"),
    ("09-stash-tags-ignore.md", "فصل ۹ — Stash، Tag و gitignore"),
    ("10-github-remotes.md", "فصل ۱۰ — ریموت‌ها، push/pull، فورک"),
    ("11-pull-requests.md", "فصل ۱۱ — Pull Request، ریویو و Issue"),
    ("12-team-workflows.md", "فصل ۱۲ — گردش‌کارهای تیمی"),
    ("13-rescue-cookbook.md", "فصل ۱۳ — کتاب نجات 🚑"),
    ("14-git-hooks.md", "فصل ۱۴ — Git Hooks"),
    ("15-actions-tools.md", "فصل ۱۵ — GitHub Actions و ابزارها"),
    ("16-cheatsheet.md", "فصل ۱۶ — چیت‌شیت و مصاحبه"),
]

ANCHOR = {fn: f"ch{i:02d}" for i, (fn, _) in enumerate(CHAPTERS)}
LINK_RE = re.compile(r"\]\((\.?/?)([\w\-]+\.md)([#\w\-]*)\)")

MD_EXT = ["tables", "fenced_code", "codehilite", "md_in_html", "attr_list", "sane_lists"]
MD_CFG = {"codehilite": {"guess_lang": False}}


def preprocess(text: str) -> str:
    def repl(m):
        target, frag = m.group(2), m.group(3) or ""
        if target in ANCHOR:
            return f"](#{ANCHOR[target]}{frag})"
        return m.group(0)
    text = LINK_RE.sub(repl, text)
    text = re.sub(r"```mermaid\n(.*?)```", lambda m: f'<div class="mermaid">\n{m.group(1)}</div>', text, flags=re.S)
    text = text.replace("<details>", '<details markdown="1" open>')
    text = text.replace("<summary>", '<summary markdown="span">')
    return text


def render_chapter(fn: str, idx: int) -> str:
    raw = (BASE / fn).read_text(encoding="utf-8")
    body = markdown.markdown(preprocess(raw), extensions=MD_EXT, extension_configs=MD_CFG)
    return f'<section class="chapter" id="ch{idx:02d}">{body}</section>'


CSS = """
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Regular.ttf') format('truetype'); font-weight:400; }
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Medium.ttf') format('truetype'); font-weight:500; }
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Bold.ttf') format('truetype'); font-weight:700; }
@font-face { font-family:'JetBrains Mono'; src:url('fonts/JetBrainsMono-Regular.ttf') format('truetype'); font-weight:400; }
@font-face { font-family:'JetBrains Mono'; src:url('fonts/JetBrainsMono-Bold.ttf') format('truetype'); font-weight:700; }

@page { size: A4; margin: 16mm 13mm 18mm 13mm; }

:root {
  --ink:#1c1917; --muted:#78716c; --line:#e7e5e4;
  --primary:#c2410c; --primary-soft:#fff7ed;
  --accent:#0d9488; --accent-soft:#f0fdfa;
  --green:#16a34a; --green-soft:#f0fdf4;
  --amber:#b45309; --amber-soft:#fffbeb;
  --rose:#be123c; --rose-soft:#fff1f2;
  --code-bg:#1c1917; --code-ink:#e7e5e4;
}
* { box-sizing:border-box; }
html { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body {
  direction:rtl; text-align:right;
  font-family:'Vazirmatn', Tahoma, sans-serif;
  color:var(--ink); font-size:11.2pt; line-height:2;
  margin:0; padding:0;
}

/* cover */
.cover {
  page-break-after:always; height:250mm;
  display:flex; flex-direction:column; justify-content:center; align-items:center;
  text-align:center; color:#fff; border-radius:14px; padding:20mm;
  background:linear-gradient(135deg,#431407 0%,#c2410c 45%,#0d9488 100%);
}
.cover .badge { background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.35);
  padding:4px 18px; border-radius:999px; font-size:10pt; letter-spacing:.3px; }
.cover h1 { font-size:30pt; line-height:1.6; margin:14px 0 6px; border:none; color:#fff; background:none; }
.cover h2 { font-size:14pt; font-weight:500; color:#ffedd5; border:none; margin:0; }
.cover .stack { display:flex; gap:10px; margin-top:26px; flex-wrap:wrap; justify-content:center; }
.cover .stack span { background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.3);
  border-radius:10px; padding:6px 16px; font-size:10.5pt; }
.cover .foot { margin-top:40px; font-size:9.5pt; opacity:.85; }

/* toc */
.toc { page-break-after:always; }
.toc h1 { border:none; }
.toc ol { list-style:none; padding:0; counter-reset:toc; }
.toc li { counter-increment:toc; border-bottom:1px dashed var(--line);
  padding:9px 2px; display:flex; justify-content:space-between; align-items:baseline; }
.toc a { text-decoration:none; color:var(--ink); font-weight:500; }
.toc li::before { content:counter(toc); background:var(--primary-soft); color:var(--primary);
  font-weight:700; border-radius:8px; width:30px; height:30px; display:inline-flex;
  align-items:center; justify-content:center; margin-left:14px; flex:none; }
.toc li .desc { color:var(--muted); font-size:9.5pt; }

/* chapters / headings */
.chapter { page-break-before:always; }
h1 {
  font-size:19pt; color:#fff; background:linear-gradient(90deg,#9a3412,#ea580c);
  padding:14px 22px; border-radius:12px; line-height:1.7;
  margin:0 0 18px; page-break-after:avoid;
}
h2 {
  color:var(--primary); font-size:14.5pt; margin:26px 0 10px;
  padding-right:12px; border-right:4px solid var(--primary); line-height:1.8;
  page-break-after:avoid;
}
h3 { color:var(--accent); font-size:12.5pt; margin:20px 0 8px; page-break-after:avoid; }
p { margin:8px 0; }
strong { color:#0c0a09; }
a { color:var(--primary); text-decoration:none; }

/* lists */
ul, ol { padding-right:1.6em; padding-left:0; margin:8px 0; }
li { margin:3px 0; }
li::marker { color:var(--primary); font-weight:700; }
input[type="checkbox"] { accent-color:var(--primary); }

/* tables */
table { border-collapse:collapse; width:100%; margin:12px 0; font-size:10pt;
  border-radius:10px; overflow:hidden; page-break-inside:avoid; }
.longtable table { page-break-inside:auto; }   /* جدول‌های بلند (گلاساری): اجازه شکست بین صفحات */
.longtable tr { page-break-inside:avoid; }
th { background:linear-gradient(90deg,#9a3412,#ea580c); color:#fff; font-weight:700; }
th, td { border:1px solid #e2d6cd; padding:6px 10px; text-align:right; vertical-align:top; }
tbody tr:nth-child(even) { background:#fafaf9; }

/* code */
pre, code, kbd { font-family:'JetBrains Mono','Vazirmatn',Consolas,monospace; direction:ltr; }
code { background:#fff7ed; color:#9a3412; padding:1px 6px; border-radius:5px;
  font-size:8.8pt; unicode-bidi:embed; }
pre { background:var(--code-bg); color:var(--code-ink); direction:ltr; text-align:left;
  padding:13px 16px; border-radius:12px; overflow-x:hidden; font-size:8.6pt;
  line-height:1.65; margin:10px 0; border:1px solid #292524; page-break-inside:avoid; }
pre code { background:none; color:inherit; padding:0; font-size:inherit; }
.codehilite { background:var(--code-bg); border-radius:12px; margin:10px 0; page-break-inside:avoid; }
.codehilite pre { margin:0; border:none; }
.codehilite .k,.codehilite .kd,.codehilite .kn,.codehilite .ow { color:#fdba74; }
.codehilite .s,.codehilite .s1,.codehilite .s2,.codehilite .sd,.codehilite .sa { color:#a7f3d0; }
.codehilite .n,.codehilite .na,.codehilite .nx { color:#e7e5e4; }
.codehilite .nf { color:#fde047; }
.codehilite .mi,.codehilite .mf { color:#fca5a5; }
.codehilite .o,.codehilite .p { color:#a8a29e; }
.codehilite .nb,.codehilite .nv { color:#5eead4; }
.codehilite .err { color:#e7e5e4; background:none; border:none; }
.codehilite .c,.codehilite .c1,.codehilite .cm,.codehilite .cp { color:#93c5fd !important; font-style:italic; }
.codehilite .nt { color:#f0abfc; }
.codehilite .nd { color:#fde047; }

/* blockquotes */
blockquote {
  margin:12px 0; padding:10px 16px; border-radius:12px;
  border-right:5px solid var(--accent); background:var(--accent-soft);
  page-break-inside:avoid;
}
blockquote p { margin:4px 0; }
blockquote p:first-child { font-weight:500; }
blockquote:has(> p:first-child strong:contains("⚠")) { background:var(--amber-soft); border-right-color:var(--amber); }
blockquote:has(> p:first-child strong:contains("💡")) { background:var(--green-soft); border-right-color:var(--green); }
blockquote:has(> p:first-child strong:contains("🚨")) { background:var(--rose-soft); border-right-color:var(--rose); }
blockquote:has(> p:first-child strong:contains("🔒")) { background:var(--rose-soft); border-right-color:var(--rose); }
blockquote:has(> p:first-child strong:contains("🔑")) { background:var(--green-soft); border-right-color:var(--green); }
blockquote:has(> p:first-child strong:contains("🎯")) { background:var(--primary-soft); border-right-color:var(--primary); }
blockquote:has(> p:first-child strong:contains("🧘")) { background:var(--green-soft); border-right-color:var(--green); }
blockquote:has(> p:first-child strong:contains("🚑")) { background:var(--rose-soft); border-right-color:var(--rose); }

/* hr, details */
hr { border:none; border-top:2px dashed var(--line); margin:22px 0; }
details { background:#fafaf9; border:1px solid var(--line); border-radius:10px;
  padding:8px 14px; margin:10px 0; page-break-inside:avoid; }
summary { cursor:pointer; font-weight:700; color:var(--green); }

/* mermaid */
.mermaid {
  background:#fff; border:1px solid var(--line); border-radius:12px;
  padding:10px; margin:12px 0; text-align:center; page-break-inside:avoid;
  display:flex; justify-content:center;
}
.mermaid svg { max-width:100%; height:auto; }

del { color:var(--muted); }
em { color:#292524; }
"""

PYGMENTS_CSS = HtmlFormatter(style="default").get_style_defs(".codehilite")

COVER = """
<section class="cover">
  <div class="badge">آموزش صفر تا صد — نسخه ۲۰۲۶</div>
  <h1>Git و GitHub<br/>برای دولوپرهای آماده‌ی تیم</h1>
  <h2>از «کامیت و پوش بلدم» تا حرفه‌ایِ شاخه، PR و کار در شرکت</h2>
  <div class="stack">
    <span>Git 2.5x</span><span>GitHub Flow</span><span>Pull Request</span>
    <span>Rebase &amp; Conflict</span><span>Git Hooks</span><span>GitHub Actions</span>
  </div>
  <div class="foot">۱۶ فصل · تمرین با جواب · ۱۵ سناریوی نجات · ۲۴ سوال مصاحبه · چیت‌شیت و گلاساری</div>
</section>
"""

DESCS = {
    "README.md": "نقشه دوره و روش مطالعه",
    "01-git-why.md": "snapshot، سه ناحیه، HEAD، SHA",
    "02-install-config.md": "نصب ویندوز، Git Bash، config، کلید SSH، clone",
    "03-staging-commits.md": "staging، add -p، git mv، Conventional Commits",
    "04-git-internals.md": "تور .git، آبجکت‌ها، dedup، index، git gc",
    "05-git-log.md": "فیلترها، pickaxe، pretty format، blame",
    "06-undo.md": "restore، reset، revert، reflog",
    "07-branches-merge.md": "switch، merge، حل تعارض قدم‌به‌قدم",
    "08-rebase.md": "rebase -i، squash، قانون طلایی",
    "09-stash-tags-ignore.md": "stash، tag و semver، .gitignore، bisect",
    "10-github-remotes.md": "fetch/pull، push -u، fork و upstream",
    "11-pull-requests.md": "قالب PR، ریویو، squash merge، Rulesets، Issue",
    "12-team-workflows.md": "GitHub Flow، Git Flow، trunk-based",
    "13-rescue-cookbook.md": "۱۵ سناریوی «چه کار کنم اگر...»",
    "14-git-hooks.md": "pre-commit، commit-msg، Husky و lint-staged",
    "15-actions-tools.md": "workflow یامل، Checks، Dependabot، امضا",
    "16-cheatsheet.md": "مرور سریع + واژه‌نامه + ۲۴ سوال مصاحبه",
}


def build_toc() -> str:
    items = []
    for i, (fn, title) in enumerate(CHAPTERS):
        items.append(f'<li><a href="#ch{i:02d}">{title}</a><span class="desc">{DESCS.get(fn, "")}</span></li>')
    return f'<section class="toc"><h1>فهرست مطالب</h1><ol>{"".join(items)}</ol></section>'


def main():
    parts = [COVER, build_toc()]
    for i, (fn, _) in enumerate(CHAPTERS):
        parts.append(render_chapter(fn, i))
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"/>
<title>دوره Git و GitHub</title>
<style>{CSS}
{PYGMENTS_CSS}
</style></head>
<body>{''.join(parts)}
<script src="mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad:true, theme:'base',
  themeVariables: {{ fontFamily:'Vazirmatn, Tahoma', fontSize:'13px',
    primaryColor:'#fff7ed', primaryBorderColor:'#c2410c', primaryTextColor:'#1c1917',
    lineColor:'#78716c', secondaryColor:'#f0fdfa', tertiaryColor:'#fafaf9',
    gitBranchLabel: 'main' }},
  flowchart: {{ htmlLabels:true, curve:'basis' }}, gitGraph: {{ showBranches:true }} }});</script>
</body></html>"""
    out = BUILD / "course.html"
    out.write_text(html, encoding="utf-8")
    print(f"OK -> {out}  ({len(html)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
