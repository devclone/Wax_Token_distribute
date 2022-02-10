#!/usr/bin/python3

import contract
import time
import logging
from logger import log
from settings import user_param
from settings import cfg

class Distribute:
    def __init__(self) -> None:
        self.log: logging.LoggerAdapter = log
        self.wax_account: str = user_param.wax_account

    # 签署交易(只许成功，否则抛异常）
    def wax_transact(self, transaction: dict):

        self.log.debug("begin transact: {0}".format(transaction))
        success, result = contract.push_transaction(transaction)
        if success:
            self.log.debug("transact ok, transaction_id: [{0}]".format(result["transaction_id"]))
            self.log.debug("transact result: {0}".format(result))
            time.sleep(cfg.transact_interval)
            return result
        else:
            if "is greater than the maximum billable" in result:
                self.log.error("CPU资源不足，可能需要质押更多WAX，一般为误报，稍后重试 maximum")
            elif "estimated CPU time (0 us) is not less than the maximum billable CPU time for the transaction (0 us)" in result:
                self.log.error("CPU资源不足，可能需要质押更多WAX，一般为误报，稍后重试 estimated")
            else:
                self.log.error("transact error: {0}".format(result))
            raise TransactException(result)

    def start(self):
        self.log.info("正在分发资金...")

        for account in user_param.to_accounts:
            for key in account.keys():
                fwf = format(account[key], '.4f')
                quantity = fwf + " FWF"

                transaction = {
                    "actions": [{
                        "account": "farmerstoken",
                        "name": "transfer",
                        "authorization": [{
                            "actor": self.wax_account,
                            "permission": "active",
                        }],
                        "data": {
                            "from": self.wax_account,
                            "to" : key,
                            "quantity": quantity,
                            "memo": "distribution",
                        },
                    }],
                }
                self.log.info(f"Send {account[key]} FWF to {key}")
                self.wax_transact(transaction)
        
        self.log.info("资金分发完成！！")

class FarmerException(Exception):
    pass

# 调用智能合约出错，此时应停止并检查日志，不宜反复重试
class TransactException(FarmerException):
    # 有的智能合约错误可以重试,-1为无限重试
    def __init__(self, msg, retry=True, max_retry_times: int = -1):
        super().__init__(msg)
        self.retry = retry
        self.max_retry_times = max_retry_times
