import sys, smtplib 
import base64
# from email.message import EmailMessage
from azure.communication.email import EmailClient


# SENDER_EMAIL = "daniellee7618@gmail.com"
# APP_PASSWORD = "dasiibnkdopwfppn"  # Store securely in env vars later
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 465

CONNECTION_STRING = "your_azure_connection_string_here"
SENDER_EMAIL = "donotreply@your-verified-domain.azurecomm.net"

def main():
    # Entry point for the CLI
    print("=== Buoy CLI: Command Sender ===")

    imei = input("Enter IMEI (e.g., 300234012345678): ")
    command = input("Enter command (e.g., RELAY ON 3): ")
    recipient = input("Enter recipient email: ")

    # Save the command into a .sbd file
    sbd_filename = "command.sbd"
    try:
        with open(sbd_filename, "w") as f:
            f.write(command)
    except Exception as e:
        print(f"Error writing .sbd file: {e}")
        return

    # Base64 encode the .sbd file
    try:
        with open(sbd_filename, "rb") as f:
            encoded_attachment = base64.b64encode(f.read()).decode()
    except Exception as e:
        print(f"Error reading .sbd file: {e}")
        return

    # Construct message for Azure
    message = {
        "content": {
            "subject": f"Command for IMEI {imei}",
            "plainText": f"Attached is the command for IMEI {imei}.",
            "html": f"<html><p>Attached is the command for IMEI {imei}.</p></html>"
        },
        "recipients": {
            "to": [
                {
                    "address": recipient,
                    "displayName": "Command Receiver"
                }
            ]
        },
        "senderAddress": SENDER_EMAIL,
        "attachments": [
            {
                "contentInBase64": encoded_attachment,
                "contentType": "application/octet-stream",
                "name": sbd_filename
            }
        ]
    }

    # Send the email using Azure EmailClient
    try:
        client = EmailClient.from_connection_string(CONNECTION_STRING)
        poller = client.begin_send(message)
        result = poller.result()
        if result["status"] == "Succeeded":
            print("Command sent successfully!")
        else:
            print("Failed to send:", result["error"])
    except Exception as e:
        print(f"Azure email sending failed: {e}")

if __name__ == "__main__":
    main()