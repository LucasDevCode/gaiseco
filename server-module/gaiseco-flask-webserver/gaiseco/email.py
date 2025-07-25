import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def format_email_body(employee, original_prompt, marked_prompt):
    text = f"""\
        GaiSeCo - ALERT
        Empregado: {employee}
        Possível cometeu um erro de segurança/compliance: 
        Em anexo seguem: o prompt original e prompt com a marcação da falha de segurança."""
    
    return text
    

def format_email_body_html(employee, original_prompt, marked_prompt, list_issues):
    html = """\
        <html>
        <head>
            <style>
                table, th, td {
                    border: 1px solid rgb(78, 102, 168);
                    border-collapse: collapse;
                    padding: 5px;
                }
            </style>
        </head>
        """
    html += f"""\
        <body>
            <h1> GaiSeCo - ALERT </h1>
            <br>
            <p> Empregado: {employee} </p>
            <br>
            <p>Possível cometeu um erro de segurança/compliance: </p>
            <br>
    
            <table>
                <tr>
                    <th>Tipo de Falha</th>
                    <th>Score</th>
                </tr>
        """
    
    for issue in list_issues:
        html += f"""\
                    <tr>
                        <td> {issue['type']} </td>
                        <td> {issue['score']} </td>
                    </tr>
        """

    html += f"""\
            </table>
            <br>
            <p>Em anexo seguem: o prompt original e prompt com a marcação da falha de segurança.</p>
        </body>
        </html>
        """
    return html




     
def send_email(receivers_email: list, employee:str, original_prompt: str, marked_prompt: str, list_issues):
    obj = None

    with open(file='data.json', mode='r') as f:
        obj = json.load( f )

    message = MIMEMultipart("alternative")
    message["Subject"] = f"GAISeCo: Prompts de {employee} possui falha de Compliance e Security"
    message["From"] = obj["sender_email"]
    message["To"] = ", ".join(receivers_email)

    # Create the plain-text and HTML version of your message
    text = format_email_body(employee, original_prompt, marked_prompt)
    html = format_email_body_html(employee, original_prompt, marked_prompt,list_issues)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    part3 = MIMEText(original_prompt)
    part3.add_header('Content-Disposition', 'attachment', filename='prompt_original.txt')

    part4 = MIMEText(marked_prompt)
    part4.add_header('Content-Disposition', 'attachment', filename='prompt_marked_issues.txt')
    

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    message.attach(part3)
    message.attach(part4)
    

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(obj["sender_email"], obj["password"])
        server.sendmail(
            obj["sender_email"], receivers_email, message.as_string()
        )

    return None