from upload_ids_to_repo import UploadIDstoRepo
import pandas as pd
from config import link_github_subscribers


def run():
    subscribers = pd.read_csv(link_github_subscribers)
    for i in range(subscribers.shape[0]):
        channel_id, frequency_to_check, episode_name = subscribers.iloc[i]
        frequency_to_check = 1800
        upload_process = UploadIDstoRepo(channel_id=channel_id, last_x_hours=int(frequency_to_check),
                                         episode_filename=f'episode_{episode_name}.json',
                                         episode_history_filename=f'episode_history_{episode_name}.json')
        print(f'Running for {episode_name}')
        upload_process.execute()


if __name__ == "__main__":
    run()
