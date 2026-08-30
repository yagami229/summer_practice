import matplotlib.pyplot as plt
import numpy as np
import re

def parse_markdown_table(filepath):
    #Читает таблицу и извлекает данные о времени и памяти для различных алгоритмов.

    # Чтение файла, удаление пустых строк
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Парсинг заголовка
    header = [cell.strip() for cell in lines[0].strip('|').split('|')]
    # Парсинг строк данных
    data_rows = [
        [cell.strip() for cell in line.strip('|').split('|')]
        for line in lines[1:]
    ]

    # Определение индексов столбцов
    col_index = {col: i for i, col in enumerate(header)}
    size_col = col_index['Size']
    type_col = col_index['Type']

    # Выделение столбцов алгоритмов (все, кроме Size и Type)
    alg_cols = [col for col in header if col not in ['Size', 'Type']]
    if not alg_cols:
        return {}, [], []

    # Определение формата данных: объединённый (время/память в одной ячейке) или раздельный
    sample = data_rows[0][col_index[alg_cols[0]]]
    if '/' in sample:
        combined = True          # формат "время/память"
        alg_names = alg_cols
    else:
        combined = False
        # Ищем столбцы, заканчивающиеся на " Time (s)" и " Mem (KB)"
        time_cols = {col: idx for col, idx in col_index.items() if col.endswith(' Time (s)')}
        mem_cols  = {col: idx for col, idx in col_index.items() if col.endswith(' Mem (KB)')}
        # Имена алгоритмов получаем удалением суффикса
        alg_names = [col.replace(' Time (s)', '') for col in time_cols]
        # Сопоставление алгоритма с индексами его времени и памяти
        time_indices = {alg: time_cols[f'{alg} Time (s)'] for alg in alg_names}
        mem_indices  = {alg: mem_cols[f'{alg} Mem (KB)'] for alg in alg_names}

    # Сбор данных в структуру
    data = {}
    sizes_set = set()
    for row in data_rows:
        size = int(row[size_col])
        dtype = row[type_col]
        sizes_set.add(size)

        if dtype not in data:
            data[dtype] = {}
        if size not in data[dtype]:
            data[dtype][size] = {}

        for alg in alg_names:
            if combined:
                combined_str = row[col_index[alg]]
                parts = combined_str.split('/')
                t_str = parts[0] if len(parts) > 0 else ''
                m_str = parts[1] if len(parts) > 1 else ''
            else:
                t_str = row[time_indices[alg]]
                m_str = row[mem_indices[alg]]
            # Преобразование в числа, при ошибке — NaN
            try:
                t_val = float(t_str)
                m_val = float(m_str)
                data[dtype][size][alg] = (t_val, m_val)
            except ValueError:
                data[dtype][size][alg] = (np.nan, np.nan)

    sizes = sorted(sizes_set)
    return data, alg_names, sizes


def plot_time_memory(data, alg_names, sizes, output_prefix='sorting_plots'):

    #Строит графики времени выполнения и пикового использования памяти для каждого типа данных.

    types = sorted(data.keys())
    n_types = len(types)

    # -------- Графики времени ----------
    fig_time, axes_time = plt.subplots(1, n_types, figsize=(5*n_types, 4), sharey=False)
    if n_types == 1:
        axes_time = [axes_time]

    for ax, dtype in zip(axes_time, types):
        for alg in alg_names:
            times = []
            valid_sizes = []
            for size in sizes:
                if alg in data[dtype][size]:
                    t = data[dtype][size][alg][0]
                    if not np.isnan(t):
                        times.append(t)
                        valid_sizes.append(size)
            if valid_sizes:
                ax.plot(valid_sizes, times, marker='o', label=alg)
        ax.set_title(dtype)
        ax.set_xlabel('Input Size')
        ax.set_ylabel('Time (s)')
        ax.set_xscale('log')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(fontsize=8)

    fig_time.tight_layout()
    fig_time.savefig(f'{output_prefix}_time.png', dpi=150)
    plt.close(fig_time)

    # -------- Графики памяти ----------
    fig_mem, axes_mem = plt.subplots(1, n_types, figsize=(5*n_types, 4), sharey=False)
    if n_types == 1:
        axes_mem = [axes_mem]

    for ax, dtype in zip(axes_mem, types):
        for alg in alg_names:
            mems = []
            valid_sizes = []
            for size in sizes:
                if alg in data[dtype][size]:
                    m = data[dtype][size][alg][1]
                    if not np.isnan(m):
                        mems.append(m)
                        valid_sizes.append(size)
            if valid_sizes:
                ax.plot(valid_sizes, mems, marker='s', label=alg)
        ax.set_title(dtype)
        ax.set_xlabel('Input Size')
        ax.set_ylabel('Peak Memory (KB)')
        ax.set_xscale('log')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(fontsize=8)

    fig_mem.tight_layout()
    fig_mem.savefig(f'{output_prefix}_memory.png', dpi=150)
    plt.close(fig_mem)

    print(f"Plots saved as {output_prefix}_time.png and {output_prefix}_memory.png")


def main():
    #Основная функция: парсит results.md, выводит информацию и строит графики.

    # Парсинг таблицы из файла
    data, alg_names, sizes = parse_markdown_table('results.md')
    print(f"Found {len(alg_names)} algorithms: {', '.join(alg_names)}")
    print(f"Sizes: {sizes}")
    print(f"Data types: {list(data.keys())}")

    # Генерация графиков
    plot_time_memory(data, alg_names, sizes)


if __name__ == '__main__':
    main()
