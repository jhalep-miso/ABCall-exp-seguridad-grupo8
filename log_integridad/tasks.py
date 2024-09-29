from celery import Celery
import datetime
import logging
import pytz

TIME_ZONE = 'UTC'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

timezone = pytz.timezone(TIME_ZONE)

class CustomFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
        return dt

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s


formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')

# Crear un manejador de archivo para almacenar logs
log_filename = datetime.datetime.now(pytz.timezone(TIME_ZONE)).strftime(
    '/logs/integridad_monitor_%Y%m%d_%H%M%S.log'
)
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Crear un manejador de consola para mostrar logs en terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

celery_app = Celery(__name__, broker='redis://redis:6379/0')


celery_app.conf.update(worker_hijack_root_logger=False)

# Set Celery's logger to a higher log level to filter out its logs
celery_logger = logging.getLogger('celery')
celery_logger.setLevel(logging.CRITICAL + 1)


@celery_app.task(name='notify_integrity_check')
def notify_integrity_check(
    audit_id,
    factura_id,
    old_data,
    new_data,
    is_valid_checksum,
    db_user,
    db_user_ip,
    execution_time,
):

    execution_time_str = execution_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
    logger.info(
        f"Factura update audit {audit_id} - factura_id {factura_id} - is_valid_checksum {is_valid_checksum} - db_user {db_user} - db_user_ip {db_user_ip} - execution_time {execution_time_str}"
    )
