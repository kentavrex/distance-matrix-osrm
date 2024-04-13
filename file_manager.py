import pandas as pd


class Joiner:
    @staticmethod
    def process():
        file_names = [f'collected_data/part_{part}.csv' for part in range(1, 11)]
        combined_data = pd.DataFrame()
        for file in file_names:
            df = pd.read_csv(file)
            combined_data = pd.concat([combined_data, df])
        combined_data.to_csv('time_data.csv', index=False)

        print("Объединенный файл сохранен как 'time_data.csv'")


class Splitter:
    @staticmethod
    def process():
        SPLIT_PARTS = 10
        df = pd.read_csv('/datasets/distance.csv')
        total_rows = len(df)
        rows_per_part = total_rows // SPLIT_PARTS
        parts = [df.iloc[i * rows_per_part:(i + 1) * rows_per_part] for i in range(SPLIT_PARTS)]
        for i, part in enumerate(parts):
            part.to_csv(f'part_{i + 1}.csv', index=False)


class TwoTableSplitter:
    @staticmethod
    def process():
        data1 = pd.read_csv('datasets/distance.csv')
        data2 = pd.read_csv('datasets/time_data.csv')

        output1 = pd.merge(data1, data2,
                           on='id',
                           how='inner')
        output1.to_csv('datasets/result_dataset.csv', index=False)


TwoTableSplitter().process()
