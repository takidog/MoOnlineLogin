# MoOnlineLogin

一款16年的古董遊戲改成網頁登入，有夠麻煩

不就登入器是有多麻煩:I



下載打包好的請到[Releases](https://github.com/takidog/MoOnlineLogin/releases>)



## 使用方式

目前只有開發console版本，並沒有GUI介面

未來不確定，有興趣可以自己fork在PR過來哦



**Windows10 目前僅支援直接啟動mystina.exe**  

**Windows7 目前僅支援直接啟動Login.exe** 

### 設定config.json

請在同資料夾放一個`config.json` 內容如下

```json
{
    "gamePath": "C:/Lager/moonline/mystina.exe",
    "loginPath": "C:/Lager/moonline/login.exe",
    "saveCaptcha": true,
    "accountPath": "account.json"
}
```

**注意**這裡的路徑請用`/` 不要使用`\`  並且替換為你的遊戲路徑

`saveCaptcha` `accountPath`目前暫無功能

### 一般交互模式登入

#### Windows10

直接點開`simple_mode.exe` 根據指示輸入遊戲帳號及密碼，並會彈出圖形驗證碼



#### Windows7

請在`simple_mode.exe`的資料夾下寫一個`bat`  example: `win7.bat`

```bash
simple_mode.exe -mode login
```



或是在同資料夾下開啟cmd or powershell去操作

### 多組帳號登入

`simple_mode.exe`  

**注意** 在Windows7下請先讓前一個帳號的Login.exe進入遊戲，不然沒辦法開啟下一個

在`simple_mode.exe`的資料夾下寫一個`bat`  example: `start.bat`

```bash
simple_mode.exe -acc 這裡是遊戲帳號 -pwd 這裡是遊戲密碼
simple_mode.exe -acc 這裡是遊戲帳號1 -pwd 這裡是遊戲密碼2
simple_mode.exe -acc 這裡是遊戲帳號3 -pwd 這裡是遊戲密碼3
...
```

#### Windows7

```bash
simple_mode.exe -acc 這裡是遊戲帳號 -pwd 這裡是遊戲密碼 -mode login
simple_mode.exe -acc 這裡是遊戲帳號1 -pwd 這裡是遊戲密碼2 -mode login
simple_mode.exe -acc 這裡是遊戲帳號3 -pwd 這裡是遊戲密碼3 -mode login
...
```



## TODO

- [ ] 基本帳號密碼加密儲存，避免明碼
- [ ] Shell mode
- [ ] 儲存驗證碼
- [ ] GUI (不確定)