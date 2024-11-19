import streamlit as st
import requests

st.set_page_config(page_title="Email Generator with Follow-up", page_icon="📬", layout="wide")

API_URL = "http://127.0.0.1:8000"

def main():
    col1, col2 = st.columns(2)
    with col1:
        st.title("Email Generator")

        sender_name = st.text_input("Sender's Name")
        recipient_name = st.text_input("Recipient's Name")
        subject = st.text_input("Subject/Topic")
        extra_detail = st.text_input("Extra Detail (Optional)")
        tone = st.selectbox("Tone", ['Formal', 'Casual', 'Friendly'])
        preferred_length = st.selectbox("Preferred Length", ['Short', 'Medium', 'Long'])

    with col2:
        st.title("Email Preview")

    if st.button("Create Email"):
        if sender_name and recipient_name and subject:
            email_request = {
                "sender_name": sender_name,
                "recipient_name": recipient_name,
                "subject": subject,
                "extra_detail": extra_detail,
                "tone": tone,
                "preferred_length": preferred_length,
                "follow_up": False
            }
            response = requests.post(f"{API_URL}/generate-email/", json=email_request)
            email_content = response.json().get("email_content")

            with st.expander("Preview Email", expanded=True):
                st.write(email_content)

            email_outcome = st.radio("Choose an Outcome:", ["No Reply", "Seenzoned", "Not Opened"])
            
            if email_outcome:
                if st.button("Follow-Up"):
                    follow_up_request = email_request.copy()
                    follow_up_request['follow_up'] = True
                    follow_up_response = requests.post(f"{API_URL}/generate-email/", json=follow_up_request)
                    follow_up_content = follow_up_response.json().get("email_content")
                    st.write(follow_up_content)

                if st.button("Send a Message Instead"):
                    message_content = st.text_input("Message Content")
                    if message_content:
                        message_request = {
                            "sender_name": sender_name,
                            "recipient_name": recipient_name,
                            "message_content": message_content
                        }
                        message_response = requests.post(f"{API_URL}/send-message/", json=message_request)
                        st.write(message_response.json().get("message_sent"))
        else:
            st.warning("Please fill in all required fields.")

if __name__ == "__main__":
    main()
