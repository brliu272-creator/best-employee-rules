#!/usr/bin/env python3
"""Generate language variants of best-employee-rules skill.

Produces pure Chinese, pure English, or a merged bilingual version
from the canonical bilingual source file.

Usage:
  python scripts/generate.py --lang zh    # Chinese only
  python scripts/generate.py --lang en    # English only
  python scripts/generate.py --lang both  # bilingual (default)
  python scripts/generate.py --lang zh --out ./my-skill.md
"""

import argparse
import re
import sys
from pathlib import Path


# Canonical rule definitions: (english_title, chinese_title, en_body, zh_body)
RULES = [
    (
        "No Over-Engineering",
        "不画蛇添足",
        [
            "- Don't add things nobody asked for.",
            "- Don't guard against impossible scenarios.",
            "- Three repeated lines beat one premature abstraction.",
        ],
        [
            "- 不加未被要求的东西。",
            "- 不为不可能的情况做预防。",
            "- 三行重复好于一个过早抽象。",
        ],
    ),
    (
        "Report Honestly",
        "如实汇报",
        [
            "- If something went wrong, say so with specifics.",
            "- If you didn't do a step, don't imply you did.",
            "- If you did well, skip the disclaimers.",
        ],
        [
            "- 做错了就说做错了，附具体情况。",
            "- 没做的步骤不说做了。",
            "- 做好了不加免责声明。",
        ],
    ),
    (
        "No Guessing",
        "不知说不知",
        [
            "- If you don't know, say you don't know. Never fabricate.",
        ],
        [
            "- 不知道就说不知道，禁止编造。",
        ],
    ),
    (
        "Read Before Edit",
        "先看再改",
        [
            "- Never edit a file you haven't read.",
            "- Confirm your understanding of the content before changing it.",
        ],
        [
            "- 读文件后才能编辑它。",
            "- 改前先复述关键内容确认理解。",
        ],
    ),
    (
        "No Fluff",
        "沟通规范",
        [
            "- No emoji. No filler words.",
            "- Conclusion first, reasoning second.",
        ],
        [
            "- 禁用 emoji。",
            "- 不说废话，结论在前。",
        ],
    ),
    (
        "User Is Final",
        "不忤逆用户",
        [
            "- Flag ambiguity instead of assuming.",
            "- Never go against the user's explicit intent.",
        ],
        [
            "- 不明确就提问，不擅自决定。",
            "- 不允许违背用户明确意图。",
        ],
    ),
]

CHECKLIST_EN = [
    "Am I adding anything the user didn't ask for?",
    "Am I sugar-coating, deflecting, or adding disclaimers?",
    "Am I fabricating an answer from nothing?",
    "Did I read the file before editing?",
    "Is there any fluff or emoji? Conclusion first?",
    "Did I make a decision the user should have made?",
]

CHECKLIST_ZH = [
    "加了用户没要求的东西吗？",
    "在润色/推诿/加免责吗？",
    "在不知道的情况下编造了吗？",
    "改文件前读过了吗？",
    "有废话/emoji吗？结论在前吗？",
    "擅自替用户做了决定吗？",
]


def make_frontmatter(lang: str) -> str:
    if lang == "zh":
        desc = (
            "最佳员工准则 — AI 行为六铁律：不画蛇添足、如实汇报、不知说不知、"
            "先看再改、沟通规范、不忤逆用户。用户提及员工准则/行为规范时主动询问。"
        )
    elif lang == "en":
        desc = (
            "Best Employee Rules — six iron rules for AI coding assistants: "
            "no over-engineering, report honestly, no guessing, read before edit, "
            "no fluff, user is final. Trigger: rules, code of conduct, AI guidelines."
        )
    else:
        desc = (
            "最佳员工准则 Best Employee Rules — AI 行为六铁律：不画蛇添足(no over-engineering)、"
            "如实汇报(no sugar-coating)、不知说不知(no guessing)、先看再改(read before edit)、"
            "沟通规范(no fluff)、不忤逆用户(user is final)。用户提及员工准则/行为规范/rules时主动询问。"
        )

    return f"""---
name: best-employee-rules
description: |
  {desc}
---"""


def make_body(lang: str) -> str:
    if lang == "zh":
        title = "# 最佳员工准则"
        intro = "以下六条铁律在加载后持续生效，每条回复前自检。"
    elif lang == "en":
        title = "# Best Employee Rules"
        intro = "Six iron rules. Once loaded, they apply to every response for the rest of the session."
    else:
        title = "# 最佳员工准则 · Best Employee Rules"
        intro = "以下六条铁律在加载后持续生效，每条回复前自检。\nSix iron rules. Once loaded, self-check before every response."

    lines = [title, "", intro, "", "---", ""]

    for i, (en_title, zh_title, en_body, zh_body) in enumerate(RULES, 1):
        if lang == "zh":
            lines.append(f"## {i}. {zh_title}")
            lines.extend(zh_body)
        elif lang == "en":
            lines.append(f"## {i}. {en_title}")
            lines.extend(en_body)
        else:
            lines.append(f"## {i}. {zh_title} · {en_title}")
            lines.extend(zh_body)
        lines.append("")

    lines.append("---")
    lines.append("")

    if lang == "zh":
        lines.append("## Self-Check 自查清单")
        lines.append("")
        lines.append("每条指令后逐条过检：")
        lines.append("")
        lines.append("| # | Check |")
        lines.append("|---|-------|")
        for i, check in enumerate(CHECKLIST_ZH, 1):
            lines.append(f"| {i} | {check} |")
    elif lang == "en":
        lines.append("## Self-Check")
        lines.append("")
        lines.append("Before every response, verify:")
        lines.append("")
        lines.append("| # | Check |")
        lines.append("|---|-------|")
        for i, check in enumerate(CHECKLIST_EN, 1):
            lines.append(f"| {i} | {check} |")
    else:
        lines.append("## Self-Check 自查清单")
        lines.append("")
        lines.append("每条指令后逐条过检：")
        lines.append("")
        lines.append("| # | Check |")
        lines.append("|---|-------|")
        for i, (zh, en) in enumerate(zip(CHECKLIST_ZH, CHECKLIST_EN), 1):
            lines.append(f"| {i} | {zh} / {en} |")

    return "\n".join(lines) + "\n"


def generate(lang: str, out: Path | None = None) -> str:
    """Generate skill text for the given language. Returns the text."""
    fm = make_frontmatter(lang)
    body = make_body(lang)
    text = fm + "\n" + body

    if out:
        out.write_text(text, encoding="utf-8")
        print(f"Generated: {out} (lang={lang})")

    return text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate language variants of best-employee-rules"
    )
    parser.add_argument(
        "--lang",
        choices=["zh", "en", "both"],
        default="both",
        help="language variant: zh (Chinese), en (English), both (bilingual, default)",
    )
    parser.add_argument(
        "-o", "--out", type=Path, default=None, help="output file path"
    )
    args = parser.parse_args()

    # Determine output path
    if args.out:
        out = args.out
    else:
        script_dir = Path(__file__).resolve().parent
        root = script_dir.parent
        lang_map = {"zh": "best-employee-rules-zh.md", "en": "best-employee-rules-en.md", "both": "best-employee-rules.md"}
        out = root / lang_map[args.lang]

    text = generate(args.lang, out)
    if not args.out:
        print(text)


if __name__ == "__main__":
    main()
