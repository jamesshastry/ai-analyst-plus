"""Parse pipeline artifacts into structured data for gdoc_builder.build_readout().

Reads:
  - outputs/narrative_*.md         → title, context, findings, recommendations
  - working/pipeline_summary.md    → dataset name, date, metadata
  - outputs/validation_*.md        → confidence grade/score
  - outputs/close_the_loop_*.md    → success tracking, action items

All files are optional. Missing files produce None values, not errors.
"""

from __future__ import annotations

import glob
import os
import re
from pathlib import Path
from typing import Optional

from helpers.gdoc_builder import (
    AnalysisData, Finding, SubFinding, Recommendation, SqlQuery,
    SuccessTracking,
)


def _find_latest(pattern: str, base_dir: str) -> Optional[str]:
    """Find the most recently modified file matching a glob pattern."""
    matches = glob.glob(os.path.join(base_dir, pattern))
    if not matches:
        return None
    return max(matches, key=os.path.getmtime)


def _read_file(path: Optional[str]) -> Optional[str]:
    """Read file contents, return None if path is None or file missing."""
    if not path or not os.path.isfile(path):
        return None
    with open(path, "r") as f:
        return f.read()


def _extract_between(text: str, start_heading: str,
                     end_headings: list[str],
                     heading_level: int = 2) -> Optional[str]:
    """Extract text between two headings of the same level.

    Args:
        text: Full markdown text.
        start_heading: The heading text to start from (without ## prefix).
        end_headings: List of heading texts that mark the end.
        heading_level: Number of # characters (2 for ##, 3 for ###).

    Returns:
        Text between the headings, or None if start not found.
    """
    prefix = "#" * heading_level
    # Match the start heading (case-insensitive, allow leading/trailing space)
    pattern = rf"^{prefix}\s+{re.escape(start_heading)}\s*$"
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return None

    start_pos = match.end()

    # Find the next heading at the same or higher level
    next_heading_pattern = rf"^#{{{1},{heading_level}}}\s+"
    remaining = text[start_pos:]
    next_match = re.search(next_heading_pattern, remaining, re.MULTILINE)

    if next_match:
        return remaining[:next_match.start()].strip()
    return remaining.strip()


# ---------------------------------------------------------------------------
# Narrative parsing
# ---------------------------------------------------------------------------

def _parse_narrative_title(text: str) -> str:
    """Extract the H1 title from narrative markdown."""
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled Analysis"


def _parse_context(text: str) -> Optional[str]:
    """Extract the Context section."""
    return _extract_between(text, "Context", [
        "Key Findings", "Findings", "Executive Summary",
    ])


def _parse_executive_summary(text: str) -> Optional[str]:
    """Extract the Executive Summary section."""
    return _extract_between(text, "Executive Summary", [
        "Context", "Key Findings", "Findings",
    ])


def _parse_findings(text: str, charts_dir: str) -> list[Finding]:
    """Parse ## Key Findings → ### Finding N sections."""
    findings_text = _extract_between(text, "Key Findings", [
        "Insight", "Implication", "Recommendations", "Supporting Data",
    ])
    if not findings_text:
        return []

    findings = []
    # Split on ### Finding N: headings
    parts = re.split(r"^###\s+(?:Finding\s+\d+:\s*)?(.+)$",
                     findings_text, flags=re.MULTILINE)

    # parts[0] is text before first finding (usually empty)
    # parts[1] is first heading text, parts[2] is first body, etc.
    for i in range(1, len(parts), 2):
        headline = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""

        # Look for chart references in the body
        chart_path = _find_chart_for_finding(body, charts_dir)

        # For now, each finding is a single unit (no sub-findings from narrative)
        # The builder will render it as H3 with body text
        sub = SubFinding(
            title=headline,
            body=body,
            chart_path=chart_path,
            chart_caption=headline,
        )
        findings.append(Finding(
            headline=headline,
            summary=_first_sentence(body),
            sub_findings=[sub],
        ))

    return findings


def _find_chart_for_finding(body: str, charts_dir: str) -> Optional[str]:
    """Look for chart file references in finding body text."""
    # Match patterns like: ![...](outputs/charts/filename.png)
    # or: `outputs/charts/filename.png`
    # or: charts/filename.png
    patterns = [
        r"!\[.*?\]\(([^)]*\.png)\)",
        r"`((?:outputs/)?charts/[^`]+\.png)`",
        r"((?:outputs/)?charts/\S+\.png)",
    ]
    for pat in patterns:
        match = re.search(pat, body)
        if match:
            ref = match.group(1)
            # Try as absolute, relative to charts_dir, or relative to cwd
            for candidate in [ref, os.path.join(charts_dir, os.path.basename(ref))]:
                if os.path.isfile(candidate):
                    return os.path.abspath(candidate)
    return None


