from logging import basicConfig, INFO, getLogger

basicConfig(
    level=INFO,
    format="[{asctime}] [{levelname:<8}] {name}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{"
)