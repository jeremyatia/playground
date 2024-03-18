import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from the_torah_podcast.upload_ids_to_repo import UploadIDstoRepo
from the_torah_podcast import path_to_file
import pandas as pd


def main():
    subscribers = pd.read_csv(os.path.join(path_to_file, 'subscribers.csv'))
    for i in range(subscribers.shape[0]):
        channel_id, frequency_to_check, episode_name = subscribers.iloc[i]
        upload_process = UploadIDstoRepo(channel_id=channel_id, last_x_hours=int(frequency_to_check),
                                         episode_filename=f'episode_{episode_name}.json',
                                         episode_history_filename=f'episode_history_{episode_name}.json')
        upload_process.execute()


if __name__ == "__main__":
    main()