def _first_sentence(text: str) -> str:
    """Extract the first sentence from a paragraph."""
    text = text.strip()
    # Remove markdown image references
    text = re.sub(r"!\[.*?\]\([^)]*\)", "", text).strip()
    match = re.match(r"(.+?\.)\s", text)
    return match.group(1) if match else text[:200]


def _parse_recommendations(text: str) -> list[Recommendation]:
    """Parse the ## Recommendations section."""
    rec_text = _extract_between(text, "Recommendations", [
        "Supporting Data", "Skills Used", "Validation",
    ])
    if not rec_text:
        return []

    recs = []
    # Match numbered items: 1. **Action**: Description. Confidence level.
    items = re.findall(
        r"\d+\.\s+\*\*(.+?)\*\*:?\s*(.+?)(?=\n\d+\.|\Z)",
        rec_text, re.DOTALL,
    )
    for action, detail in items:
        detail = detail.strip()
        # Extract confidence if mentioned
        conf_match = re.search(
            r"[Cc]onfidence(?:\s+level)?:?\s*(High|Medium|Low)",
            detail, re.IGNORECASE,
        )
        confidence = conf_match.group(1).capitalize() if conf_match else "Medium"
        # Clean confidence mention from rationale
        rationale = re.sub(r"\s*[Cc]onfidence(?:\s+level)?:?\s*(High|Medium|Low)\.?",
                           "", detail).strip()
        recs.append(Recommendation(
            action=action.strip(),
            rationale=rationale,
            confidence=confidence,
        ))

    return recs


def _parse_insight(text: str) -> Optional[str]:
    """Parse the ## Insight section (maps to Synthesis)."""
    return _extract_between(text, "Insight", [
        "Implication", "Recommendations",
    ])


def _parse_implication(text: str) -> Optional[str]:
    """Parse the ## Implication section."""
    return _extract_between(text, "Implication", [
        "Recommendations", "Supporting Data",
    ])


# ---------------------------------------------------------------------------
# Pipeline summary parsing
# ---------------------------------------------------------------------------

def _parse_pipeline_summary(text: str) -> dict:
    """Extract metadata from pipeline_summary.md."""
    meta = {}

    # Title
    match = re.search(r"^#\s+Pipeline Summary:\s*(.+)$", text, re.MULTILINE)
    if match:
        meta["business_context"] = match.group(1).strip()

    # Dataset
    match = re.search(r"\*\*Dataset:\*\*\s*(.+)$", text, re.MULTILINE)
    if match:
        meta["dataset"] = match.group(1).strip()

    # Date
    match = re.search(r"\*\*Date:\*\*\s*(.+)$", text, re.MULTILINE)
    if match:
        meta["date"] = match.group(1).strip()

    return meta


# ---------------------------------------------------------------------------
# Validation parsing
# ---------------------------------------------------------------------------

def _parse_validation(text: str) -> dict:
    """Extract confidence grade and score from validation report."""
    result = {}

    # Overall Confidence: HIGH | MEDIUM | LOW
    match = re.search(r"Overall Confidence:\s*(HIGH|MEDIUM|LOW)",
                      text, re.IGNORECASE)
    if match:
        level = match.group(1).upper()
        grade_map = {"HIGH": "A", "MEDIUM": "B", "LOW": "C"}
        result["grade"] = grade_map.get(level, "B")

    # Confidence Score: A (92/100) or similar
    match = re.search(r"Confidence Score:.*?([A-F][+-]?)\s*\((\d+)/100\)", text)
    if match:
        result["grade"] = match.group(1)
        result["score"] = int(match.group(2))

    # Look for caveats in Data Quality Notes or warnings
    match = re.search(r"Data Quality Notes\s*\n(.+?)(?=\n##|\Z)",
                      text, re.DOTALL)
    if match:
        caveat = match.group(1).strip()
        if caveat and caveat.lower() != "none":
            result["caveat"] = caveat[:200]  # truncate long caveats

    return result


# ---------------------------------------------------------------------------
# SQL collection
# ---------------------------------------------------------------------------

