import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class EmailService:
    """
    Serviço responsável pelo envio de e-mails, como recuperação de senha.
    Isola a complexidade da biblioteca smtplib e formatação MIME.
    """

    @staticmethod
    def send_password_reset_email(user_email: str, code: str) -> None:
        """
        Envia um e-mail com código de recuperação de senha.

        Parâmetros:
        - user_email (str): O endereço de e-mail do destinatário.
        - code (str): O código de 4 dígitos gerado para o reset.

        Retorno:
        - None

        Comportamento:
        - Utiliza as variáveis de ambiente EMAIL_SENDER e EMAIL_PASSWORD.
        - Se as variáveis não estiverem configuradas, apenas loga um aviso (para dev).
        """
        sender_email = os.environ.get("EMAIL_SENDER")
        sender_password = os.environ.get("EMAIL_PASSWORD")
        
        if not sender_email or not sender_password:
            print("Aviso: EMAIL_SENDER ou EMAIL_PASSWORD não configurados no .env")
            return

        try:
            msg = MIMEMultipart('related')
            msg['From'] = sender_email
            msg['To'] = user_email
            msg['Subject'] = "Recuperação de Senha - Raízes Locais"
            
            msg_alternative = MIMEMultipart('alternative')
            msg.attach(msg_alternative)

            text = f"Seu código de recuperação é: {code}\\nEste código expira em 15 minutos."
            html = f"""\
            <html>
                <head>
                <style>
                    .container {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    text-align: center;
                    }}
                    .logo {{
                    max-width: 150px;
                    margin-bottom: 20px;
                    }}
                    .code {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #4CAF50;
                    letter-spacing: 5px;
                    margin: 20px 0;
                    padding: 10px;
                    background: #f9f9f9;
                    border-radius: 5px;
                    }}
                    .footer {{
                    margin-top: 30px;
                    font-size: 12px;
                    color: #777;
                    }}
                </style>
                </head>
                <body>
                <div class="container">
                    <img src="cid:logo_image" alt="Raízes Locais Logo" class="logo">
                    <h2>Recuperação de Senha</h2>
                    <p>Olá,</p>
                    <p>Recebemos uma solicitação para redefinir a sua senha no aplicativo <strong>Raízes Locais</strong>.</p>
                    <p>Utilize o código abaixo no aplicativo para criar uma nova senha:</p>
                    <div class="code">{code}</div>
                    <p>Este código expira em 15 minutos.</p>
                    <p>Se você não solicitou a recuperação, pode ignorar este email com segurança.</p>
                    <div class="footer">
                    <p>&copy; 2026 Raízes Locais. Todos os direitos reservados.</p>
                    </div>
                </div>
                </body>
            </html>
            """
            msg_alternative.attach(MIMEText(text, 'plain'))
            msg_alternative.attach(MIMEText(html, 'html'))
            
            # Anexando logo se existir
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            logo_path = os.path.join(project_root, 'frontend', 'assets', 'logo.png')
            
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    img_data = f.read()
                image = MIMEImage(img_data, name='logo.png')
                image.add_header('Content-ID', '<logo_image>')
                msg.attach(image)
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())
            server.quit()
            print(f"--- EMAIL SENT TO {user_email} ---")
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise Exception("Erro ao enviar o email de recuperação.")
