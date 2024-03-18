# The Torah Podcast

The goal of the torah podcast is to automatically publish your torah podcast from Youtube.

It uses the repo: https://github.com/Schrodinger-Hat/youtube-to-anchorfm

And has been forked to make changes easily: https://github.com/thetorahpodcast/youtube-to-anchorfm

The script `upload_ids_to_repo.py` makes sure to edit two files (by default): 
- episode.json - containing the video id that is being uploaded to your podcast platform (triggered with Github Action)
- episode_history.json - containing the video ids that are already uploaded

## Installation

```bash
pip install -r requirements.txt
```



## Usage

1) Define the two env variables in the file `.env.sample`
    - GOOGLE_API_KEY: to connect to the Youtube API
    - TORAH_PODCAST_GITHUB_TOKEN: to be able to modify the `thetorahpodcast` repo

2) rename `.env.sample` by `.env`

3) Edit the youtube `CHANNEL_ID` from which you want to get the latest videos ids (last 12 hours) and upload them

4) Then run the script
```shell
$ python upload_ids_to_repo.py
```

3) Outputs (example)
```shell
GOOGLE_API_KEY is successfully set.
TORAH_PODCAST_GITHUB_TOKEN is successfully set.

xBYDBXkT6P0 is already uploaded according to the episode_history.json

MifBfwrSgr4 is already uploaded according to the episode_history.json

YZ_BVtMyNzA is already uploaded according to the episode_history.json

IYbRu_TdBGE is already uploaded according to the episode_history.json
```



# AWS

To set up AWS

- install the aws cli 
- run `aws configure` 
- Fill AWS Access Key ID and secret Key
## License
Enjoy tsadik

