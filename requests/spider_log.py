import logging

from logging import StreamHandler
from logging import Formatter, FileHandler


def new_logger(name):
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 创建日志的处理器
    handler = StreamHandler()
    handler.setLevel(logging.INFO)

    # 创建日志格式化对象
    formatter = Formatter(fmt='[ %(asctime)s of %(name)s - %(levelname)s] %(message)s',
                          datefmt='%Y-%m-%d %H:%M:%S')

    # 设置处理器的日志格式化
    handler.setFormatter(formatter)

    # 添加记录器的处理器
    logger.addHandler(handler)

    file_handler = FileHandler('access.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(Formatter('<%(asctime)s at %(lineno)s of %(name)s - %(levelname)s] %(message)s',
                                        '%Y-%m-%d %H:%M:%S'))
    logger.addHandler(file_handler)
    return logger


if __name__ == '__main__':
    logger = new_logger('spider')
    logger.info('test1')
    logger.error('test2')
