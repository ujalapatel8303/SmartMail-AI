import base64

from gmail_service import get_gmail_service
from gmail_service import get_emails


def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]

    return ""


service = get_gmail_service()

emails = get_emails(
    service,
    max_results=5
)

print("Number of emails found:", len(emails))


for email in emails:

    message = service.users().messages().get(
        userId="me",
        id=email["id"],
        format="full"
    ).execute()

    headers = message["payload"]["headers"]

    sender = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date = get_header(headers, "Date")

    body = ""

    payload = message["payload"]

    if "parts" in payload:

        for part in payload["parts"]:

            if part["mimeType"] == "text/plain":

                data = part["body"].get("data")

                if data:
                    body = base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

                break

    else:

        data = payload["body"].get("data")

        if data:
            body = base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore"
            )


    print("\n==============================")
    print("FROM:", sender)
    print("SUBJECT:", subject)
    print("DATE:", date)
    print("BODY:")
    print(body[:1000])