"""
Pre-post analysis for causal inference.

Simplest quasi-experimental method. Compares outcomes before and after
an intervention. WEAK causal evidence — assumes nothing else changed.

Mandatory caveat: "Assumes nothing else changed during this period.
Any concurrent event could explain this result."
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm


CAVEAT = (
    "CAUSAL CAVEAT: Pre-post analysis assumes nothing else changed during "
    "this period. Any concurrent event (seasonality, other product changes, "
    "external factors) could explain this result. This is the weakest form "
    "of causal evidence."
)


def pre_post_analysis(pre, post, covariates=None, alpha=0.05):
    """Pre-post comparison with optional covariate adjustment via OLS.

    Compares metric values before vs after an intervention. Optionally
    controls for covariates using regression adjustment.

    Args:
        pre: array-like of pre-period metric values (one per unit).
        post: array-like of post-period metric values (one per unit).
        covariates: optional DataFrame of covariates (aligned with pre/post).
            If provided, estimates the pre-post change controlling for these.
        alpha: significance level (default 0.05).

    Returns:
        dict with: estimate (change), ci_lower, ci_upper, p_value,
        significant, pre_mean, post_mean, method, caveat, interpretation.
    """
    pre = np.asarray(pre, dtype=float)
    post = np.asarray(post, dtype=float)

    mask = ~(np.isnan(pre) | np.isnan(post))
    pre, post = pre[mask], post[mask]

    if len(pre) < 2:
        return {
            "error": "Need at least 2 observations",
            "interpretation": "Insufficient data.",
        }

    pre_mean = float(pre.mean())
    post_mean = float(post.mean())

    if covariates is not None and len(covariates) > 0:
        # Regression-adjusted pre-post
        # Stack pre and post, add treatment indicator
        n = len(pre)
        y = np.concatenate([pre, post])
        treat = np.concatenate([np.zeros(n), np.ones(n)])

        cov_df = pd.DataFrame(covariates)
        # Stack covariates for pre and post (same units, repeated)
        cov_stacked = pd.concat([cov_df.iloc[:n].reset_index(drop=True),
                                  cov_df.iloc[:n].reset_index(drop=True)],
                                 ignore_index=True)

        X = sm.add_constant(pd.concat([
            pd.DataFrame({"post": treat}),
            cov_stacked,
        ], axis=1))

        model = sm.OLS(y, X).fit()
        estimate = float(model.params["post"])
        ci = model.conf_int(alpha=alpha).loc["post"]
        ci_lower, ci_upper = float(ci[0]), float(ci[1])
        p_value = float(model.pvalues["post"])
        method = "regression_adjusted_pre_post"
    else:
        # Simple paired pre-post (paired t-test)
        diff = post - pre
        from scipy import stats as sp_stats

        t_stat, p_value = sp_stats.ttest_rel(post, pre)
        estimate = float(diff.mean())
        se = float(diff.std(ddof=1) / np.sqrt(len(diff)))
        t_crit = sp_stats.t.ppf(1 - alpha / 2, len(diff) - 1)
        ci_lower = estimate - t_crit * se
        ci_upper = estimate + t_crit * se
        p_value = float(p_value)
        method = "paired_pre_post"

    significant = bool(p_value < alpha)
    rel_change = estimate / abs(pre_mean) * 100 if pre_mean != 0 else float("inf")

    sig_label = "significant" if significant else "not significant"
    interp = (
        f"Pre-post change: {estimate:+.4f} ({rel_change:+.1f}%), "
        f"p = {p_value:.4f} ({sig_label}). "
        f"Pre-mean = {pre_mean:.4f}, post-mean = {post_mean:.4f}. "
        f"95% CI: [{ci_lower:+.4f}, {ci_upper:+.4f}]. "
        f"Method: {method}. {CAVEAT}"
    )

    return {
        "estimate": estimate,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "p_value": p_value,
        "significant": significant,
        "pre_mean": pre_mean,
        "post_mean": post_mean,
        "relative_change_pct": float(rel_change),
        "method": method,
        "n": len(pre),
        "alpha": alpha,
        "caveat": CAVEAT,
        "confidence_level": "LOW",
        "interpretation": interp,
    }
