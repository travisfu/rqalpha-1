# -*- coding: utf-8 -*-

from rqalpha import run_file

# config = {
#   "base": {
#     "start_date": "2016-06-01",
#     "end_date": "2016-12-01",
#     "benchmark": "000300.XSHG",
#     "accounts": {
#       "stock": 100000
#     }
#   },
#   "extra": {
#     "log_level": "verbose",
#   },
#   "mod": {
#     "sys_analyser": {
#       "enabled": True,
#       "plot": True
#     }
#   }
# }

config = {
  "base": {
      "data_bundle_path": "E:\PycharmProjects/rqalpha-1/.rqalpha/bundle",
      "start_date": "2020-01-15",
      "end_date": "2020-06-30",
      "benchmark": "000932.XSHG",
      "accounts": {
        "stock": 10000000000,
        "future": 0.1

      }
  },
  "extra": {
      "log_level": "verbose",
  },
  "mod": {
      "sys_analyser": {
        "enabled": True,
        "plot": True
      },
      "sys_simulation": {
          "enabled": True,
          "signal": True
      },
      "sys_risk": {
          "enabled": True,
          # 关闭仓位是否充足相关的风控判断
          "validate_is_trading": False
      },
      "vwap_backtest": {
        "enabled": False
      }
  }
}

# strategy_file_path = "./buy_and_hold.py"
strategy_file_path = "strategies/order_execution_stock.py"

run_file(strategy_file_path, config)
