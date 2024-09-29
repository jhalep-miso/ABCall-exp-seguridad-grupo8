import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import re

log_dir = 'logs'


# Funcion para parsear archivo de logs de simulacion de modificaciones
def parse_simulacion_modificaciones_log(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            timestamp_str, logType, action, factura_str, checksum_str = (
                line.strip().split(' - ')
            )
            if action != 'Actualización Factura' or logType != 'INFO':
                continue
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            factura_id = int(factura_str.split(' ')[-1])
            checksum = checksum_str.split(' ')[-1]
            data.append(
                {
                    'timestamp': timestamp,
                    'factura_id': factura_id,
                    'action': action,
                    'checksum': checksum,
                }
            )
    return pd.DataFrame(data)


# Funcion para parsear archivo de logs de monitor de integridad
def parse_monitor_integridad_log(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            if 'Factura update audit' not in line:
                continue
            (
                timestamp_str,
                _,
                factura_audit,
                factura_str,
                checksum_str,
                db_user_str,
                db_user_ip_str,
                execution_time_str,
            ) = line.strip().split(' - ')
            checksum = checksum_str.split(' ')[-1]
            factura_id = int(factura_str.split(' ')[-1])
            execution_time = execution_time_str.split(' ')[-1]
            timestamp = datetime.strptime(execution_time, '%Y-%m-%dT%H:%M:%S.%f')
            data.append(
                {
                    'timestamp': timestamp,
                    'factura_id': factura_id,
                    'checksum': checksum,
                }
            )
    return pd.DataFrame(data)


def get_most_recent_log_file(log_dir, pattern):
    log_files = [f for f in os.listdir(log_dir) if re.match(pattern, f)]
    if not log_files:
        raise FileNotFoundError("No log files found matching the pattern.")

    # Extract dates from filenames and sort them
    log_files.sort(
        key=lambda x: datetime.strptime(
            re.search(r'\d{8}_\d{6}', x).group(), '%Y%m%d_%H%M%S'
        ),
        reverse=True,
    )
    return os.path.join(log_dir, log_files[0])


def generar_grafico():
    monitor_integridad_log_pattern = r'integridad_monitor_\d{8}_\d{6}\.log'
    simulador_modificaciones_log_pattern = r'simulacion_modificaciones_\d{8}_\d{6}\.log'
    monitor_integridad_log_file = get_most_recent_log_file(
        log_dir, monitor_integridad_log_pattern
    )
    simulacion_modificaciones_log_file = get_most_recent_log_file(
        log_dir, simulador_modificaciones_log_pattern
    )

    # Parsear logs
    print(f'plotting monitor integridad file {monitor_integridad_log_file}')
    print(f'plotting simulated modifications file {simulacion_modificaciones_log_file}')
    simulaciones_df = parse_simulacion_modificaciones_log(
        simulacion_modificaciones_log_file
    )
    monitor_integridad_df = parse_monitor_integridad_log(monitor_integridad_log_file)

    facturas = simulaciones_df['factura_id'].unique()

    # Marcadores distintos para identificar actualizacion simulada con checksum correcto o incorrecto
    checksum_markers = {'False': ('x', 'red'), 'True': ('o', 'green')}

    fig, axes = plt.subplots(
        len(facturas), 1, figsize=(15, 5 * len(facturas)), sharex=True
    )

    # Gráfica por cada factura
    for i, factura in enumerate(facturas):
        ax = axes[i] if len(facturas) > 1 else axes
        simulacion_modificaciones_data = simulaciones_df[
            simulaciones_df['factura_id'] == factura
        ]
        monitor_integridad_data = monitor_integridad_df[
            monitor_integridad_df['factura_id'] == factura
        ]

        # Plot monitor de integridad de factura
        ax.plot(
            monitor_integridad_data['timestamp'],
            monitor_integridad_data['checksum'],
            label=f'factura {factura} Detección de integridad',
            color='blue',
        )

        # Plot simulacion de modificaciones de factura
        for checksum, marker in checksum_markers.items():
            checksum_data = simulacion_modificaciones_data[
                simulacion_modificaciones_data['checksum'] == checksum
            ]
            ax.scatter(
                checksum_data['timestamp'],
                checksum_data['checksum'],
                label=f'factura {factura} Modificación válida {checksum}',
                marker=marker[0],
                color=marker[1],
            )

        # Formatting the subplot
        ax.set_title(f'Factura: {factura}')
        ax.set_ylabel('Modificacion válida')
        ax.legend()

    # Formatting the plot
    plt.xlabel('Timestamp')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()