def _collect_sql(base_dir: str) -> list[SqlQuery]:
    """Collect SQL files from working/sql_queries/."""
    sql_dir = os.path.join(base_dir, "working", "sql_queries")
    if not os.path.isdir(sql_dir):
        return []

    queries = []
    for path in sorted(glob.glob(os.path.join(sql_dir, "*.sql"))):
        name = Path(path).stem
        # Convert filename to title: "01_revenue_by_segment" → "Revenue By Segment"
        title = re.sub(r"^\d+_", "", name).replace("_", " ").title()
        sql = _read_file(path) or ""
        queries.append(SqlQuery(title=title, sql=sql))

    return queries


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_pipeline_outputs(base_dir: str = ".") -> AnalysisData:
    """Parse all pipeline artifacts and return structured AnalysisData.

    Args:
        base_dir: Root directory of the ai-analyst-plus project.

    Returns:
        AnalysisData ready for gdoc_builder.build_readout().
    """
    outputs_dir = os.path.join(base_dir, "outputs")
    working_dir = os.path.join(base_dir, "working")
    charts_dir = os.path.join(outputs_dir, "charts")

    # Find source files
    narrative_path = _find_latest("narrative_*.md", outputs_dir)
    summary_path = os.path.join(working_dir, "pipeline_summary.md")
    validation_path = _find_latest("validation_*.md", outputs_dir)
    close_loop_path = _find_latest("close_the_loop_*.md", outputs_dir)

    # Read files
    narrative_text = _read_file(narrative_path)
    summary_text = _read_file(summary_path)
    validation_text = _read_file(validation_path)
    close_loop_text = _read_file(close_loop_path)

    # Parse narrative (primary source)
    title = "Untitled Analysis"
    context = None
    findings = []
    recommendations = []
    synthesis = None
    implications = None

    if narrative_text:
        title = _parse_narrative_title(narrative_text)
        context = _parse_context(narrative_text)
        findings = _parse_findings(narrative_text, charts_dir)
        recommendations = _parse_recommendations(narrative_text)
        synthesis = _parse_insight(narrative_text)
        implications = _parse_implication(narrative_text)

        # If no context from narrative, try executive summary
        if not context:
            context = _parse_executive_summary(narrative_text)

    # Parse pipeline summary (metadata)
    meta = _parse_pipeline_summary(summary_text) if summary_text else {}
    dataset = meta.get("dataset", "")
    date = meta.get("date", "")
    subtitle = f"{dataset} | {date}" if dataset else None

    # Parse validation (confidence)
    validation = _parse_validation(validation_text) if validation_text else {}
    confidence_grade = validation.get("grade")
    confidence_score = validation.get("score")
    confidence_caveat = validation.get("caveat")

    # Collect SQL queries
    sql_queries = _collect_sql(base_dir)

    # Parse close-the-loop (success tracking)
    success_tracking = None
    open_questions = None
    next_steps_actions = None

    if close_loop_text:
        # Try to extract action items
        actions_section = _extract_between(close_loop_text, "Action Items", [
            "Success", "Open Questions", "Follow-up",
        ])
        if actions_section:
            next_steps_actions = actions_section

        # Try to extract success metric
        success_section = _extract_between(close_loop_text, "Success Metric", [
            "Open Questions", "Action Items", "Follow-up",
        ])
        if success_section:
            metric_match = re.search(r"Metric:\s*(.+)", success_section)
            baseline_match = re.search(r"Baseline:\s*(.+)", success_section)
            target_match = re.search(r"Target:\s*(.+)", success_section)
            checkin_match = re.search(r"Check.in:\s*(.+)", success_section)
            if metric_match:
                success_tracking = SuccessTracking(
                    metric=metric_match.group(1).strip(),
                    baseline=baseline_match.group(1).strip() if baseline_match else "TBD",
                    target=target_match.group(1).strip() if target_match else "TBD",
                    check_in_date=checkin_match.group(1).strip() if checkin_match else None,
                )

        # Open questions
        oq_section = _extract_between(close_loop_text, "Open Questions", [
            "Action Items", "Success", "Follow-up",
        ])
        if oq_section:
            open_questions = oq_section

    return AnalysisData(
        title=title,
        subtitle=subtitle,
        author="AI Analyst",
        date=date,
        confidence_grade=confidence_grade,
        confidence_score=confidence_score,
        confidence_caveat=confidence_caveat,
        context=context,
        findings=findings,
        synthesis=synthesis,
        implications=implications,
        recommendations=recommendations,
        next_steps_actions=next_steps_actions,
        success_tracking=success_tracking,
        open_questions=open_questions,
        sql_queries=sql_queries,
        data_sources=f"Dataset: {dataset}" if dataset else None,
    )
