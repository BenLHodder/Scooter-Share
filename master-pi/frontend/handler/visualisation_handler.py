import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class VisualisationHandler:
    def __init__(self):
        self.folder = "frontend/static/"
        
    def generate_visualisation(self, time_period, bookings):
        df = self.__process_bookings(bookings)
        
        if time_period == 'day':
            self.__plot_usage(df, time_period, self.folder + 'day.png')
        else:
            self.__plot_usage(df, time_period, self.folder + 'week.png')

    def __process_bookings(self, bookings):
        data = []
        for booking in bookings:
            date_format = "%a, %d %b %Y %H:%M:%S %Z"
            actual_start = datetime.strptime(booking['actual_start_datetime'], date_format)
            actual_end = datetime.strptime(booking['actual_end_datetime'], date_format)
            duration = (actual_end - actual_start).total_seconds() / 60 
            data.append({
                'scooter_id': booking['scooter_id'],
                'date': actual_start.date(),
                'week': actual_start.isocalendar()[1],
                'duration': duration
            })
        return pd.DataFrame(data)
    
    def __plot_usage(self, df, time_period, output_file):
        if time_period == 'day':
            df_grouped = df.groupby(['scooter_id', 'date'])['duration'].sum().reset_index()
            title = 'Daily Scooter Usage (Minutes) per Scooter'
            xlabel = 'Date'
        elif time_period == 'week':
            df_grouped = df.groupby(['scooter_id', 'week'])['duration'].sum().reset_index()
            title = 'Weekly Scooter Usage (Minutes) per Scooter'
            xlabel = 'Week Number'
        else:
            return

        # Plotting
        plt.figure(figsize=(10, 6))
        scooters = df_grouped['scooter_id'].unique()  # Get unique scooters

        for scooter in scooters:
            scooter_data = df_grouped[df_grouped['scooter_id'] == scooter]
            plt.plot(scooter_data.iloc[:, 1], scooter_data['duration'], label=f'Scooter {scooter}', marker='o')

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel('Usage Duration (Minutes)')
        plt.legend(title='Scooter ID')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the figure
        plt.savefig(output_file)

        # Clear the figure after saving
        plt.clf()
