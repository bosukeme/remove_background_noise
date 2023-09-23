from background_noise_removal import config as conf


accesslog = '-'

bind = '{}:{}'.format(conf.HOST, conf.PORT)
workers = 6
threads = 2
