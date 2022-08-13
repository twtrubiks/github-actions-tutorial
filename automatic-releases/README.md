# github actions 搭配 automatic-releases 教學

* [Youtube Tutorial - github actions 搭配 automatic-releases 教學](https://youtu.be/pCnGcLj_3Lg)

官方文件可參考 [https://github.com/marketplace/actions/automatic-releases](https://github.com/marketplace/actions/automatic-releases)

底下主要有兩個分別是 [pre-release.yml](https://github.com/twtrubiks/github-actions-tutorial/blob/main/automatic-releases/.github/workflows/pre-release.yml) 和 [tagged-release.yml](https://github.com/twtrubiks/github-actions-tutorial/blob/main/automatic-releases/.github/workflows/tagged-release.yml),

[pre-release.yml](https://github.com/twtrubiks/github-actions-tutorial/blob/main/automatic-releases/.github/workflows/pre-release.yml)

當你 push main(master) 分支時, 會自動幫你產生一個 pre-release 的頁面

![alt tag](https://i.imgur.com/VHx9jze.png)

[tagged-release.yml](https://github.com/twtrubiks/github-actions-tutorial/blob/main/automatic-releases/.github/workflows/tagged-release.yml)

當你下 push tag 時,

```cmd
❯ git tag v1.0.1
❯ git push origin v1.0.1
```

會自動幫你產生一個 release 頁面,

非常建議搭配 [規格化 commit](https://github.com/twtrubiks/python-notes/tree/master/commitizen_pre_commit_tutorial) 一起始用,

因為這樣就會自動幫你整理成漂亮的格式

![alt tag](https://i.imgur.com/smiHnlG.png)
