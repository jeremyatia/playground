from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
from github import Github, GithubException
from time import sleep
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()


class UploadIDstoRepo:
    def __init__(self, channel_id: str, last_x_hours: int = 12,
                  episode_filename='episode.json', episode_history_filename='episode_history.json'):
        self.channel_id = channel_id
        self.last_x_hours = last_x_hours
        self.episode_filename = episode_filename
        self.episode_history_filename = episode_history_filename
        self._sanity_checks()

    def _sanity_checks(self):
        if os.environ.get('GOOGLE_API_KEY') is not None:
            self.google_api_key = os.environ['GOOGLE_API_KEY']
            print('GOOGLE_API_KEY is successfully set.')
        else:
            raise MissingEnvironmentVariable("GOOGLE_API_KEY does not exist")
        
        if os.environ.get('TORAH_PODCAST_GITHUB_TOKEN') is not None:
            self.github_token = os.environ['TORAH_PODCAST_GITHUB_TOKEN']
            print('TORAH_PODCAST_GITHUB_TOKEN is successfully set.')
        else:
            raise MissingEnvironmentVariable("TORAH_PODCAST_GITHUB_TOKEN does not exist")
        
    def _check_if_file_exists(self, repo, filename):
        try:
            repo.get_contents(filename)
        except GithubException:
            return False
        return True

    def _create_file(self, repo, filename):
        repo.create_file(filename, f"create {filename} file", "[]", branch="main")
        
    def _get_latest_video_ids_from_youtube_channel(self) -> list:
        # Build the YouTube Data API client
        youtube = build('youtube', 'v3', developerKey=self.google_api_key)

        # Calculate the start and end dates for the query
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=self.last_x_hours)

        # Format the dates for the API query
        start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Call the API to fetch the videos uploaded in the last 12 hours
        response = youtube.search().list(
            part="id",
            channelId=self.channel_id,
            type="video",
            publishedAfter=start_date_str,
            publishedBefore=end_date_str,
            maxResults=50  # Maximum number of results to fetch (adjust as needed)
        ).execute()

        # Extract video IDs from the response
        return [item['id']['videoId'] for item in response['items']]
    
    def _check_if_already_uploaded(self, repo, id):
        content_str = repo.get_contents(self.episode_history_filename).decoded_content
        content_list = eval(content_str)
        return True if id in content_list else False

    def execute(self, sleep_between_uploads_in_minutes:int=3):
        g = Github(self.github_token)
        repo = g.get_repo("thetorahpodcast/youtube-to-anchorfm")
        ids_to_upload = self._get_latest_video_ids_from_youtube_channel()
        print(f'These ids are fetched\n {ids_to_upload}')
        if not self._check_if_file_exists(repo, filename=self.episode_filename):
            print(f'The file {self.episode_filename} does not exist.')
            print(f'Creating it...')
            self._create_file(repo, self.episode_filename)
            print(f'{self.episode_filename} created.')
            self._create_file(repo, self.episode_history_filename)
            print(f'{self.episode_history_filename} created.')
        for id in tqdm(ids_to_upload):
            if self._check_if_already_uploaded(repo, id):
                print(f"\n{id} is already uploaded according to the {self.episode_history_filename}")
                continue
            else:
                # update id to episode file
                content_episode = repo.get_contents(self.episode_filename, ref="main")
                repo.update_file(path=content_episode.path, message=f"upload {id} in {self.episode_filename}", content='{"id": "' + id + '"}',
                                  sha=content_episode.sha, branch="main")
                print(f'{id} updated')
                # append id to history file
                content_history = repo.get_contents(self.episode_history_filename, ref="main")
                ch_decoded_content = eval(content_history.decoded_content)
                ch_decoded_content.append(id)
                repo.update_file(path=content_history.path, message=f"upload {id} in {self.episode_history_filename}", content=str(ch_decoded_content),
                                  sha=content_history.sha, branch="main")
                print(f'\nWill upload the next id in {sleep_between_uploads_in_minutes} minutes.')
                sleep(sleep_between_uploads_in_minutes*60)


class MissingEnvironmentVariable(Exception):
    pass


def main():
    # The YouTube channel ID you want to fetch videos from
    CHANNEL_ID = "UCpWaR3gNAQGsX48cIlQC0qw"
    upload_ids = UploadIDstoRepo(CHANNEL_ID)
    upload_ids.execute()


if __name__ == "__main__":
    main()