<<<<<<< HEAD
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="EDI Labs",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

conn = sqlite3.connect(
    "edis.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS learning_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    situation TEXT,
    decision TEXT,
    assumptions TEXT,
    expected_outcome TEXT,
    actual_outcome TEXT,
    learning TEXT,
    evidence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def load_records():

    return pd.read_sql_query(
        """
        SELECT
            id,
            title,
            situation,
            decision,
            assumptions,
            expected_outcome,
            actual_outcome,
            learning,
            evidence,
            created_at
        FROM learning_records
        ORDER BY id DESC
        """,
        conn
    )


def save_learning_record(
    title,
    situation,
    decision,
    assumptions,
    expected_outcome,
    evidence
):

    cursor.execute(
        """
        INSERT INTO learning_records (
            title,
            situation,
            decision,
            assumptions,
            expected_outcome,
            evidence
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            situation,
            decision,
            assumptions,
            expected_outcome,
            evidence
        )
    )

    conn.commit()


def update_outcome(
    record_id,
    actual_outcome,
    learning
):

    cursor.execute(
        """
        UPDATE learning_records
        SET
            actual_outcome = ?,
            learning = ?
        WHERE id = ?
        """,
        (
            actual_outcome,
            learning,
            record_id
        )
    )

    conn.commit()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("EDI Labs")

st.subheader(
    "Organizational Learning Infrastructure"
)

st.write(
    """
Capture decisions.
Track assumptions.
Measure outcomes.
Compound intelligence.
"""
)

st.markdown("---")

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Create Learning Record",
        "Learning Repository",
        "Outcome Review",
        "Ask EDI"
    ]
)

# ==================================================
# TAB 1
# ==================================================

with tab1:

    st.header("Create Learning Record")

    title = st.text_input(
        "Title",
        placeholder="Anthropic + AWS Accelerator Application"
    )

    situation = st.text_area(
        "Situation",
        placeholder="""
Describe the situation that led to this decision.
"""
    )

    decision = st.text_area(
        "Decision",
        placeholder="""
What decision was made?
"""
    )

    assumptions = st.text_area(
        "Assumptions",
        placeholder="""
What must be true for this decision to succeed?

Example:
- Enterprise demand exists
- Claude improves decision quality
- Buyers value organizational learning
"""
    )

    expected_outcome = st.text_area(
        "Expected Outcome",
        placeholder="""
What do we expect to happen?
"""
    )

    evidence = st.text_area(
        "Evidence",
        placeholder="""
Links, decks, documents, research, notes.
"""
    )

    if st.button(
        "Create Learning Record",
        use_container_width=True
    ):

        if (
            title.strip() == ""
            or situation.strip() == ""
            or decision.strip() == ""
        ):

            st.error(
                "Title, Situation and Decision are required."
            )

        else:

            save_learning_record(
                title,
                situation,
                decision,
                assumptions,
                expected_outcome,
                evidence
            )

            st.success(
                "Learning Record Created Successfully"
            )

            st.subheader("Record Summary")

            st.code(
f"""
TITLE

{title}

SITUATION

{situation}

DECISION

{decision}

ASSUMPTIONS

{assumptions}

EXPECTED OUTCOME

{expected_outcome}
"""
            )

# ==================================================
# TAB 2
# ==================================================

with tab2:

    st.header("Enterprise Learning Repository")

    df = load_records()

    st.metric(
        "Total Learning Records",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# ==================================================
# TAB 3
# ==================================================

with tab3:

    st.header("Outcome Review")

    df = load_records()

    if len(df) == 0:

        st.info(
            "No Learning Records available."
        )

    else:

        record_id = st.selectbox(
            "Select Learning Record",
            df["id"].tolist()
        )

        selected = df[
            df["id"] == record_id
        ].iloc[0]

        st.subheader(selected["title"])

        st.write("### Decision")
        st.write(selected["decision"])

        st.write("### Expected Outcome")
        st.write(selected["expected_outcome"])

        actual_outcome = st.text_area(
            "Actual Outcome",
            value=""
            if pd.isna(selected["actual_outcome"])
            else selected["actual_outcome"]
        )

        learning = st.text_area(
            "Learning",
            value=""
            if pd.isna(selected["learning"])
            else selected["learning"]
        )

        if st.button(
            "Save Outcome Review",
            use_container_width=True
        ):

            update_outcome(
                record_id,
                actual_outcome,
                learning
            )

            st.success(
                "Outcome Review Saved"
            )

# ==================================================
# TAB 4
# ==================================================

with tab4:

    st.header("Ask EDI")

    st.info(
        """
Future Organizational Intelligence Layer

Examples:

• Have we seen this before?

• Which assumptions repeatedly fail?

• What have we learned about partnerships?

• What patterns exist across strategic decisions?

This will become the Claude-powered retrieval layer.
"""
    )

    question = st.text_input(
        "Ask EDI",
        placeholder="What have we learned about partnerships?"
    )

    if question:

        df = load_records()

        if len(df) == 0:

            st.warning(
                "No Learning Records available."
            )

        else:

            question_lower = question.lower()

            matches = []

            for _, row in df.iterrows():

                text = " ".join(
                    [
                        str(row["title"]),
                        str(row["situation"]),
                        str(row["decision"]),
                        str(row["assumptions"]),
                        str(row["expected_outcome"]),
                        str(row["actual_outcome"]),
                        str(row["learning"])
                    ]
                ).lower()

                if any(
                    word in text
                    for word in question_lower.split()
                ):
                    matches.append(row)

            if len(matches) == 0:

                st.write(
                    "No matching learning records found."
                )

            else:

                st.success(
                    f"Found {len(matches)} related records."
                )

                for row in matches:

                    with st.expander(
                        f"{row['id']} - {row['title']}"
                    ):

                        st.write(
                            f"**Situation:** {row['situation']}"
                        )

                        st.write(
                            f"**Decision:** {row['decision']}"
                        )

                        st.write(
                            f"**Learning:** {row['learning']}"
                        )
=======
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
>>>>>>> 50f210bd86963ebefbf3865fa381bafd35c9adc3
