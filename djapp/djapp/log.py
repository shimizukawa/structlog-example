import logging
import structlog

from django.conf import settings


def dict_config(logging_settings):
    """structlogの初期化を行う。

    djapp.settings.LOGGING_CONFIG 設定によって呼び出される関数。
    `LOGGING_CONFIG = "djapp.log.dict_config"`
    """
    shared_processors = [
        # コンテキスト情報をログ出力にマージする
        structlog.contextvars.merge_contextvars,
        # ログレベルを出力
        structlog.stdlib.add_log_level,
        # ロガー名を出力
        structlog.stdlib.add_logger_name,
        # 時刻をisoフォーマットで出力
        structlog.processors.TimeStamper(fmt="iso"),
        # info("some %s", value) 形式の位置引数をフォーマット
        structlog.stdlib.PositionalArgumentsFormatter(),
        # bytes型データをstrに変換
        structlog.processors.UnicodeDecoder(),
        # ログ出力の実行位置を出力
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
        # Eventにstack_info=Trueがあれば、スタック情報を入れるEventのstackに入れる
        structlog.processors.StackInfoRenderer(),
        # Eventにexc_info=Trueがあれば、例外をフォーマットしてEventのexceptionに入れる
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=[
            # 標準loggerのレベル設定によるフィルタを最初に行う、標準のloggingでは不要。
            # structlog側で固定してよければ、 wrapper_class=structlog.make_filtering_bound_logger(logging.INFO) 等に置き換えられる。
            structlog.stdlib.filter_by_level,
        ]
        + shared_processors
        + [
            # 最後に、ログ出力は標準ライブラリのLOGGING設定に任せるため、データ構造を調整する
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        # 標準ライブラリのloggingと同じAPIのインスタンスを使う
        wrapper_class=structlog.stdlib.BoundLogger,
        # 標準ライブラリのlogging.Loggerを最終的な出力に使う
        logger_factory=structlog.stdlib.LoggerFactory(),
        # ログ出力時に遅延作成されるloggerインスタンスを再利用する
        cache_logger_on_first_use=True,
    )

    if settings.DEBUG:
        # ローカル開発中は人間が見やすい表示で出力
        renderer = structlog.dev.ConsoleRenderer()
    else:
        # 運用ではJSONで出力
        renderer = structlog.processors.JSONRenderer()
    logging_settings["formatters"]["structlog"] = {
        "()": structlog.stdlib.ProcessorFormatter,
        "processors": [
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        "foreign_pre_chain": shared_processors,
    }
    logging.config.dictConfig(logging_settings)
    structlog.get_logger().debug("こんにちは structlog!")
