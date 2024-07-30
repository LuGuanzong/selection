class ResponseCode(object):
    Success = 0  # 成功
    Fail = -1  # 失败
    NoResourceFound = 40001  # 未找到资源
    InvalidParameter = 40002  # 参数无效
    AccountOrPassWordErr = 40003  # 账户或密码错误
    VerificationCodeError = 40004  # 验证码错误
    PleaseSignIn = 40005  # 请登陆


class ResponseMessage(object):
    Success = "成功"
    Fail = "失败"
    NoResourceFound = "未找到资源"
    InvalidParameter = "参数无效"
    AccountOrPassWordErr = "账户或密码错误"
    VerificationCodeError = "验证码错误"
    PleaseSignIn = "请登陆"


# 状态码与信息映射字典
code_to_message = {
    ResponseCode.Success: ResponseMessage.Success,
    ResponseCode.Fail: ResponseMessage.Fail,
    ResponseCode.NoResourceFound: ResponseMessage.NoResourceFound,
    ResponseCode.InvalidParameter: ResponseMessage.InvalidParameter,
    ResponseCode.AccountOrPassWordErr: ResponseMessage.AccountOrPassWordErr,
    ResponseCode.VerificationCodeError: ResponseMessage.VerificationCodeError,
    ResponseCode.PleaseSignIn: ResponseMessage.PleaseSignIn,
}


def get_message_by_code(code):
    """根据状态码获取对应的文本信息"""
    return code_to_message.get(code, "未知错误")
