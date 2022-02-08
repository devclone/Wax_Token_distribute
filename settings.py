from dataclasses import dataclass
from datetime import timedelta


@dataclass
class Settings:
    path_logs: str

    # 发送合约请求的间隔
    transact_interval = 10

# 用户配置参数
class user_param:
    wax_account: str = None
    private_key: str = None
    rpc_domain_list: list = []
    rpc_domain: str = None
    to_accounts: list = []

    @staticmethod
    def to_dict():
        return {
            "wax_account": user_param.wax_account,
            "private_key": user_param.private_key,
            "rpc_domain_list": user_param.rpc_domain_list,
            "rpc_domain": user_param.rpc_domain,
            "to_accounts": user_param.to_accounts, 
        }


def load_user_param(user: dict):
    user_param.wax_account = user["wax_account"]
    user_param.private_key = user.get("private_key", None)
    user_param.rpc_domain_list = user.get("rpc_domain_list", ['https://api.wax.alohaeos.com'])
    user_param.rpc_domain = user.get("rpc_domain", 'https://api.wax.alohaeos.com')
    user_param.to_accounts = user.get("to_accounts", [])

cfg = Settings(
    path_logs="./logs/",
)
