
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.settings import get_settings

settings = get_settings()


class EmailService:
    def __init__(self, host: str = None, port: int = None, username: str = None, password: str = None):
        self.host = host or settings.SMTP_HOST
        self.port = port or settings.SMTP_PORT
        self.username = username or settings.SMTP_USERNAME
        self.password = password or settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM or self.username

    async def send_tender_notice(self, to_emails: list, tender_info: dict) -&gt; bool:
        if not self.host:
            return False
        
        subject = f"【招标通知】{tender_info.get('title', '招标项目')}"
        
        html_content = f"""
        &lt;html&gt;
        &lt;body&gt;
            &lt;h2&gt;{subject}&lt;/h2&gt;
            &lt;p&gt;尊敬的供应商：&lt;/p&gt;
            &lt;p&gt;您好！现邀请您参与以下招标项目：&lt;/p&gt;
            &lt;ul&gt;
                &lt;li&gt;&lt;strong&gt;项目名称：&lt;/strong&gt;{tender_info.get('title', '')}&lt;/li&gt;
                &lt;li&gt;&lt;strong&gt;截止时间：&lt;/strong&gt;{tender_info.get('deadline', '')}&lt;/li&gt;
            &lt;/ul&gt;
            &lt;p&gt;请点击以下链接提交应标文件：&lt;/p&gt;
            &lt;p&gt;&lt;a href="{tender_info.get('bid_url', '#')}"&gt;{tender_info.get('bid_url', '#')}&lt;/a&gt;&lt;/p&gt;
            &lt;p&gt;此致&lt;/p&gt;
            &lt;p&gt;招标管理系统&lt;/p&gt;
        &lt;/body&gt;
        &lt;/html&gt;
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

    async def send_winner_notice(self, to_email: str, result_info: dict) -&gt; bool:
        if not self.host:
            return False
        
        subject = "【中标通知】恭喜您中标！"
        
        html_content = f"""
        &lt;html&gt;
        &lt;body&gt;
            &lt;h2&gt;{subject}&lt;/h2&gt;
            &lt;p&gt;尊敬的供应商：&lt;/p&gt;
            &lt;p&gt;恭喜！贵公司在以下招标项目中成功中标：&lt;/p&gt;
            &lt;ul&gt;
                &lt;li&gt;&lt;strong&gt;项目名称：&lt;/strong&gt;{result_info.get('tender_title', '')}&lt;/li&gt;
                &lt;li&gt;&lt;strong&gt;中标金额：&lt;/strong&gt;{result_info.get('quote_amount', '')}&lt;/li&gt;
            &lt;/ul&gt;
            &lt;p&gt;请尽快与我们联系签订合同。&lt;/p&gt;
            &lt;p&gt;此致&lt;/p&gt;
            &lt;p&gt;招标管理系统&lt;/p&gt;
        &lt;/body&gt;
        &lt;/html&gt;
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

