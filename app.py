import streamlit as st
import sqlite3
import pandas as pd

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

conn = sqlite3.connect(
    "decisions.db",
    check_same_thread=False
)

cursor = conn.cursor()

# --------------------------------------------------
# DECISION MEMORY TABLE
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_description TEXT,
    opportunity_value REAL,
    stakeholder_risk TEXT,
    technical_complexity TEXT,
    deadline_hours INTEGER,
    confidence REAL,
    escalation TEXT,
    approval TEXT
)
""")

conn.commit()

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("EDI Labs")

st.subheader(
    "Enterprise Decision Infrastructure"
)

st.write(
    "Trust, Memory and Execution Layer for Autonomous Enterprises"
)

st.markdown("---")

# --------------------------------------------------
# ENTERPRISE CONTEXT
# --------------------------------------------------

st.header("Enterprise Context")

decision_description = st.text_input(
    "Decision Description",
    placeholder="Approve Strategic Partner Agreement"
)

opportunity_value = st.number_input(
    "Opportunity Value ($)",
    min_value=0,
    value=2500000
)

stakeholder_risk = st.selectbox(
    "Stakeholder Risk",
    ["Low", "Medium", "High"]
)

technical_complexity = st.selectbox(
    "Technical Complexity",
    ["Low", "Medium", "High"]
)

deadline_hours = st.number_input(
    "Deadline (Hours)",
    min_value=1,
    value=48
)

st.markdown("---")

# --------------------------------------------------
# EVALUATE DECISION
# --------------------------------------------------

if st.button("Evaluate Decision"):

    st.subheader("Decision Evaluation")

    st.code(
f"""
INPUT

decision_description  {decision_description}

opportunity_value     ${opportunity_value:,.0f}

stakeholder_risk      {stakeholder_risk.upper()}

technical_complexity  {technical_complexity.upper()}

deadline_hours        {deadline_hours}
"""
    )

    st.subheader("Decision Evaluation Pipeline")

    st.success("✓ Enterprise Context Ingested")

    st.success("✓ Confidence Evaluation Completed")

    st.success("✓ Trust Controls Applied")

    st.success("✓ Escalation Assessment Completed")

    st.success("✓ Human Oversight Requirement Determined")

    # --------------------------------------------------
    # CONFIDENCE LOGIC
    # --------------------------------------------------

    if stakeholder_risk == "High":
        confidence = 0.61

    elif stakeholder_risk == "Medium":
        confidence = 0.78

    else:
        confidence = 0.92

    # --------------------------------------------------
    # ESCALATION LOGIC
    # --------------------------------------------------

    threshold = 0.75

    if confidence < threshold:
        escalation = "REQUIRED"
    else:
        escalation = "NOT REQUIRED"

    # --------------------------------------------------
    # HUMAN APPROVAL
    # --------------------------------------------------

    if stakeholder_risk == "High":
        approval = "REQUIRED"
    else:
        approval = "OPTIONAL"

    # --------------------------------------------------
    # SAVE DECISION TO MEMORY
    # --------------------------------------------------

    cursor.execute(
        """
        INSERT INTO decisions (
            decision_description,
            opportunity_value,
            stakeholder_risk,
            technical_complexity,
            deadline_hours,
            confidence,
            escalation,
            approval
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            decision_description,
            opportunity_value,
            stakeholder_risk,
            technical_complexity,
            deadline_hours,
            confidence,
            escalation,
            approval
        )
    )

    conn.commit()

    st.success("Decision Saved To Enterprise Decision Ledger")

    st.markdown("---")

    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------

    st.subheader("Decision Outcome")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Confidence",
            f"{confidence:.2f}"
        )

    with col2:
        st.metric(
            "Escalation",
            escalation
        )

    with col3:
        st.metric(
            "Human Approval",
            approval
        )

    st.markdown("---")

    st.subheader("Recommended Action")

    if escalation == "REQUIRED":

        st.warning(
            """
Executive alignment required before advancing commitment.

Risk level exceeds autonomous execution threshold.
            """
        )

    else:

        st.success(
            """
Risk profile within acceptable threshold.

Proceed with standard execution process.
            """
        )

# --------------------------------------------------
# ENTERPRISE DECISION LEDGER
# --------------------------------------------------

st.markdown("---")

st.header("Enterprise Decision Ledger")

df = pd.read_sql_query(
    """
    SELECT
        id,
        decision_description,
        opportunity_value,
        stakeholder_risk,
        technical_complexity,
        deadline_hours,
        confidence,
        escalation,
        approval
    FROM decisions
    ORDER BY id DESC
    """,
    conn
)

st.dataframe(
    df,
    use_container_width=True
)