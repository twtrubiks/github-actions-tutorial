# 透過 github action 遠端 ssh server

ssh-action-tutorial (注意 .github 資料夾)

這篇文章是使用 PRIVATE_KEY 的方式, 還有其他方式可參考 [ssh-action](https://github.com/appleboy/ssh-action)

使用方法,

先在遠端 目標server(你要 ssh 的server) 執行以下的指令

```cmd
ssh-keygen -t rsa -b 4096 -C "github-actions"
```

接著 在遠端 目標server(你要 ssh 的server) 執行以下的指令

```cmd
cat ~/.ssh/id_rsa_github_actions.pub >> ~/.ssh/authorized_keys
```

之後設定 yaml 即可, 可參考 [workflows/demo.yml](https://github.com/twtrubiks/github-actions-tutorial/blob/main/ssh-server-github-action/.github/workflows/demo.yml)

需要設定幾個參數,

SSH_HOST 目標server(你要 ssh 的server) ip

SSH_USER 目標server(你要 ssh 的server) 使用者

SSH_PRIVATE_KEY 貼上我們建立出來的 PRIVATE_KEY `~/.ssh/id_rsa_github_actions`

SSH_PORT 目標server(你要 ssh 的server) port

![alt tag](https://i.imgur.com/wapDARQ.png)

之後就可以簡單測試一下  :blush:  :blush:

這邊說明一下 ssh 的流程,

| 流程說明           |                |         |
|----------------|----------------|---------|
|                | 正常             | 遠端      |
| 一般 ssh         | 留下私人的key       |  放 .pub |
| github action | 環境變數貼上 PRIVATE_KEY |  放 .pub |

仔細思考, 其實就是流程反過來而已, 因為我們沒辦法進去 github action 那台機器設定,

所以變成我們自己先設定好 ssh key, 再將 private key 貼到 github action 中的環境變數,

只要把想法想成我們的本機現在是 github action 那台機器就會比較了解了 :smiley:
