# Best Employee Rules

> Six iron rules for AI coding assistants — keep it sharp, honest, and user-first.

A Reasonix / Kun / Codex skill that enforces disciplined AI behavior: no over-engineering, no sugar-coating, no guessing, no blind edits, no fluff, and no overriding the user. Each rule includes an automated self-check the AI runs before every response.

---

## The Six Iron Rules

| # | Rule | Meaning |
|---|------|---------|
| 1 | **No Over-Engineering** | Don't add things nobody asked for. Three repeated lines beat one premature abstraction. |
| 2 | **Report Honestly** | If something went wrong, say so with specifics. No sugar-coating, no disclaimers. |
| 3 | **No Guessing** | If you don't know, say you don't know. Never fabricate. |
| 4 | **Read Before Edit** | Never edit a file you haven't read. Confirm understanding first. |
| 5 | **No Fluff** | No emoji. No filler. Conclusion first, reasoning second. |
| 6 | **User Is Final** | Flag ambiguity instead of assuming. Never override the user's intent. |

---

## File Structure

```
best-employee-rules/
├── best-employee-rules.md       # Bilingual skill (ZH + EN)
├── best-employee-rules-en.md    # Pure English variant
├── scripts/
│   ├── validate.py              # Validate skill format & completeness
│   ├── install.py               # One-click install to skills directory
│   └── generate.py              # Generate ZH / EN / bilingual variants
├── README.md
└── LICENSE
```

---

## Scripts

### `validate.py` — Format & completeness check

```bash
python scripts/validate.py best-employee-rules.md
python scripts/validate.py --quiet best-employee-rules-en.md
```

Checks: YAML frontmatter fields, exactly 6 numbered rules, self-check checklist table, non-empty body. Exit code 0 on pass.

### `install.py` — One-click install

```bash
python scripts/install.py                        # auto-detect target directory
python scripts/install.py --variant en           # install English version
python scripts/install.py -t ~/.reasonix/skills/ # explicit target
python scripts/install.py --dry-run              # preview only
```

Auto-detects `.reasonix/skills/`, `.codex/skills/`, or `.kun/skills/`.

### `generate.py` — Multi-language generation

```bash
python scripts/generate.py --lang zh            # Chinese only
python scripts/generate.py --lang en            # English only
python scripts/generate.py --lang both          # bilingual (default)
python scripts/generate.py --lang en -o out.md  # custom output path
```

All generated files pass `validate.py`.

---

## Installation

**Auto:** Run the install script:
```bash
python scripts/install.py
```

**Manual:** Copy `best-employee-rules.md` (or `best-employee-rules-en.md`) into your Reasonix skills directory:
```
~/.reasonix/skills/best-employee-rules.md
```

---

## 中文简介

**最佳员工准则** — 六条 AI 行为铁律：

1. **不画蛇添足** — 不加没要求的东西，避免过度设计
2. **如实汇报** — 不润色、不过度谦虚、不加免责声明
3. **不知说不知** — 不知道就说不知道，不编造答案
4. **先看再改** — 必须先读文件再编辑
5. **沟通规范** — 不用 emoji、不说废话、结论在前
6. **不忤逆用户** — 不擅自替用户做决定

每条规则附带自动化自查项。推荐使用 `scripts/install.py` 一键安装。

---

## License

MIT
