import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BOM Risk Analyzer",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "https://bom-risk-analyzer-api.onrender.com"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        padding: 30px 0 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔧 BOM Risk Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered electronic component procurement '
    'and supply-chain risk intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Control Center")

    st.write(
        "Upload a Bill of Materials to evaluate "
        "component procurement risk."
    )

    st.divider()

    # --------------------------------------------------------
    # BACKEND STATUS
    # --------------------------------------------------------

    st.subheader("Backend Status")

    try:

        response = requests.get(
            f"{API_URL}/",
            timeout=3
        )

        if response.status_code == 200:

            st.success("🟢 Backend Online")

        else:

            st.warning("🟡 Backend Responding")

    except requests.exceptions.RequestException:

        st.error("🔴 Backend Offline")

        st.caption(
            "Start FastAPI with:"
        )

        st.code(
            "uvicorn app:app --reload",
            language="powershell"
        )

    st.divider()

    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    st.subheader("ℹ️ About")

    st.caption(
        "The platform combines machine-learning "
        "risk prediction, component enrichment, "
        "substitute recommendation and AI-generated "
        "risk explanations."
    )

    st.divider()

    st.caption(
        "BOM Risk Analyzer • AI Domain-X Challenge 2026"
    )


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_result" not in st.session_state:

    st.session_state["analysis_result"] = None


if "uploaded_filename" not in st.session_state:

    st.session_state["uploaded_filename"] = None


# ============================================================
# BOM UPLOAD
# ============================================================

st.header("📤 Upload Bill of Materials")

st.write(
    "Upload a CSV containing your BOM components. "
    "The backend will validate and analyze the file."
)

uploaded_file = st.file_uploader(
    "Choose a BOM CSV file",
    type=["csv"],
    help="CSV files only."
)


# ============================================================
# FILE PREVIEW
# ============================================================

if uploaded_file is not None:

    st.session_state["uploaded_filename"] = (
        uploaded_file.name
    )

    st.success(
        f"✓ Uploaded: **{uploaded_file.name}**"
    )

    try:

        preview_df = pd.read_csv(
            uploaded_file
        )

        st.subheader("📋 BOM Preview")

        preview_col1, preview_col2 = st.columns(
            [3, 1]
        )

        with preview_col1:

            st.dataframe(
                preview_df.head(10),
                use_container_width=True,
                hide_index=True
            )

        with preview_col2:

            st.metric(
                "Rows",
                len(preview_df)
            )

            st.metric(
                "Columns",
                len(preview_df.columns)
            )

        st.caption(
            "Showing the first 10 rows."
        )

    except Exception as e:

        st.error(
            f"Could not read the CSV: {e}"
        )


# ============================================================
# ANALYZE BUTTON
# ============================================================

