
import httpx
from src.config.settings import get_settings

settings = get_settings()


class DingTalkService:
    def __init__(self, app_key: str = None, app_secret: str = None):
        self.app_key = app_key or settings.DINGTALK_APP_KEY
        self.app_secret = app_secret or settings.DINGTALK_APP_SECRET
        self.base_url = "https://oapi.dingtalk.com"
        self._access_token = None

    async def get_access_token(self) -&gt; str:
        if self._access_token:
            return self._access_token
        
        url = f"{self.base_url}/gettoken"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={
                    "appkey": self.app_key,
                    "appsecret": self.app_secret
                }
            )
            result = response.json()
            if result.get("errcode") == 0:
                self._access_token = result["access_token"]
                return self._access_token
            raise Exception(f"钉钉API认证失败: {result.get('errmsg')}")

    async def get_department_list(self) -&gt; list:
        access_token = await self.get_access_token()
        url = f"{self.base_url}/topapi/v2/department/listsub"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={"access_token": access_token}
            )
            result = response.json()
            if result.get("errcode") == 0:
                return result.get("result", [])
            raise Exception(f"获取部门列表失败: {result.get('errmsg')}")

    async def get_department_users(self, dept_id: int) -&gt; list:
        access_token = await self.get_access_token()
        url = f"{self.base_url}/topapi/user/list"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={
                    "access_token": access_token,
                    "dept_id": dept_id
                }
            )
            result = response.json()
            if result.get("errcode") == 0:
                return result.get("result", {}).get("userlist", [])
            raise Exception(f"获取部门用户失败: {result.get('errmsg')}")

    async def send_work_notice(self, user_id: str, message: dict) -&gt; dict:
        access_token = await self.get_access_token()
        url = f"{self.base_url}/topapi/message/corpconversation/asyncsend_v2"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                params={"access_token": access_token},
                json={
                    "userid_list": user_id,
                    "msg": message
                }
            )
            result = response.json()
            if result.get("errcode") == 0:
                return result
            raise Exception(f"发送工作通知失败: {result.get('errmsg')}")

