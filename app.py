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