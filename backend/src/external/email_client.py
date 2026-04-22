
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.settings import get_settings

settings = get_settings()


class EmailService:
    def __init__(self, host=None, port=None, username=None, password=None):
        self.host = host or settings.SMTP_HOST
        self.port = port or settings.SMTP_PORT
        self.username = username or settings.SMTP_USERNAME
        self.password = password or settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM or self.username

    async def send_tender_notice(self, to_emails, tender_info):
        if not self.host:
            return False

        subject = f"【招标通知】{tender_info.get('title', '招标项目')}"

        html_content = f"""
        <html>
        <body>
            <h2>{subject}</h2>
            <p>尊敬的供应商：</p>
            <p>您好！现邀请您参与以下招标项目：</p>
            <ul>
                <li><strong>项目名称：</strong>{tender_info.get('title', '')}</li>
                <li><strong>截止时间：</strong>{tender_info.get('deadline', '')}</li>
            </ul>
            <p>请点击以下链接提交应标文件：</p>
            <p><a href="{tender_info.get('bid_url', '#')}">{tender_info.get('bid_url', '#')}</a></p>
            <p>此致</p>
            <p>招标管理系统</p>
        </body>
        </html>
        """

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = self.from_email
        message["To"] = ", ".join(to_emails)
        message.attach(MIMEText(html_content, "html"))

        try:
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True
            )
            return True
        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False

    async def send_winner_notice(self, to_email, result_info):
        if not self.host:
            return False

        subject = "【中标通知】恭喜您中标！"

        html_content = f"""
        <html>
        <body>
            <h2>{subject}</h2>
            <p>尊敬的供应商：</p>
            <p>恭喜！贵公司在以下招标项目中成功中标：</p>
            <ul>
                <li><strong>项目名称：</strong>{result_info.get('tender_title', '')}</li>
                <li><strong>中标金额：</strong>{result_info.get('quote_amount', '')}</li>
            </ul>
            <p>请尽快与我们联系签订合同。</p>
            <p>此致</p>
            <p>招标管理系统</p>
        </body>
        </html>
        """

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = self.from_email
        message["To"] = to_email
        message.attach(MIMEText(html_content, "html"))

        try:
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True
            )
            return True
        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False
