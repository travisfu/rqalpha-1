# Created by qinxuan at 2019/5/6
from rqalpha.api import *
import pandas as pd
import os.path


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    # 是否已发送了order
    context.fired = False
    # future_strategy = 0
    # if future_strategy == 1:
    #     file_path = os.path.abspath(os.path.dirname(__file__))
    #     context.multiplier = pd.read_excel(file_path + "\examples\data_source\multiplier.xlsx", index_col=0)
    #     for ticker in context.multiplier.index:
    #        print (ticker, context.multiplier.loc[ticker, 'multiplier'])




def before_trading(context):
    # 初始化当天的交易标志
    context.traded_today = False
    pass


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 日频交易，如果当天已经交易过了，则跳出
    print(context.portfolio.stock_account.total_value)
    # print(context.portfolio.future_account.total_value)
    print(context.now.strftime("%H%M"))


    if context.traded_today is True:
        return

    file_path = "E:\PycharmProjects\\rqalpha_trade\\" + context.now.strftime('%Y%m%d') + ".xlsx"
    # file_path = os.path.abspath('../../rqalpha_trade\\') + context.now.strftime('%Y%m%d') + ".xlsx"
    print(file_path)
    try:
        portfolio_stock = pd.read_excel(file_path, 'equity', index_col=0)
        # portfolio_future = pd.read_excel(file_path, 'future', index_col=0)
    except FileNotFoundError:
        return

    # 交易股票
    # 将待交易的投资组合用逆序排序
    portfolio_stock.sort_values('weight', inplace=True, ascending=False)
    # 先卖出在现有组合且不在未来组合中的股票
    set_sell = set(context.portfolio.stock_account.positions.keys()) - set(portfolio_stock.index)
    for stock_sell in set_sell:
        order_target_percent(stock_sell, 0)

    # 买入投资组合中的对应权益资产,权重大的先买入
    if sum(portfolio_stock['weight']) > 1:
        logger.info("所有权重相加大于1")

    # 需要执行先卖后买的操作
    stock_positions = context.portfolio.stock_account.positions
    # 权重减少的股票，等同于卖
    stock_reduce = set()
    for stock_adjust in portfolio_stock.index:
        if portfolio_stock.loc[stock_adjust, 'weight'] < stock_positions[stock_adjust].value_percent:
            stock_reduce.add(stock_adjust)
    stock_increase = set(portfolio_stock.index) - stock_reduce

    print(stock_reduce, stock_increase, "tttttt")

    # 执行先卖后买的方法
    for ticker in stock_reduce:
        order_target_percent(ticker, portfolio_stock.loc[ticker, 'weight'])

    for ticker in stock_increase:
        order_target_percent(ticker, portfolio_stock.loc[ticker, 'weight'])

    print(context.portfolio.stock_account.positions.keys(),"actual position")

    # # 交易期货
    # for future_order in portfolio_future.index:
    #     # 先进行所有期货仓位的平仓  此处存储的代码是否一致！！！
    #     set_close = set(context.portfolio.future_account.positions.keys()) - set(portfolio_future.index)
    #     multiplier = context.multiplier
    #
    #     # print("~~~~~~~~~~~~~~~")
    #     # print(context.portfolio.future_account.positions.keys())
    #     # print(set(portfolio_future.index))
    #     # print(context.portfolio.future_account.total_value)
    #     # for future_ticker in portfolio_future.index:
    #     #     print(future_ticker, multiplier.loc[future_ticker,  'multiplier'])
    #     #     print (history_bars(future_ticker, 1, '1d', 'close'))
    #     #     print ("YES")
    #     # print("!!!!!!!!!!!!!!!!!!")
    #
    #     future_positions = context.portfolio.future_account.positions
    #     for future_close in set_close:
    #         if future_positions[future_close].closable_sell_quantity > 0:
    #             buy_close(future_close, future_positions[future_close].closable_sell_quantity)
    #         if future_positions[future_close].closable_buy_quantity > 0:
    #             sell_close(future_close, future_positions[future_close].closable_buy_quantity)
    #
    #     # 目标手数
    #     # print(future_order, context.portfolio.future_account.total_value,portfolio_future.loc[future_order, 'weight'], history_bars(future_order, 1, '1d', 'close')[0],\
    #     #       multiplier.loc[future_order,  'multiplier'],round(context.portfolio.future_account.total_value*\
    #     #       portfolio_future.loc[future_order, 'weight'] \
    #     #                 /history_bars(future_order, 1, '1d', 'close')[0] / multiplier.loc[future_order,  'multiplier']))
    #     target_amount = round(context.portfolio.future_account.total_value*portfolio_future.loc[future_order, 'weight'] \
    #                     /history_bars(future_order, 1, '1d', 'close')[0] / multiplier.loc[future_order,  'multiplier'])
    #
    #     # 净持仓量
    #     net_current_amount = future_positions[future_order].buy_quantity - \
    #         future_positions[future_order].sell_quantity
    #     # 净交易量
    #     net_exe_amount = target_amount - net_current_amount
    #
    #
    #     # 目标手数减当前手数为正，做多单，先平后开
    #     if net_exe_amount > 0:
    #         if future_positions[future_order].sell_quantity > 0:
    #             if net_exe_amount <= future_positions[future_order].sell_quantity:
    #                 buy_close(future_order, net_exe_amount)
    #             else:
    #                 buy_close(future_order, future_positions[future_order].sell_quantity)
    #                 buy_open(future_order, net_exe_amount - future_positions[future_order].sell_quantity)
    #         else:
    #             buy_open(future_order, net_exe_amount)
    #
    #     # 目标手数减当前当前手数为负，做空单，先平后买
    #     if net_exe_amount < 0:
    #         if future_positions[future_order].buy_quantity > 0:
    #             if abs(net_exe_amount) <= future_positions[future_order].buy_quantity:
    #                 sell_close(future_order, abs(net_exe_amount))
    #             else:
    #                 sell_close(future_order, future_positions[future_order].buy_quantity)
    #                 sell_open(future_order, abs(net_exe_amount) - future_positions[future_order].buy_quantity)
    #         else:
    #             sell_open(future_order, abs(net_exe_amount))

    context.traded_today = True


