import numpy as np
import math

def z_score_and_pvalue(mean1, var1, n1, mean2, var2, n2):
    # pooled std denom for two-sample z (approx for large n)
    denom = math.sqrt(var1 / n1 + var2 / n2)
    if denom == 0:
        return 0.0, 1.0
    z = (mean1 - mean2) / denom
    # two-sided p-value using normal approx
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return z, p

def severity_from_p(p):
    if p < 0.01:
        return "high"
    if p < 0.05:
        return "medium"
    return "low"