if uploaded_file is not None:

    st.divider()

    analyze_button = st.button(
        "🔍 Analyze BOM",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        with st.status(
            "🤖 AI is analyzing your BOM...",
            expanded=True
        ) as status:

            st.write(
                "📋 Sending BOM to the analysis engine..."
            )

            st.write(
                "🧠 Running machine-learning risk analysis..."
            )

            st.write(
                "🔄 Evaluating substitute components..."
            )

            st.write(
                "🤖 Generating AI risk explanations..."
            )

            try:

                uploaded_file.seek(0)

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/csv"
                    )
                }

                response = requests.post(
                    f"{API_URL}/analyze",
                    files=files,
                    timeout=300
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state[
                        "analysis_result"
                    ] = result

                    status.update(
                        label="✅ BOM analysis complete!",
                        state="complete",
                        expanded=False
                    )

                    st.success(
                        "Analysis completed successfully."
                    )

                else:

                    try:

                        error_detail = (
                            response.json()
                            .get(
                                "detail",
                                response.text
                            )
                        )

                    except Exception:

                        error_detail = response.text

                    status.update(
                        label="❌ Analysis failed",
                        state="error",
                        expanded=True
                    )

                    st.error(
                        f"Backend error "
                        f"({response.status_code}): "
                        f"{error_detail}"
                    )

            except requests.exceptions.Timeout:

                status.update(
                    label="⏱️ Analysis timed out",
                    state="error",
                    expanded=True
                )

                st.error(
                    "The backend took longer than "
                    "5 minutes to complete the analysis."
                )

                st.info(
                    "The backend performs AI analysis "
                    "for each component, so larger BOMs "
                    "may take longer."
                )

            except requests.exceptions.ConnectionError:

                status.update(
                    label="🔴 Backend unavailable",
                    state="error",
                    expanded=True
                )

                st.error(
                    "Could not connect to the FastAPI backend."
                )

            except Exception as e:

                status.update(
                    label="❌ Unexpected error",
                    state="error",
                    expanded=True
                )

                st.error(
                    f"Unexpected error: {e}"
                )

else:

    st.info(
        "👆 Upload a CSV BOM file to begin."
    )


# ============================================================
# GET ANALYSIS RESULT
# ============================================================

result = st.session_state.get(
    "analysis_result"
)


# ============================================================
# EVERYTHING BELOW ONLY APPEARS AFTER ANALYSIS
# ============================================================

if result is not None:

    # ========================================================
    # GET COMPONENT RESULTS
    # ========================================================

    components = result.get(
        "risk_ranked_components",
        []
    )

    total_components = result.get(
        "total_components",
        len(components)
    )


    # ========================================================
    # PREPARE DATA
    # ========================================================

    prepared_rows = []

    for item in components:

        component = item.get(
            "component",
            {}
        )

        risk = item.get(
            "risk_analysis",
            {}
        )

        recommendation = item.get(
            "substitute_recommendation",
            {}
        )

        prepared_rows.append({

            "Part Number":
                component.get(
                    "part_number",
                    "Unknown"
                ),

            "Category":
                component.get(
                    "category",
                    "Unknown"
                ),

            "Criticality":
                component.get(
                    "criticality",
                    "Unknown"
                ),

            "Risk Score":
                risk.get(
                    "score",
                    0
                ),

            "Risk Level":
                risk.get(
                    "level",
                    "Unknown"
                ),

            "Substitute":
                recommendation.get(
                    "part_number"
                ),

            "Compatibility":
                recommendation.get(
                    "compatibility_percentage",
                    0
                )
        })


    analysis_df = pd.DataFrame(
        prepared_rows
    )


    # ========================================================
    # HANDLE EMPTY RESULTS
    # ========================================================

    if analysis_df.empty:

        st.warning(
            "The backend returned no component results."
        )

    else:

        # ====================================================
        # RISK COUNTS
        # ====================================================

        high_count = int(
            (
                analysis_df["Risk Level"]
                .astype(str)
                .str.upper()
                == "HIGH"
            ).sum()
        )

        medium_count = int(
            (
                analysis_df["Risk Level"]
                .astype(str)
                .str.upper()
                == "MEDIUM"
            ).sum()
        )

        low_count = int(
            (
                analysis_df["Risk Level"]
                .astype(str)
                .str.upper()
                == "LOW"
            ).sum()
        )


        # ====================================================
        # HEALTH SCORE
        # ====================================================

        average_risk = (
            pd.to_numeric(
                analysis_df["Risk Score"],
                errors="coerce"
            )
            .fillna(0)
            .mean()
        )

        health_score = round(
            max(
                0,
                min(
                    100,
                    100 - average_risk
                )
            )
        )


        # ====================================================
        # HEALTH LABEL
        # ====================================================

        if health_score >= 80:

            health_label = "HEALTHY"
            health_icon = "🟢"

        elif health_score >= 60:

            health_label = "MODERATE"
            health_icon = "🟡"

        else:

            health_label = "AT RISK"
            health_icon = "🔴"


        # ====================================================
        # TOP 5 RISKS
        # ====================================================

        top_risks = (
            analysis_df
            .sort_values(
                "Risk Score",
                ascending=False
            )
            .head(5)
        )


        # ====================================================
        # EXECUTIVE DASHBOARD
        # ====================================================

        st.divider()

        st.header(
            "📊 BOM Executive Dashboard"
        )

        st.caption(
            f"Analysis results for "
            f"**{st.session_state.get('uploaded_filename', 'BOM')}**"
        )


        # ====================================================
        # METRIC CARDS
        # ====================================================

        metric1, metric2, metric3, metric4, metric5 = st.columns(5)


        with metric1:

            st.metric(
                "📦 Components",
                total_components
            )


        with metric2:

            st.metric(
                "🔴 High Risk",
                high_count
            )


        with metric3:

            st.metric(
                "🟡 Medium Risk",
                medium_count
            )


        with metric4:

            st.metric(
                "🟢 Low Risk",
                low_count
            )


        with metric5:

            st.metric(
                f"{health_icon} BOM Health",
                f"{health_score}/100"
            )


        # ====================================================
        # HEALTH SECTION
        # ====================================================

        st.divider()

        health_col1, health_col2 = st.columns(
            [1, 2]
        )


        with health_col1:

            st.subheader(
                "❤️ BOM Health"
            )

            st.metric(
                "Overall Health Score",
                f"{health_score}/100"
            )

            st.write(
                f"{health_icon} **{health_label}**"
            )


        with health_col2:

            st.subheader(
                "Health Indicator"
            )

            st.progress(
                health_score
            )

            if health_score >= 80:

                st.success(
                    "The BOM has a strong overall "
                    "procurement risk profile."
                )

            elif health_score >= 60:

                st.warning(
                    "The BOM contains moderate "
                    "procurement risks that should be monitored."
                )

            else:

                st.error(
                    "The BOM contains significant "
                    "procurement risks requiring attention."
                )


        # ====================================================
        # RISK DISTRIBUTION
        # ====================================================

        st.divider()

        st.header(
            "📈 Risk Profile"
        )


        risk_data = pd.DataFrame({

            "Risk Level": [
                "HIGH",
                "MEDIUM",
                "LOW"
            ],

            "Components": [
                high_count,
                medium_count,
                low_count
            ]
        })


        chart_col1, chart_col2 = st.columns(2)


        with chart_col1:

            fig_pie = px.pie(
                risk_data,
                names="Risk Level",
                values="Components",
                title="Risk Distribution",
                hole=0.5
            )

            fig_pie.update_traces(
                textposition="inside",
                textinfo="label+percent"
            )

            st.plotly_chart(
                fig_pie,
                use_container_width=True
            )


        with chart_col2:

            fig_bar = px.bar(
                risk_data,
                x="Risk Level",
                y="Components",
                text="Components",
                title="Components by Risk Level"
            )

            fig_bar.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )


        # ====================================================
        # TOP 5 RISKS
        # ====================================================

        st.divider()

        st.header(
            "🏆 Top 5 Components Requiring Attention"
        )


        if not top_risks.empty:

            for rank, (_, row) in enumerate(
                top_risks.iterrows(),
                start=1
            ):

                risk_level = str(
                    row["Risk Level"]
                ).upper()


                if risk_level == "HIGH":

                    icon = "🔴"

                elif risk_level == "MEDIUM":

                    icon = "🟡"

                else:

                    icon = "🟢"


                col1, col2, col3, col4 = st.columns(
                    [0.5, 3, 2, 2]
                )


                with col1:

                    st.write(
                        f"**{rank}**"
                    )


                with col2:

                    st.write(
                        f"{icon} **{row['Part Number']}**"
                    )

                    st.caption(
                        str(row["Category"])
                    )


                with col3:

                    st.write(
                        f"**Risk:** {risk_level}"
                    )


                with col4:

                    st.write(
                        f"**Score:** "
                        f"{row['Risk Score']}/100"
                    )


        # ====================================================
        # ACTION CENTER
        # ====================================================

        st.divider()

        st.header(
            "🚨 Action Center"
        )


        action_col1, action_col2, action_col3 = st.columns(3)


        with action_col1:

            st.error(
                f"🔴 **{high_count} HIGH-risk component(s)**"
            )

            if high_count > 0:

                st.write(
                    "Immediate engineering review "
                    "is recommended."
                )

            else:

                st.write(
                    "No high-risk components detected."
                )


        with action_col2:

            st.warning(
                f"🟡 **{medium_count} MEDIUM-risk component(s)**"
            )

            if medium_count > 0:

                st.write(
                    "Monitor supply conditions and "
                    "prepare alternate sourcing."
                )

            else:

                st.write(
                    "No medium-risk components detected."
                )


        with action_col3:

            st.success(
                f"🟢 **{low_count} LOW-risk component(s)**"
            )

            if low_count > 0:

                st.write(
                    "No immediate procurement action "
                    "is required."
                )

            else:

                st.write(
                    "No low-risk components detected."
                )


        # ====================================================
        # COMPONENT EXPLORER
        # ====================================================

        st.divider()

        st.header(
            "🔍 Component Explorer"
        )

        st.write(
            "Search and filter components to investigate "
            "individual procurement risks."
        )


        filter_col1, filter_col2, filter_col3 = st.columns(
            [2, 1, 1]
        )


        with filter_col1:

            search_term = st.text_input(
                "Search component",
                placeholder="Enter part number..."
            )


        with filter_col2:

            selected_risk = st.selectbox(
                "Risk Level",
                [
                    "ALL",
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ]
            )


        with filter_col3:

            categories = sorted(
                analysis_df["Category"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_category = st.selectbox(
                "Category",
                ["ALL"] + categories
            )


        # ====================================================
        # APPLY FILTERS
        # ====================================================

        filtered_df = analysis_df.copy()


        if search_term:

            filtered_df = filtered_df[
                filtered_df["Part Number"]
                .astype(str)
                .str.contains(
                    search_term,
                    case=False,
                    na=False
                )
            ]


        if selected_risk != "ALL":

            filtered_df = filtered_df[
                filtered_df["Risk Level"]
                .astype(str)
                .str.upper()
                == selected_risk
            ]


        if selected_category != "ALL":

            filtered_df = filtered_df[
                filtered_df["Category"]
                .astype(str)
                == selected_category
            ]


        st.caption(
            f"Showing **{len(filtered_df)}** component(s)."
        )


        # ====================================================
        # TABLE
        # ====================================================

        if not filtered_df.empty:

            display_df = filtered_df[
                [
                    "Part Number",
                    "Category",
                    "Criticality",
                    "Risk Score",
                    "Risk Level",
                    "Substitute",
                    "Compatibility"
                ]
            ].copy()


            display_df = display_df.sort_values(
                "Risk Score",
                ascending=False
            )


            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No components match the selected filters."
            )


        # ====================================================
        # DETAILED COMPONENT ANALYSIS
        # ====================================================

        st.divider()

        st.header(
            "🧩 Detailed Component Analysis"
        )


        for item in components:

            component = item.get(
                "component",
                {}
            )

            risk = item.get(
                "risk_analysis",
                {}
            )

            recommendation = item.get(
                "substitute_recommendation",
                {}
            )

            explanation = item.get(
                "ai_explanation",
                ""
            )


            part_number = component.get(
                "part_number",
                "Unknown"
            )

            category = component.get(
                "category",
                "Unknown"
            )

            criticality = component.get(
                "criticality",
                "Unknown"
            )

            risk_score = risk.get(
                "score",
                0
            )

            risk_level = str(
                risk.get(
                    "level",
                    "Unknown"
                )
            )

            risk_level_upper = risk_level.upper()


            if risk_level_upper == "HIGH":

                icon = "🔴"

            elif risk_level_upper == "MEDIUM":

                icon = "🟡"

            else:

                icon = "🟢"


            with st.expander(
                f"{icon} {part_number} | "
                f"{risk_level_upper} | "
                f"Risk Score: {risk_score}/100"
            ):

                # --------------------------------------------
                # COMPONENT INFORMATION
                # --------------------------------------------

                st.subheader(
                    "📦 Component Information"
                )


                info1, info2, info3 = st.columns(3)


                with info1:

                    st.write(
                        "**Part Number**"
                    )

                    st.write(
                        part_number
                    )


                with info2:

                    st.write(
                        "**Category**"
                    )

                    st.write(
                        category
                    )


                with info3:

                    st.write(
                        "**Criticality**"
                    )

                    st.write(
                        criticality
                    )


                st.divider()


                # --------------------------------------------
                # RISK ANALYSIS
                # --------------------------------------------

                st.subheader(
                    "⚠️ Risk Analysis"
                )


                score_col1, score_col2 = st.columns(
                    [1, 3]
                )


                with score_col1:

                    st.metric(
                        "Risk Score",
                        f"{risk_score}/100"
                    )

                    st.write(
                        f"**Risk Level:** "
                        f"{icon} {risk_level_upper}"
                    )


                with score_col2:

                    st.write(
                        "**Risk Severity**"
                    )

                    score_value = max(
                        0,
                        min(
                            100,
                            int(float(risk_score))
                        )
                    )

                    st.progress(
                        score_value
                    )


                # --------------------------------------------
                # RISK FACTORS
                # --------------------------------------------

                factors = risk.get(
                    "factors",
                    {}
                )


                if factors:

                    st.subheader(
                        "📌 Risk Factor Breakdown"
                    )


                    factor_cols = st.columns(
                        len(factors)
                    )


                    for factor_index, (
                        factor_name,
                        factor_value
                    ) in enumerate(
                        factors.items()
                    ):

                        with factor_cols[
                            factor_index
                        ]:

                            display_name = (
                                str(factor_name)
                                .replace(
                                    "_",
                                    " "
                                )
                                .title()
                            )

                            st.metric(
                                display_name,
                                factor_value
                            )


                st.divider()


                # --------------------------------------------
                # SUBSTITUTE RECOMMENDATION
                # --------------------------------------------

                st.subheader(
                    "🔄 Substitute Recommendation"
                )


                substitute = recommendation.get(
                    "part_number"
                )

                compatibility = recommendation.get(
                    "compatibility_percentage",
                    0
                )

                alternative_type = recommendation.get(
                    "alternative_type",
                    "Unknown"
                )

                reason = recommendation.get(
                    "reason",
                    "No reason provided."
                )


                if substitute:

                    sub_col1, sub_col2, sub_col3 = st.columns(
                        3
                    )


                    with sub_col1:

                        st.write(
                            "**Recommended Component**"
                        )

                        st.success(
                            str(substitute)
                        )


                    with sub_col2:

                        st.write(
                            "**Compatibility**"
                        )

                        st.metric(
                            "Match",
                            f"{compatibility}%"
                        )


                    with sub_col3:

                        st.write(
                            "**Alternative Type**"
                        )

                        st.write(
                            alternative_type
                        )


                    st.write(
                        f"**Reason:** {reason}"
                    )


                    try:

                        compatibility_value = int(
                            float(
                                compatibility
                            )
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        compatibility_value = 0


                    compatibility_value = max(
                        0,
                        min(
                            100,
                            compatibility_value
                        )
                    )


                    st.progress(
                        compatibility_value
                    )


                else:

                    st.warning(
                        "No suitable substitute was found."
                    )


                st.divider()


                # --------------------------------------------
                # AI EXPLANATION
                # --------------------------------------------

                st.subheader(
                    "🤖 AI Risk Explanation"
                )


                if explanation:

                    st.markdown(
                        explanation
                    )

                else:

                    st.info(
                        "No AI explanation was returned."
                    )


        # ====================================================
        # EXPORT
        # ====================================================

        st.divider()

        st.header(
            "📥 Export Analysis"
        )


        export_rows = []


        for item in components:

            component = item.get(
                "component",
                {}
            )

            risk = item.get(
                "risk_analysis",
                {}
            )

            recommendation = item.get(
                "substitute_recommendation",
                {}
            )


            export_rows.append({

                "Part Number":
                    component.get(
                        "part_number"
                    ),

                "Category":
                    component.get(
                        "category"
                    ),

                "Criticality":
                    component.get(
                        "criticality"
                    ),

                "Risk Score":
                    risk.get(
                        "score"
                    ),

                "Risk Level":
                    risk.get(
                        "level"
                    ),

                "Suggested Substitute":
                    recommendation.get(
                        "part_number"
                    ),

                "Compatibility %":
                    recommendation.get(
                        "compatibility_percentage"
                    ),

                "Alternative Type":
                    recommendation.get(
                        "alternative_type"
                    ),

                "Recommendation Reason":
                    recommendation.get(
                        "reason"
                    )
            })


        export_df = pd.DataFrame(
            export_rows
        )


        csv_data = export_df.to_csv(
            index=False
        )


        download_col1, download_col2 = st.columns(2)


        with download_col1:

            st.download_button(
                label="⬇️ Download CSV Report",
                data=csv_data,
                file_name="bom_risk_analysis.csv",
                mime="text/csv",
                use_container_width=True
            )


        with download_col2:

            st.download_button(
                label="⬇️ Download Raw JSON",
                data=pd.Series(result).to_json(
                    indent=2
                ),
                file_name="bom_risk_analysis.json",
                mime="application/json",
                use_container_width=True
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        BOM Risk Analyzer • AI-powered procurement intelligence
    </div>
    """,
    unsafe_allow_html=True
)