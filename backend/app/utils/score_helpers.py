from app.models.analysis import ScoreColor


def get_score_color(score: float) -> ScoreColor:
    if score >= 90:
        return ScoreColor.GREEN
    if score >= 70:
        return ScoreColor.LIGHT_GREEN
    if score >= 50:
        return ScoreColor.YELLOW
    if score >= 30:
        return ScoreColor.ORANGE
    return ScoreColor.RED


def get_score_label(score: float) -> str:
    if score >= 90:
        return "Excellent Opportunity"
    if score >= 70:
        return "Strong Opportunity"
    if score >= 50:
        return "Moderate Opportunity"
    if score >= 30:
        return "Weak Opportunity"
    return "Poor Opportunity"


def score_color_to_hex(color: ScoreColor) -> str:
    mapping = {
        ScoreColor.GREEN: "#22c55e",
        ScoreColor.LIGHT_GREEN: "#86efac",
        ScoreColor.YELLOW: "#eab308",
        ScoreColor.ORANGE: "#f97316",
        ScoreColor.RED: "#ef4444",
    }
    return mapping.get(color, "#6b7280")
