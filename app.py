import streamlit as st
import sqlite3
import pandas as pd

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
    category TEXT,
    impact TEXT,
    confidence INTEGER,
    owner TEXT,

    situation TEXT,
    decision TEXT,
    assumptions TEXT,

    expected_outcome TEXT,
    actual_outcome TEXT,

    success_rating TEXT,

    learning TEXT,
    evidence TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

try:
    cursor.execute(
        "ALTER TABLE learning_records ADD COLUMN success_rating TEXT"
    )
    conn.commit()
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE learning_records ADD COLUMN category TEXT"
    )
    conn.commit()
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE learning_records ADD COLUMN impact TEXT"
    )
    conn.commit()
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE learning_records ADD COLUMN confidence INTEGER"
    )
    conn.commit()
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE learning_records ADD COLUMN owner TEXT"
    )
    conn.commit()
except:
        pass

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def load_records():

    return pd.read_sql_query(
        """
        SELECT
            id,
            title,
            category,
            impact,
            confidence,
            owner,
            situation,
            decision,
            assumptions,
            expected_outcome,
            actual_outcome,
            success_rating,
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
    category,
    impact,
    confidence,
    owner,
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
            category,
            impact,
            confidence,
            owner,
            situation,
            decision,
            assumptions,
            expected_outcome,
            evidence
        )
        
        VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?)
        """,
        (
            title,
            category,
            impact,
            confidence,
            owner,
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
    success_rating,
    learning
):

    cursor.execute(
    """
    UPDATE learning_records
    SET
        actual_outcome = ?,
        success_rating = ?,
        learning = ?
    WHERE id = ?
    """,
    (
        actual_outcome,
        success_rating,
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
    "Enterprise Decision Infrastructure"
)

st.caption(
    "Testing the hypothesis that autonomous enterprises will require systems of record for decisions, just as they require systems of record for customers, transactions, work, and data."
)

st.markdown("""
### Organizations have systems of record for:

• Customers (CRM)

• Transactions (ERP)

• Work (Project Systems)

• Data (Data Platforms)

# They do not have systems of record for decisions.
""")

st.info(
    """
Organizations can usually answer:

✓ What happened?

✓ Who did it?

✓ When did it happen?

Organizations often struggle to answer:

✕ Why was a decision made?

✕ Which assumptions drove it?

✕ Which assumptions proved wrong?

✕ What should future teams learn?
"""
)

st.markdown("---")

# --------------------------------------------------
# TABS
# --------------------------------------------------


# --------------------------------------------------
# EXECUTIVE DASHBOARD
# --------------------------------------------------

df = load_records()

total_decisions = len(df)

total_reviews = len(
    df[df["actual_outcome"].notna()]
)

total_learnings = len(
    df[df["learning"].notna()]
)

coverage = round(
    (total_learnings / max(total_decisions, 1)) * 100
)

success_count = len(
    df[
        df["success_rating"].isin(
            [
                "Exceeded Expectations",
                "Met Expectations"
            ]
        )
    ]
)

success_rate = round(
    success_count /
    max(total_reviews, 1) * 100
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Decisions", total_decisions)

with col2:
    st.metric("Reality Checks", total_reviews)

with col3:
    st.metric("Learnings", total_learnings)

with col4:
    st.metric(
        "Memory Coverage",
        f"{coverage}%"
    )

with col5:
    st.metric(
        "Success Rate",
        f"{success_rate}%"
    )

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Decision Workspace",
        "Decision Memory",
        "Decision Analysis",
        "Decision Intelligence"
    ]
)

# ==================================================
# TAB 1
# ==================================================

with tab1:

    st.header("The Decision Record")

    
    category = st.selectbox(
    "Decision Category",
    [
        "Strategic Partnership",
        "Enterprise AI",
        "Vendor Selection",
        "Technology Adoption",
        "Product Launch",
        "Capital Allocation",
        "Hiring"
    ]
)

    impact = st.selectbox(
    "Business Impact",
    [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]
)

    confidence = st.slider(
    "Decision Confidence",
    0,
    100,
    70
)

    owner = st.text_input(
    "Decision Owner",
    placeholder="Strategy Team"
)

    title = st.text_input(
        "Decision Title",
        placeholder="Enter decision title"
    )

    st.caption(
        """
Examples:

• Enterprise AI Transformation

• Strategic Partnership

• Vendor Selection

• Capital Allocation

• Product Launch

• Autonomous Agent Deployment
"""
    )

    situation = st.text_area(
        "Context",
        placeholder="""
Describe the business context, stakeholders, constraints, and factors influencing this decision.
"""
    )

    decision = st.text_area(
        "Decision",
        placeholder="""
Describe the decision being considered.
"""
    )

    assumptions = st.text_area(
        "Assumptions",
        placeholder="""
What assumptions must be true for this decision to succeed?

Examples:

- Market demand exists
- Adoption targets are realistic
- Required resources are available
- Regulatory conditions remain favorable
"""
    )

    expected_outcome = st.text_area(
        "Expected Outcome",
        placeholder="""
What outcome do you expect if these assumptions prove correct?
"""
    )

    evidence = st.text_area(
        "Evidence",
        placeholder="""
Links, research, decks, documents, supporting information.
"""
    )

    if st.button(
        "Save Decision Record",
        use_container_width=True
    ):

        if (
            title.strip() == ""
            or situation.strip() == ""
            or decision.strip() == ""
        ):

            st.error(
                "Decision Title, Context and Decision are required."
            )

        else:

            save_learning_record(
                title,
                category,
                impact,
                confidence,
                owner,
                situation,
                decision,
                assumptions,
                expected_outcome,
                evidence
            )

            st.success(
                "Decision Record Created"
            )

# ==================================================
# TAB 2
# ==================================================

with tab2:

    st.header("Decision Repository")

    df = load_records()

    st.metric(
        "Total Decision Records",
        len(df)
    )

    display_cols = [
        "id",
        "title",
        "owner",
        "category",
        "impact",
        "confidence",
        "success_rating",
        "created_at"
    ]

    available_cols = [
        c for c in display_cols
        if c in df.columns
    ]

    st.write("DEBUG COLUMNS")
    st.write(df.columns.tolist())

    st.dataframe(
        df[available_cols],
        use_container_width=True
    )
   

# ==================================================
# TAB 3
# ==================================================

with tab3:

    st.header("Reality Check")

    df = load_records()

    if len(df) == 0:

        st.info(
            "No Decision Records available."
        )

    else:

        record_id = st.selectbox(
            "Select Decision Record",
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
        
        success_rating = st.selectbox(
    "Outcome Rating",
    [
        "Exceeded Expectations",
        "Met Expectations",
        "Partially Successful",
        "Failed"
    ]
)



        learning = st.text_area(
            "Learning",
            value=""
            if pd.isna(selected["learning"])
            else selected["learning"]
        )

        if st.button(
            "Save Reality Check",
            use_container_width=True
        ):

            update_outcome(
                record_id,
                actual_outcome,
                success_rating,
                learning
            )

            st.success(
                "Decision Memory Updated"
            )

# ==================================================
# TAB 4
# ==================================================

with tab4:

    st.header("Ask EDI")

    st.info(
        """
Future Decision Intelligence Layer

Examples:

• Why did similar decisions fail?

• Which assumptions repeatedly break?

• What have we learned about partnerships?

• What should future teams know?

• Which decisions created the most value?

This will become the retrieval layer for organizational decision memory.
"""
    ) 
    
    st.info(
    """
Future Enterprise Retrieval Layer

Examples:

• Should we deploy autonomous agents into production?

• Why did previous AI transformation initiatives fail?

• Which assumptions repeatedly break across strategic programs?

• What have we learned from high-risk enterprise decisions?

• Which decisions created durable organizational value?

This prototype demonstrates how organizational decision memory
can become queryable intelligence.
"""
)

    question = st.text_input(
        "Ask Decision Memory",
        placeholder="Which assumptions repeatedly failed across strategic decisions?"
    )

    if question:

        df = load_records()

        if len(df) == 0:

            st.warning(
                "No Decision Records available."
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
                    "No matching decision records found."
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
                            f"**Context:** {row['situation']}"
                        )

                        st.write(
                            f"**Decision:** {row['decision']}"
                        )

                        st.write(
                            f"**Learning:** {row['learning']}"
                        )