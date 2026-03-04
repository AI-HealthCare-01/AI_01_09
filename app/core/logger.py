import logging
import sys


def setup_logger(
    name: str = "ai_worker",
    level: int = logging.INFO,
) -> logging.Logger:
    """
    애플리케이션 전역에서 사용할 표준 로거를 설정하고 반환합니다.
    표준 출력(sys.stdout)을 통해 로그를 기록하며, 중복 핸들러 생성을 방지합니다.

    Args:
        name (str): 로거 이름
        level (int): 로깅 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    _logger = logging.getLogger(name)

    # 중복 핸들러 방지 (중요)
    if _logger.handlers:
        return _logger

    _logger.setLevel(level)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")

    # 콘솔 출력
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    _logger.addHandler(console_handler)
    _logger.propagate = False  # root logger로 중복 전달 방지

    return _logger


# 앱 전역에서 사용할 기본 로거 인스턴스
default_logger = setup_logger()
