aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 992382515700.dkr.ecr.eu-north-1.amazonaws.com
docker build -t torahpodcast-docker .
docker tag torahpodcast-docker:latest 992382515700.dkr.ecr.eu-north-1.amazonaws.com/torahpodcast-docker:latest
docker push 992382515700.dkr.ecr.eu-north-1.amazonaws.com/torahpodcast-docker:latest
