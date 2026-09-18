import streamlit as st
import re



# =========================================================
# MOTIVELENS CLEAN PRESENTATION LAYER
# =========================================================
st.markdown("""
<style>
.block-container {
    max-width: 1120px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}
h1 { letter-spacing: -0.035em; }
h2, h3 { letter-spacing: -0.02em; }

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(49,51,63,.12);
}
[data-testid="stMetric"] {
    border: 1px solid rgba(49,51,63,.12);
    border-radius: 16px;
    padding: .9rem 1rem;
    background: #ffffff;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px !important;
    border-color: rgba(49,51,63,.12) !important;
    background: #ffffff;
}
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}
[data-testid="stAlert"] { border-radius: 12px; }

.ml-top {
    padding: 1.15rem 1.25rem;
    border: 1px solid rgba(49,51,63,.12);
    border-radius: 18px;
    margin-bottom: 1.2rem;
    background: linear-gradient(100deg,#faf9ff,#f7fbff);
}
.ml-top-title {
    font-size: 1.7rem;
    font-weight: 800;
    letter-spacing: -.04em;
    color: #202235;
}
.ml-top-sub {
    color: #626779;
    margin-top: .25rem;
    line-height: 1.5;
}
.ml-tag {
    display:inline-block;
    padding:.22rem .55rem;
    margin:.55rem .25rem 0 0;
    border-radius:999px;
    background:#f0edff;
    color:#5145a5;
    font-size:.73rem;
    font-weight:700;
}
.ml-eyebrow {
    font-size:.72rem;
    font-weight:800;
    letter-spacing:.1em;
    text-transform:uppercase;
    color:#7166b8;
    margin-bottom:.25rem;
}
.ml-help {
    color:#777c8c;
    font-size:.88rem;
    margin-top:-.3rem;
    margin-bottom:.8rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ml-top">
  <div class="ml-eyebrow">MotiveLens</div>
  <div class="ml-top-title">Understand your recommendation environment</div>
  <div class="ml-top-sub">
    Separate attention from intent, inspect goal relevance and commercial signals,
    and decide whether your feed is moving in the direction you actually want.
  </div>
  <span class="ml-tag">Attention ≠ Intent</span>
  <span class="ml-tag">Explainable</span>
  <span class="ml-tag">User-controlled</span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="MotiveLens",
    page_icon="🔍",
    layout="wide"
)


# =========================================================
# SESSION STORAGE
# =========================================================
if "interactions" not in st.session_state:
    st.session_state["interactions"] = []

if "intent_answers" not in st.session_state:
    st.session_state["intent_answers"] = {}

if "goal" not in st.session_state:
    st.session_state["goal"] = ""

if "interests" not in st.session_state:
    st.session_state["interests"] = ""

if "feed_direction_choice" not in st.session_state:
    st.session_state["feed_direction_choice"] = None

if "refocus_category" not in st.session_state:
    st.session_state["refocus_category"] = None


# =========================================================
# GOAL ALIGNMENT ENGINE
# =========================================================
def check_goal_alignment(goal, category, title, description):

    goal_text = goal.lower()

    content_text = (
        category + " " + title + " " + description
    ).lower()

    goal_connections = {
        "placement": [
            "programming",
            "java",
            "dsa",
            "coding",
            "interview",
            "software",
            "technical",
            "ai",
            "engineer"
        ],

        "software": [
            "programming",
            "java",
            "dsa",
            "coding",
            "interview",
            "software",
            "cloud",
            "technical",
            "ai",
            "engineer"
        ],

        "cloud": [
            "cloud",
            "aws",
            "azure",
            "technology"
        ],

        "ai": [
            "ai",
            "machine learning",
            "artificial intelligence",
            "python",
            "data science"
        ]
    }

    matched_evidence = []

    for goal_word, related_words in goal_connections.items():

        if goal_word in goal_text:

            for word in related_words:

                if word in content_text:
                    matched_evidence.append(word)

    matched_evidence = list(dict.fromkeys(matched_evidence))

    if matched_evidence:
        return True, matched_evidence

    return False, []


# =========================================================
# COMMERCIAL / INFLUENCE SIGNAL ENGINE
# =========================================================
def detect_commercial_signals(title, description):

    text = (title + " " + description).lower()

    signals = []

    # Discount patterns such as 70% OFF
    discount_matches = re.findall(
        r"\b\d{1,3}%\s*off\b",
        text
    )

    if discount_matches:
        signals.append(
            (
                "Discount",
                ", ".join(discount_matches)
            )
        )

    urgency_words = [
        "today",
        "limited-time",
        "limited time",
        "hurry",
        "last chance",
        "ends soon"
    ]

    urgency_found = []

    for word in urgency_words:
        if word in text:
            urgency_found.append(word)

    if urgency_found:
        signals.append(
            (
                "Urgency",
                ", ".join(urgency_found)
            )
        )

    call_to_action_words = [
        "enroll now",
        "buy now",
        "shop now",
        "book now",
        "sign up",
        "register now",
        "order now"
    ]

    action_found = []

    for phrase in call_to_action_words:
        if phrase in text:
            action_found.append(phrase)

    if action_found:
        signals.append(
            (
                "Call-to-action",
                ", ".join(action_found)
            )
        )

    return signals


# =========================================================
# DEMO RECOMMENDER ENGINE
# =========================================================
def calculate_demo_scores(interactions):
    scores = {}

    for interaction in interactions:
        category = interaction["category"]
        action = interaction["action"]

        if category not in scores:
            scores[category] = 0

        if action == "view":
            scores[category] += 1
        elif action == "like":
            scores[category] += 3
        elif action == "skip":
            scores[category] -= 2

    return scores


def get_strongest_categories(scores):
    positive_scores = {
        category: score
        for category, score in scores.items()
        if score > 0
    }

    if not positive_scores:
        return []

    highest_score = max(positive_scores.values())

    return [
        category
        for category, score in positive_scores.items()
        if score == highest_score
    ]


# =========================================================
# APP TITLE
# =========================================================
st.title("MotiveLens")

st.caption(
    "A social feed with user-side recommendation intelligence"
)


# =========================================================
# NAVIGATION
# =========================================================
page = st.sidebar.radio(
    "Navigate",
    [
        "My Space",
        "Discover",
        "MotiveLens Insights"
    ]
)

st.sidebar.caption(
    "MotiveLens audits recommendation evidence from the user's perspective: "
    "attention ≠ interest ≠ intent ≠ need."
)
st.sidebar.divider()

if st.sidebar.button("🧹 Reset Demo", use_container_width=True):
    for key in [
        "goal",
        "interests",
        "interactions",
        "intent_answers",
        "feed_direction_choice",
        "refocus_category"
    ]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


# =========================================================
# PAGE 1 - MY PROFILE
# =========================================================
if page == "My Space":

    st.header("👤 My Space")

    st.write(
        "Tell MotiveLens about your current goal and interests. "
        "These are explicit signals provided by you."
    )

    goal = st.text_input(
        "What is your current goal?",
        value=st.session_state["goal"],
        placeholder="Example: Prepare for software placements"
    )

    interests = st.text_input(
        "What are you interested in?",
        value=st.session_state["interests"],
        placeholder="Example: Technology, Cars, Cooking, Art, Comedy"
    )

    if st.button("Save Profile"):

        st.session_state["goal"] = goal
        st.session_state["interests"] = interests

        st.success("Profile saved!")


# =========================================================
# PAGE 2 - SOCIAL FEED
# =========================================================
elif page == "Discover":

    st.header("For You")

    st.caption(
        "Explore your personalized demo feed"
    )

    posts = [
        {
            "title": "Java DSA Roadmap for Coding Interviews",
            "creator": "Code Academy",
            "category": "Programming",
            "description":
                "Learn DSA concepts and prepare for technical interviews."
        },

        {
            "title": "BMW M5 Competition - Full Review",
            "creator": "Auto World",
            "category": "Cars",
            "description":
                "Performance, design and features of the BMW M5."
        },

        {
            "title": "AWS Cloud Engineer Roadmap",
            "creator": "Cloud Tech",
            "category": "Technology",
            "description":
                "A beginner roadmap to start a career in cloud computing."
        },

        {
            "title": "A Day in the Life of a Celebrity",
            "creator": "Daily Buzz",
            "category": "Entertainment",
            "description":
                "Behind the scenes of a celebrity lifestyle."
        },

        {
            "title": "Become an AI Engineer - 70% OFF Today!",
            "creator": "AI Mastery",
            "category": "Education",
            "description":
                "Limited-time offer. Enroll now and start learning AI."
        },

        {
            "title": "10-Minute Beginner Mobility Routine",
            "creator": "Move Daily",
            "category": "Fitness",
            "description":
                "A simple guided mobility routine for everyday movement."
        },

        {
            "title": "Weekend Travel Guide: Hidden Places to Explore",
            "creator": "Travel Notes",
            "category": "Travel",
            "description":
                "Ideas for short trips, local experiences and travel planning."
        },

        {
            "title": "Flash Sale - 50% OFF! Buy Now",
            "creator": "Shop Smart",
            "category": "Shopping",
            "description":
                "Limited-time shopping deal. Buy now before the offer ends."
        }
    ]


    # =====================================================
    # ADAPTIVE DEMO RECOMMENDER + EXPLICIT USER CONTROL
    # =====================================================
    demo_scores = calculate_demo_scores(
        st.session_state["interactions"]
    )

    strongest_categories = get_strongest_categories(demo_scores)
    preferred_category = st.session_state.get("refocus_category")

    if preferred_category:
        st.info(
            "🎯 **User-directed demo feed: "
            + preferred_category
            + "**\n\n"
            "You explicitly asked the MotiveLens demo to give more attention "
            "to "
            + preferred_category
            + ". This preference takes priority over engagement-only ranking."
        )

        posts = sorted(
            posts,
            key=lambda post: (
                post["category"] == preferred_category
            ),
            reverse=True
        )

    elif strongest_categories:

        if len(strongest_categories) == 1:
            strongest_category = strongest_categories[0]

            st.info(
                "🔄 **Demo feed tendency: "
                + strongest_category
                + "**\n\n"
                "The simulated recommender is moving "
                + strongest_category
                + " content higher because this category currently has "
                "the strongest recorded engagement signal."
            )

            posts = sorted(
                posts,
                key=lambda post: (
                    post["category"] == strongest_category
                ),
                reverse=True
            )

        else:
            st.info(
                "🔄 **Demo feed tendency: Tie between "
                + " & ".join(strongest_categories)
                + "**\n\n"
                "The simulated recommender sees equally strong engagement "
                "signals, so it is not forcing one tied category above "
                "the other."
            )

    else:
        st.caption(
            "🔄 Demo recommender: No strong positive engagement signal yet. "
            "Interact with the feed to let it adapt."
        )

    st.caption(
        "Demo behavior only — this simulated ranking does not represent "
        "the algorithm of any real social platform."
    )


    # =====================================================
    # DISPLAY POSTS
    # =====================================================
    for i, post in enumerate(posts):

        with st.container(border=True):

            st.subheader(
                post["title"]
            )

            st.caption(
                post["creator"]
            )

            st.write(
                post["description"]
            )

            st.write(
                "Category:",
                post["category"]
            )

            col1, col2, col3 = st.columns(3)


            # VIEW
            with col1:

                if st.button(
                    "👀 View",
                    key=f"view_{i}"
                ):

                    st.session_state["interactions"].append(
                        {
                            "title": post["title"],
                            "description": post["description"],
                            "category": post["category"],
                            "action": "view"
                        }
                    )

                    st.success("Viewed")


            # LIKE
            with col2:

                if st.button(
                    "❤️ Like",
                    key=f"like_{i}"
                ):

                    st.session_state["interactions"].append(
                        {
                            "title": post["title"],
                            "description": post["description"],
                            "category": post["category"],
                            "action": "like"
                        }
                    )

                    st.success("Liked")


            # SKIP
            with col3:

                if st.button(
                    "⏭ Skip",
                    key=f"skip_{i}"
                ):

                    st.session_state["interactions"].append(
                        {
                            "title": post["title"],
                            "description": post["description"],
                            "category": post["category"],
                            "action": "skip"
                        }
                    )

                    st.info("Skipped")


# =========================================================
# PAGE 3 - MOTIVELENS INSIGHTS
# =========================================================
elif page == "MotiveLens Insights":

    st.header(
        "MotiveLens Insights"
    )

    st.caption(
        "Understanding what your engagement actually means"
    )


    # -----------------------------------------------------
    # CURRENT USER GOAL
    # -----------------------------------------------------
    if st.session_state["goal"]:

        st.info(
            "🎯 **Your current goal:** "
            + st.session_state["goal"]
        )

    else:

        st.warning(
            "No goal has been set. "
            "Add your current goal in My Profile."
        )


    # -----------------------------------------------------
    # CURRENT INTERESTS
    # -----------------------------------------------------
    if st.session_state["interests"]:

        st.caption(
            "Explicit interests: "
            + st.session_state["interests"]
        )


    interactions = st.session_state["interactions"]


    # -----------------------------------------------------
    # NO ACTIVITY
    # -----------------------------------------------------
    if not interactions:

        st.info(
            "Use the Social Feed first to generate some activity."
        )


    # -----------------------------------------------------
    # ANALYZE ACTIVITY
    # -----------------------------------------------------
    else:

        category_engagement = {}

        for interaction in interactions:

            category = interaction["category"]
            action = interaction["action"]

            if category not in category_engagement:
                category_engagement[category] = 0

            if action == "view":
                category_engagement[category] += 1

            elif action == "like":
                category_engagement[category] += 3

            elif action == "skip":
                category_engagement[category] -= 2


        # =================================================
        # RECOMMENDATION PATTERN DASHBOARD
        # =================================================
        st.subheader("📊 Attention Map")
        st.caption("Where your positive engagement is concentrated. This does not prove intent or need.")

        positive_scores = {
            category: max(score, 0)
            for category, score in category_engagement.items()
        }

        total_positive_score = sum(positive_scores.values())

        if total_positive_score > 0:

            category_percentages = {
                category: (score / total_positive_score) * 100
                for category, score in positive_scores.items()
                if score > 0
            }

            sorted_percentages = sorted(
                category_percentages.items(),
                key=lambda item: item[1],
                reverse=True
            )

            for category, percentage in sorted_percentages:
                st.write(
                    f"**{category}:** {percentage:.1f}% "
                    "of observed positive engagement"
                )
                st.progress(percentage / 100)

            highest_percentage = max(category_percentages.values())

            strongest_categories = [
                category
                for category, percentage in category_percentages.items()
                if abs(percentage - highest_percentage) < 0.0001
            ]

            if len(strongest_categories) == 1:
                st.success(
                    "📌 **Strongest observed engagement signal:** "
                    + strongest_categories[0]
                )
            else:
                st.success(
                    "📌 **Strongest observed engagement signals:** "
                    + " & ".join(strongest_categories)
                    + " (tie)"
                )

            st.caption(
                "Calculated from interactions recorded in this MotiveLens demo: "
                "View = +1, Like = +3, Skip = -2. "
                "Percentages represent observed positive engagement share, "
                "not the internal algorithm or recommendation percentage of "
                "Instagram, YouTube, or any other real platform."
            )

            st.info(
                "A high engagement share shows where your attention is "
                "currently concentrated. It does not by itself prove your "
                "intent, need, or goal."
            )

        else:
            st.info(
                "There is not enough positive engagement yet to calculate "
                "a recommendation pattern. View or like some content first."
            )


        # =================================================
        # RECOMMENDER VS MOTIVELENS
        # =================================================
        strongest_demo_categories = get_strongest_categories(category_engagement)

        st.subheader("🧭 Feed Direction & Diversity")
        st.caption("A transparent demo view of whether your engagement is broad or becoming concentrated.")

        drift_scores = calculate_demo_scores(st.session_state.get("interactions", []))
        positive_drift_scores = {
            category: max(score, 0)
            for category, score in drift_scores.items()
            if max(score, 0) > 0
        }
        positive_drift_total = sum(positive_drift_scores.values())

        if positive_drift_total == 0:
            st.info(
                "Not enough positive engagement evidence yet to evaluate feed drift "
                "or diversity. View or like a few posts in the demo feed first."
            )
        else:
            drift_shares = {
                category: (score / positive_drift_total) * 100
                for category, score in positive_drift_scores.items()
            }
            drift_category = max(drift_shares, key=drift_shares.get)
            drift_share = drift_shares[drift_category]
            active_categories = len(drift_shares)

            if drift_share >= 75:
                drift_label = f"Strong concentration toward {drift_category}"
            elif drift_share >= 55:
                drift_label = f"Emerging concentration toward {drift_category}"
            else:
                drift_label = "No single category strongly dominates"

            if active_categories <= 1 or drift_share >= 75:
                diversity_label = "Concentrated"
                diversity_explanation = (
                    "Most observed positive engagement is currently centered on one "
                    "category, so the interaction pattern is relatively narrow."
                )
            elif active_categories >= 3 and drift_share < 55:
                diversity_label = "Broad"
                diversity_explanation = (
                    "Positive engagement is distributed across several categories "
                    "without one category strongly dominating."
                )
            else:
                diversity_label = "Moderate"
                diversity_explanation = (
                    "Positive engagement spans more than one category, but some "
                    "concentration is still visible."
                )

            col_drift, col_diversity = st.columns(2)
            with col_drift:
                st.metric("📈 Drift signal", drift_label)
            with col_diversity:
                st.metric("🌐 Diversity", diversity_label)

            st.write(
                f"**Observed concentration:** {drift_category} currently represents "
                f"**{drift_share:.1f}%** of positive engagement evidence in this demo."
            )
            st.write(f"**Diversity interpretation:** {diversity_explanation}")

            st.info(
                "MotiveLens surfaces this concentration instead of assuming it is "
                "what you want. A concentrated pattern may be intentional, temporary, "
                "or simply caused by what captured your attention."
            )
            st.caption(
                "Prototype measure only. Drift and diversity are calculated from "
                "interactions recorded in this MotiveLens demo using the same scoring "
                "scheme as Recommendation Pattern (View = +1, Like = +3, Skip = -2). "
                "They do not measure the internal behavior of any real platform."
            )

        st.subheader("🎛️ Take Control")
        st.caption("Tell the demo whether the current direction is intentional or explicitly refocus it.")

        if positive_drift_total == 0:
            st.info(
                "Interact with the demo feed first. MotiveLens will offer feed "
                "direction controls once an engagement pattern is visible."
            )
        else:
            st.write(
                f"Your current observed pattern is most concentrated toward "
                f"**{drift_category}**. Is this direction intentional?"
            )

            control_col1, control_col2 = st.columns(2)

            with control_col1:
                if st.button(
                    "✅ Keep this direction",
                    key="keep_feed_direction",
                    use_container_width=True
                ):
                    st.session_state["feed_direction_choice"] = "keep"
                    st.session_state["refocus_category"] = None

            with control_col2:
                if st.button(
                    "🎯 Help me refocus",
                    key="refocus_feed_direction",
                    use_container_width=True
                ):
                    st.session_state["feed_direction_choice"] = "refocus"

            if st.session_state["feed_direction_choice"] == "keep":
                st.success(
                    f"You confirmed that the current concentration toward "
                    f"**{drift_category}** is intentional. MotiveLens records "
                    "your choice instead of treating concentration itself as a problem."
                )

            elif st.session_state["feed_direction_choice"] == "refocus":
                refocus_options = [
                    "Programming",
                    "Technology",
                    "Cars",
                    "Entertainment",
                    "Education",
                    "Fitness",
                    "Travel",
                    "Shopping"
                ]

                selected_refocus_category = st.selectbox(
                    "Which topic would you like the demo feed to give more attention to?",
                    refocus_options,
                    index=(
                        refocus_options.index(st.session_state["refocus_category"])
                        if st.session_state["refocus_category"] in refocus_options
                        else 0
                    ),
                    key="refocus_selector"
                )

                if st.button(
                    "Apply my preference",
                    key="apply_refocus_preference",
                    use_container_width=True
                ):
                    st.session_state["refocus_category"] = selected_refocus_category

                if st.session_state["refocus_category"]:
                    st.success(
                        "User preference recorded: give more attention to "
                        f"**{st.session_state['refocus_category']}**."
                    )
                    st.info(
                        "This is explicit user input. The MotiveLens demo will "
                        "prioritize this preference instead of relying only on "
                        "engagement signals."
                    )

        st.caption(
            "User Control changes only the MotiveLens demo feed. "
            "It does not modify recommendations on any real social platform."
        )

        st.subheader("🔍 What engagement says vs what MotiveLens knows")

        if len(strongest_demo_categories) == 1:
            strongest_category = strongest_demo_categories[0]
            related_items = [
                item for item in interactions
                if item["category"] == strongest_category
            ]
            latest_strongest_item = related_items[-1]

            st.write(
                "**Demo Recommender sees:** "
                + strongest_category
                + " currently has the strongest engagement signal, "
                "so the simulated feed prioritizes this category."
            )

            confirmed_reason = st.session_state["intent_answers"].get(
                strongest_category
            )

            if confirmed_reason:
                st.write(
                    "**MotiveLens adds user context:** Your confirmed reason "
                    "for engaging with " + strongest_category
                    + " content is **" + confirmed_reason + "**."
                )
            else:
                st.write(
                    "**MotiveLens adds user context:** Your intent for "
                    + strongest_category
                    + " is still unknown. Engagement alone is not enough "
                    "to infer why you are engaging."
                )

            if st.session_state["goal"]:
                aligned, evidence = check_goal_alignment(
                    st.session_state["goal"],
                    strongest_category,
                    latest_strongest_item["title"],
                    latest_strongest_item["description"]
                )
                if aligned:
                    st.write(
                        "**Goal relationship:** Potentially aligned with "
                        "your current stated goal."
                    )
                else:
                    st.write(
                        "**Goal relationship:** A relationship to your "
                        "current stated goal is not established."
                    )
            else:
                st.write(
                    "**Goal relationship:** Cannot evaluate because "
                    "no current goal is set."
                )

            if confirmed_reason == "Entertainment":
                st.info(
                    "💡 **Key insight:** Strong engagement with "
                    + strongest_category
                    + " shows attention and possible interest, but your "
                    "confirmed reason is entertainment. MotiveLens therefore "
                    "does not treat this engagement as evidence of purchase "
                    "intent or goal-related need."
                )
            elif confirmed_reason:
                st.info(
                    "💡 **Key insight:** The recommender reacts to engagement, "
                    "while MotiveLens keeps your explicitly confirmed reason "
                    "separate from attention. High engagement alone does not "
                    "prove a need or final action."
                )
            else:
                st.info(
                    "💡 **Key insight:** The simulated recommender can react "
                    "to attention before your intent is known. MotiveLens "
                    "keeps intent unknown instead of guessing it."
                )

        elif len(strongest_demo_categories) > 1:
            st.write(
                "**Demo Recommender sees:** A tie between "
                + " & ".join(strongest_demo_categories) + "."
            )
            st.info(
                "💡 **MotiveLens interpretation:** There is no single "
                "strongest engagement category yet, so the demo should not "
                "pretend that one category clearly represents your intent."
            )
        else:
            st.info(
                "Not enough positive engagement is available for a "
                "recommender comparison yet."
            )


        st.subheader(
            "What MotiveLens Observed"
        )


        # =================================================
        # ANALYZE EACH CATEGORY
        # =================================================
        for category, engagement in category_engagement.items():

            if engagement > 0:

                with st.container(border=True):

                    st.write(
                        "###",
                        category
                    )


                    # =====================================
                    # FIND LATEST INTERACTION
                    # =====================================
                    related_interactions = [
                        item
                        for item in interactions
                        if item["category"] == category
                    ]

                    latest_item = related_interactions[-1]


                    # =====================================
                    # GOAL / NEED ALIGNMENT
                    # =====================================
                    if not st.session_state["goal"]:

                        st.write(
                            "🧭 **Goal / Need Alignment:** "
                            "Cannot evaluate because no goal is set."
                        )

                    else:

                        is_aligned, evidence = check_goal_alignment(
                            st.session_state["goal"],
                            category,
                            latest_item["title"],
                            latest_item["description"]
                        )

                        if is_aligned:

                            st.success(
                                "🧭 **Goal / Need Alignment:** "
                                "Potentially aligned with your "
                                "current stated goal."
                            )

                            st.caption(
                                "Related evidence found: "
                                + ", ".join(evidence)
                            )

                        else:

                            st.info(
                                "🧭 **Goal / Need Alignment:** "
                                "Relationship to your current "
                                "stated goal is not established."
                            )

                            st.caption(
                                "This does not mean the content is "
                                "bad or irrelevant to you. It only "
                                "means MotiveLens found no evidence "
                                "connecting it to your current goal."
                            )


                    # =====================================
                    # ATTENTION + INTEREST
                    # =====================================
                    if engagement >= 3:

                        st.write(
                            "👀 **Attention:** "
                            "Repeated engagement detected"
                        )

                        st.write(
                            "💡 **Interest:** "
                            "There is evidence that this topic "
                            "is interesting to you."
                        )

                    else:

                        st.write(
                            "👀 **Attention:** "
                            "Some engagement detected"
                        )

                        st.write(
                            "💡 **Interest:** "
                            "Possible, but evidence is limited."
                        )


                    # =====================================
                    # COMMERCIAL / INFLUENCE SIGNALS
                    # =====================================
                    commercial_signals = detect_commercial_signals(
                        latest_item["title"],
                        latest_item["description"]
                    )

                    if commercial_signals:

                        st.warning(
                            "🛍️ **Commercial / Influence Signals:** "
                            "Promotional signals detected."
                        )

                        for signal_type, signal_evidence in commercial_signals:

                            st.write(
                                f"• **{signal_type}:** "
                                f"{signal_evidence}"
                            )

                        st.caption(
                            "These signals do not mean the recommendation "
                            "is bad or misleading. They show that promotional "
                            "language is present and may be useful context "
                            "when interpreting the recommendation."
                        )

                    else:

                        st.write(
                            "🛍️ **Commercial / Influence Signals:** "
                            "No clear promotional signals detected."
                        )


                    # =====================================
                    # RECOMMENDATION INTEREST BALANCE
                    # =====================================
                    st.write("#### ⚖️ Recommendation Interest Balance")

                    user_evidence = []
                    commercial_evidence = []

                    # User-side: goal relationship
                    if st.session_state["goal"]:
                        balance_aligned, balance_goal_evidence = check_goal_alignment(
                            st.session_state["goal"],
                            category,
                            latest_item["title"],
                            latest_item["description"]
                        )
                        if balance_aligned:
                            user_evidence.append("Related to your stated goal")

                    # User-side: explicit interests
                    explicit_interest_text = st.session_state["interests"].lower()
                    if (
                        explicit_interest_text
                        and category.lower() in explicit_interest_text
                    ):
                        user_evidence.append(
                            "Matches an interest you explicitly provided"
                        )

                    # User-side: observed engagement
                    if engagement > 0:
                        user_evidence.append(
                            "Positive engagement with this category"
                        )

                    # User-side: confirmed context
                    balance_intent = st.session_state["intent_answers"].get(category)
                    if balance_intent and balance_intent != "Don't want to specify":
                        user_evidence.append(
                            "Confirmed context: " + balance_intent
                        )

                    # Commercial-side: detected promotional evidence
                    for signal_type, signal_evidence in commercial_signals:
                        commercial_evidence.append(
                            signal_type + ": " + signal_evidence
                        )

                    total_balance_evidence = (
                        len(user_evidence) + len(commercial_evidence)
                    )

                    if total_balance_evidence > 0:
                        user_share = (
                            len(user_evidence) / total_balance_evidence
                        ) * 100
                        commercial_share = (
                            len(commercial_evidence) / total_balance_evidence
                        ) * 100

                        balance_col1, balance_col2 = st.columns(2)

                        with balance_col1:
                            st.metric(
                                "👤 User-side evidence share",
                                f"{user_share:.0f}%"
                            )

                        with balance_col2:
                            st.metric(
                                "🏢 Commercial-signal evidence share",
                                f"{commercial_share:.0f}%"
                            )

                        if user_evidence:
                            st.write("**User-side evidence found:**")
                            for evidence_item in user_evidence:
                                st.write("✓ " + evidence_item)
                        else:
                            st.write(
                                "**User-side evidence found:** "
                                "No clear user-relevance evidence detected."
                            )

                        if commercial_evidence:
                            st.write("**Commercial-side evidence found:**")
                            for evidence_item in commercial_evidence:
                                st.write("⚠ " + evidence_item)
                        else:
                            st.write(
                                "**Commercial-side evidence found:** "
                                "No obvious promotional signals detected."
                            )

                        if user_share > commercial_share:
                            tendency = "User-side evidence is more prominent"
                        elif commercial_share > user_share:
                            tendency = "Commercial-signal evidence is more prominent"
                        else:
                            tendency = "Mixed / balanced detected evidence"

                        st.info(
                            "**Evidence tendency:** " + tendency + ".\n\n"
                            "MotiveLens compares only the evidence it can observe "
                            "in this prototype. This describes the detected signal "
                            "balance, not who secretly benefits from or controls "
                            "the recommendation."
                        )

                        st.caption(
                            "These percentages are explainable evidence-share "
                            "scores based only on the signals listed above. "
                            "They are not probabilities, benefit percentages, "
                            "or proof of a company's motive, and they do not reveal "
                            "a real platform's private recommendation algorithm."
                        )


                    # =====================================
                    # INTENT - ASK, DON'T ASSUME
                    # =====================================
                    if category not in st.session_state[
                        "intent_answers"
                    ]:

                        st.warning(
                            "🎯 **Intent:** Unknown — "
                            "engagement alone does not prove "
                            "what you intend to do."
                        )

                        st.write(
                            "**Why are you engaging with "
                            + category
                            + " content?**"
                        )

                        answer = st.selectbox(
                            "Choose the closest reason",
                            [
                                "Select an option",
                                "Entertainment",
                                "Learning",
                                "Research",
                                "Comparing options",
                                "Planning to take action",
                                "Don't want to specify"
                            ],
                            key=f"intent_{category}"
                        )

                        if st.button(
                            "Confirm",
                            key=f"confirm_{category}"
                        ):

                            if answer != "Select an option":

                                st.session_state[
                                    "intent_answers"
                                ][category] = answer

                                st.rerun()


                    # =====================================
                    # USER-CONFIRMED CONTEXT
                    # =====================================
                    else:

                        answer = st.session_state[
                            "intent_answers"
                        ][category]

                        st.success(
                            "🎯 **User-confirmed context:** "
                            + answer
                        )


                        if answer == "Entertainment":

                            st.write(
                                "MotiveLens will not interpret "
                                "your engagement as evidence "
                                "that you intend to purchase "
                                "or take action."
                            )


                        elif answer == "Learning":

                            st.write(
                                "Your engagement is currently "
                                "understood as learning interest "
                                "rather than an automatic action "
                                "or purchase intention."
                            )


                        elif answer == "Research":

                            st.write(
                                "Your engagement provides evidence "
                                "of research interest, but "
                                "MotiveLens does not assume a "
                                "final decision."
                            )


                        elif answer == "Comparing options":

                            st.write(
                                "You are comparing options. "
                                "This provides stronger intent "
                                "evidence, but does not prove "
                                "that a final action will occur."
                            )


                        elif answer == "Planning to take action":

                            st.write(
                                "You have explicitly indicated "
                                "an intention to take action. "
                                "This is stronger evidence than "
                                "engagement alone."
                            )


                        else:

                            st.write(
                                "MotiveLens keeps your intent "
                                "unspecified rather than guessing it."
                            )