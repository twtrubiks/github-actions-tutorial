# Self-Hosted GitHub Actions Runner 教學

這邊教大家怎麼用自己建立的機器 (Runner) 跑 GitHub Actions,

之前的範例都是用 github 提供的 Runner (但通常這個有一些限制, 像是超過要付費之類的),

首先, 先建立一個 repo, 然後準備一台機器(用本機或是線上的機器都可以),

![alt tag](https://i.imgur.com/sXuhJRY.png)

註冊建立 Runner

(簡單說就是我們建立的機器會主動和 github 連線, 當它問 github 發現有任務要執行的時候, 就會執行任務),

到這邊選則對應的機器, 無腦複製貼上(基本上都 enter 即可), 這邊會有你的 repo 的 token,

![alt tag](https://i.imgur.com/xivQyYO.png)

最後貼上 `./run.sh` 就可以順利建立 Runner 了

![alt tag](https://i.imgur.com/cjW34RH.png)

建立一個簡單的 [workflows/blank.yml](https://github.com/twtrubiks/github-actions-tutorial/blob/main/self-hosted-gitHub-actions-runner/.github/workflows/blank.yml), 記得要改成 `self-hosted`

```yml
# This is a basic workflow to help you get started with Actions

name: CI

# Controls when the action will run.
on:
  # Triggers the workflow on push or pull request events but only for the master branch
  # push:
  #   branches: [ master ]
  # pull_request:
  #   branches: [ master ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: self-hosted

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v4

      # Runs a single command using the runners shell
      - name: Run a one-line script
        run: echo Hello, world!

      # Runs a set of commands using the runners shell
      - name: Run a multi-line script
        run: |
          echo Add other actions to build,
          echo test, and deploy your project.
          date

      #- name: Run docker ps
      #  run: docker ps

      #- name: Run docker nginx
      #  run: docker run --name nginx_test -d nginx:1.27.1

```

然後回到 github action 上, 去跑跑看, 你會發現指定的 Runner 有反應了,

你也可以去看你自己建立的 Runner, 會有 log 的

![alt tag](https://i.imgur.com/VlTVWdt.png)

如果你的 Runner 中斷, 然後你重新執行指令可能會出現以下的錯誤

```text
Cannot configure the runner because it is already configured. To reconfigure the runner, run 'config.cmd remove' or './config.sh remove' first
```

請執行 `./config.sh remove` 然後填入你的 repo 的 token 即可.

# Docker Github Actions Runner

接著來介紹一個 Docker 建立 Github Actions Runner 的版本

docker in docker 的概念.

[Docker Github Actions Runner](https://github.com/myoung34/docker-github-actions-runner)

安裝建立的流程可參考 [Usage](https://github.com/myoung34/docker-github-actions-runner/wiki/Usage)

準備一台機器(用本機或是線上的機器都可以),

## 事前準備

設定 Token

![alt tag](https://i.imgur.com/5Sdgo4h.png)

github 必須開權限

![alt tag](https://i.imgur.com/pEQTmBQ.png)

```text
repo (all)
admin:org (all) (mandatory for organization-wide runner)
admin:enterprise (all) (mandatory for enterprise-wide runner)
admin:public_key - read:public_key
admin:repo_hook - read:repo_hook
admin:org_hook
notifications
workflow
```

複製你的 Token.

有很多的安裝方法, 這邊介紹幾個給大家

## Systemd

如果不懂 Systemd, 可參考 [systemctl教學](https://github.com/twtrubiks/linux-note/tree/master/systemctl-tutorial)

建立一個 `ephemeral-github-actions-runner.service`

```service
[Unit]
Description=Ephemeral GitHub Actions Runner Container
After=docker.service
Requires=docker.service
[Service]
TimeoutStartSec=0
Restart=always
ExecStartPre=-/usr/bin/docker stop %N
ExecStartPre=-/usr/bin/docker rm %N
ExecStartPre=-/usr/bin/docker pull myoung34/github-runner:latest
ExecStart=/usr/bin/docker run --rm \
                              --env-file /etc/ephemeral-github-actions-runner.env \
                              -e RUNNER_NAME=%H \
                              -v /var/run/docker.sock:/var/run/docker.sock \
                              --name %N \
                              myoung34/github-runner:latest
[Install]
WantedBy=multi-user.target
```

然後建立需要的環境變數 `ephemeral-github-actions-runner.env`

```env
# Install with:
#   sudo install -m 600 ephemeral-github-actions-runner.env /etc/
RUNNER_SCOPE=repo
REPO_URL=https://github.com/your-org/your-repo
# Alternate for org scope:
#RUNNER_SCOPE=org
#ORG_NAME=your-org
LABELS=any-custom-labels-go-here
ACCESS_TOKEN=foo-access-token
RUNNER_WORKDIR=/tmp/runner/work
DISABLE_AUTO_UPDATE=1
EPHEMERAL=1
```

ACCESS_TOKEN 就是貼上前面取得的 Token

最後執行以下的指令

```cmd
# Install with:
#   sudo install -m 644 ephemeral-github-actions-runner.service /etc/systemd/system/
#   sudo systemctl daemon-reload
#   sudo systemctl enable ephemeral-github-actions-runner
# Run with:
#   sudo systemctl start ephemeral-github-actions-runner
# Stop with:
#   sudo systemctl stop ephemeral-github-actions-runner
# See live logs with:
#   journalctl -f -u ephemeral-github-actions-runner.service --no-hostname --no-tail
```

查看 log 確認是否正確執行.

## docker compose 版本

這個應該是最快的, 直接 `docker compose up -d` 收工.

![alt tag](https://i.imgur.com/u3pctlC.png)

[docker-compose.yml](docker-compose.yml)

```yml
services:
  worker:
    image: myoung34/github-runner:latest
    restart: always
    environment:
      REPO_URL: https://github.com/xxxxxx
      RUNNER_NAME: example-name
      RUNNER_WORKDIR: /tmp/runner/work
      # RUNNER_GROUP: my-group
      RUNNER_SCOPE: 'repo'
      # RUNNER_TOKEN: someGithubTokenHere # This token is short lived
      ACCESS_TOKEN: Token
      LABELS: linux,x64,gpu
      DISABLE_AUTO_UPDATE: 1
      EPHEMERAL: 1
    security_opt:
      # needed on SELinux systems to allow docker container to manage other docker containers
      - label:disable
    volumes:
      - '/var/run/docker.sock:/var/run/docker.sock'
      - '/tmp/runner:/tmp/runner'
      # note: a quirk of docker-in-docker is that this path
      # needs to be the same path on host and inside the container,
      # docker mgmt cmds run outside of docker but expect the paths from within
```

這是 docker-in-docker 的概念, 也就是說你在本機執行的 `docker ps`

和在 docker(runner) 裡面執行 `docker ps` 看到的東西會是一樣的,

也就是相通, 超酷 😀

可以直接在 workflow 裡面加一個啟動 docker 的指令觀察看看.

另外建議大家 google 一下 `/var/run/docker.sock` 在 docker 中是什麼意義.