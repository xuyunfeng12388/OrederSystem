# coding:utf-8

class RET:
    OK = "0"
    TRADE_SUCCESS = "1001"
    WAIT_BUYER_PAY = "1002"
    TRADE_CLOSED = "1003"
    ORDERSEXIST = "1004"
    ORDERFINISHED = "1005"
    SOMEONE = "1006"

    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    DATAERR = "4004"

    INVALIDSIGNATURE = "4005"
    EXPIREDSIGNATURE = "4006"
    ORDERQUERYERROE = "4007"

    PARAMERR = "4103"

    REQERR = "4201"
    IPERR = "4202"
    NONMEMBER = "4203"
    NONPAYMENT = "4204"
    EXPIRMEMBER = "4205"
    ORDERSERRORS = "4206"
    GOODSERRORS = "4207"
    TRADE_NOT_EXIST = "4208"


    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"


error_map = {
    RET.OK: "成功",

    RET.SOMEONE: "有人使用餐桌",

    RET.TRADE_SUCCESS: "支付完成",
    RET.WAIT_BUYER_PAY: "待支付",
    RET.TRADE_CLOSED: "交易关闭",
    RET.ORDERSEXIST: "订单已经存在，请完成支付",
    RET.ORDERFINISHED: "订单已经完成支付，请勿重复购买",

    RET.DBERR: "数据库查询错误",
    RET.NODATA: "无数据",
    RET.DATAEXIST: "数据已存在",
    RET.DATAERR: "数据错误",

    RET.INVALIDSIGNATURE: "token无效",
    RET.EXPIREDSIGNATURE: "token过期",

    RET.PARAMERR: "参数错误",
    RET.REQERR: "非法请求或请求次数受限",

    RET.NONMEMBER: "非会员用户",
    RET.NONPAYMENT: "付费应用",
    RET.EXPIRMEMBER: "会员过期",
    RET.ORDERSERRORS: "订单错误",
    RET.GOODSERRORS: "商品错误",
    RET.TRADE_NOT_EXIST: "交易不存在或者用户还未进行支付",
    RET.ORDERQUERYERROE: "订单查询异常",





    RET.IPERR: "IP受限",
    RET.THIRDERR: "第三方系统错误",
    RET.IOERR: "文件读写错误",
    RET.SERVERERR: "内部错误",
    RET.UNKOWNERR: "未知错误",
}
