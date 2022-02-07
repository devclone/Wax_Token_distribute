#!/usr/bin/python3

import contract
import time

class Distribute:
    def __init__(self) -> None:
        pass

    # 签署交易(只许成功，否则抛异常）
    def wax_transact(self, transaction: dict):

        self.log.info("begin transact: {0}".format(transaction))
        success, result = contract.push_transaction(transaction)
        if success:
            self.log.info("transact ok, transaction_id: [{0}]".format(result["transaction_id"]))
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