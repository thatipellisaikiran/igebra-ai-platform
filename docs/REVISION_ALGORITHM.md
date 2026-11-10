# Personalized Revision Prioritization Algorithm

## 1. Objective

Given:
- A set of syllabus topics $\mathcal{T} = \{t_1, t_2, \dots, t_N\}$.
- Student diagnostic mastery score for each topic: $M(t) \in [0.0, 1.0]$.
- Exam frequency / historical importance weight: $W_{\text{exam}}(t) \in [0.0, 1.0]$.
- Estimated base revision duration required for full mastery: $D_{\text{base}}(t)$ in hours.
- Total student revision budget: $B_{\text{hours}} = \text{Available Days} \times \text{Daily Hours}$.

The goal is to compute an ordered revision sequence $\mathcal{S}$ and allocate optimal study time $A(t)$ such that the expected exam performance gain is maximized while respecting the student's study time budget.

---

## 2. Topic Priority Score (TPS) Formulation

The urgency of revising topic $t$ is calculated via:

$$\text{TPS}(t) = \alpha \cdot \text{GapScore}(t) + \beta \cdot W_{\text{exam}}(t) + \gamma \cdot \text{Urgency}(t)$$

Where:
1. **$\text{GapScore}(t) = 1.0 - M(t)$**:
   - Represents the magnitude of the knowledge deficit.
   - If a student scored $25\%$ on photosynthesis, $\text{GapScore} = 0.75$.
2. **$W_{\text{exam}}(t)$**:
   - Normalized past paper weightage:
     $$W_{\text{exam}}(t) = \frac{\text{Past Paper Marks for } t}{\sum_{j \in \mathcal{T}} \text{Past Paper Marks for } j}$$
3. **$\text{Urgency}(t)$**:
   - Categorical multiplier based on gap severity:
     - 🔴 **Weak** ($M < 0.50$): Multiplier = $1.5$
     - 🟡 **Medium** ($0.50 \le M \le 0.75$): Multiplier = $1.0$
     - 🟢 **Strong** ($M > 0.75$): Multiplier = $0.2$
4. **Weights**: Default balanced calibration:
   - $\alpha = 0.50$ (Personal Weakness)
   - $\beta = 0.35$ (Exam Weightage)
   - $\gamma = 0.15$ (Severity Multiplier)

---

## 3. Dynamic Time Allocation Algorithm

```python
def allocate_revision_budget(topics, total_budget_hours):
    """
    Allocates study hours proportionally based on Topic Priority Score (TPS).
    Topics classified as 'Strong' receive minimal maintenance time or are deferred.
    """
    eligible_topics = [t for t in topics if t.status != "strong"]
    if not eligible_topics:
        # All topics strong: distribute evenly for refresher review
        eligible_topics = topics

    total_priority = sum(t.tps_score for t in eligible_topics)
    
    allocations = []
    for topic in eligible_topics:
        share = topic.tps_score / total_priority
        raw_hours = share * total_budget_hours
        
        # Round to convenient 0.5 hour study blocks (minimum 0.5 hr, max 4 hrs per day)
        clamped_hours = max(0.5, round(raw_hours * 2) / 2)
        allocations.append({
            "topic_id": topic.id,
            "topic_title": topic.title,
            "status": topic.status,
            "allocated_hours": clamped_hours,
            "priority_order": topic.rank
        })
        
    return allocations
```

---

## 4. Closed-Loop Adaptation (Dynamic Plan Updating)

When a student takes a follow-up quiz after reviewing a 🔴 Weak topic:
1. New accuracy $M_{\text{new}}(t)$ is registered.
2. $\text{GapScore}(t)$ decreases.
3. If $M_{\text{new}}(t) \ge 0.75$, topic transitions to 🟢 Strong.
4. The revision scheduler instantly recalculates $\text{TPS}(t)$ across remaining topics, freeing up hours originally reserved for this topic and redistributing them to remaining 🔴 Weak or 🟡 Medium topics.

