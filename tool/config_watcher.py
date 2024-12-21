import configparser


class TqAccountConfig:

    def __init__(self):
        self.user_name: str = ""
        self.password: str = ""
        self.real_open: bool = False
        self.tq_kq: bool = True
        self.tq_back_test: bool = False
        self.tq_account_broker_id: str = ""
        self.tq_account_account_id: str = ""
        self.tq_account_password: str = ""


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.read(verbose=False)

    def read(self, verbose=False, ):
        self.config.read('../config.ini', encoding='utf-8-sig')
        self.config.sections()
        # Account
        self.tq_auth = self.config['TQAUTH']
        self.tq_auth_user_name = str(self.tq_auth['user_name'])
        self.tq_auth_password = str(self.tq_auth['password'])

        # 实盘账户和密码
        self.tq_account = self.config['TQACCOUNT']
        self.tq_account_broker_id = str(self.tq_account['broker_id'])
        self.tq_account_account_id = str(self.tq_account['account_id'])
        self.tq_account_password = str(self.tq_account['password'])

        # 实盘
        self.real = self.config['REAL']
        # 是否开启实盘交易
        self.real_open = self.real.getboolean('open')
        self.tq_kq = self.real.getboolean('tq_kq')
        self.tq_back_test = self.real.getboolean('tq_back_test')

        self.url = self.config['URL']
        self.feishu_webhook_url = str(self.url['feishu_webhook_url'])
        self.dingding_webhook_url = str(self.url['dingding_webhook_url'])
        self.dingding_secret = str(self.url['dingding_secret'])

        self.smtp163 = self.config['SMTP163']
        self.email_163_host = str(self.smtp163['email_host'])
        self.email_163_user = str(self.smtp163['email_user'])
        self.email_163_pass = str(self.smtp163['email_pass'])
        self.sender_163 = str(self.smtp163['sender'])
        self.receivers_163 = str(self.smtp163['receivers'])

        self.smtp_qq = self.config['SMTPQQ']
        self.email_qq_host = str(self.smtp_qq['email_host'])
        self.email_qq_user = str(self.smtp_qq['email_user'])
        self.email_qq_pass = str(self.smtp_qq['email_pass'])
        self.receivers_qq = str(self.smtp_qq['receivers'])

        if verbose:
            print('Config reloaded')


cfg = Config()

# if __name__ == '__main__':
#     cfg = Config()
#     for key in cfg.config['TQAUTH']:
#         print(key, cfg.config['TQAUTH'][key])
