import streamlit as st

from email_processor import clean_email
from llm import analyze_email, generate_smart_reply

from gmail_service import get_gmail_service
from gmail_service import get_emails
from gmail_service import get_email_details


st.set_page_config(
    page_title="SmartMail AI",
    page_icon="📧",
    layout="centered"
)


st.title("📧 SmartMail AI")

st.subheader(
    "LLM-Based Email Classification & Smart Reply Generator"
)


# Connect to Gmail
if st.button("📬 Connect Gmail"):

    with st.spinner("Connecting to Gmail..."):

        service = get_gmail_service()

        emails = get_emails(
            service,
            max_results=5
        )

    st.session_state["gmail_service"] = service
    st.session_state["emails"] = emails

    st.success(
        f"{len(emails)} emails found!"
    )


# Show emails
if "emails" in st.session_state:

    st.markdown("### 📩 Your Recent Emails")

    for index, email in enumerate(
        st.session_state["emails"]
    ):

        service = st.session_state[
            "gmail_service"
        ]

        details = get_email_details(
            service,
            email["id"]
        )

        subject = details["subject"]

        if not subject:
            subject = "(No subject)"

        if st.button(
            subject,
            key=f"email_{index}"
        ):

            st.session_state[
                "selected_email"
            ] = details


# Analyze selected email
if "selected_email" in st.session_state:

    email = st.session_state[
        "selected_email"
    ]

    st.markdown("### 📧 Selected Email")

    st.write(
        "**From:**",
        email["sender"]
    )

    st.write(
        "**Subject:**",
        email["subject"]
    )

    st.write(
        "**Date:**",
        email["date"]
    )

    st.text_area(
        "Email Body",
        email["body"],
        height=250
    )


    if st.button("🤖 Analyze Email"):

        cleaned_email = clean_email(
            email["body"]
        )

        with st.spinner(
            "Gemini is analyzing the email..."
        ):

            result = analyze_email(
                cleaned_email
            )

        st.success(
            "Email analysis completed!"
        )

        st.markdown("### 📊 AI Analysis")

        st.write(result)
        st.markdown("### 💬 Smart Reply")

if st.button("✨ Generate Smart Reply"):

    cleaned_email = clean_email(
        email["body"]
    )

    with st.spinner(
        "Gemini is generating a smart reply..."
    ):

        reply = generate_smart_reply(
            cleaned_email
        )

    st.success(
        "Smart reply generated!"
    )

    st.text_area(
        "Generated Reply",
        reply,
        height=180
    )