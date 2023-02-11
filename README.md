# BiliDownloader

使用python编写的b站视频下载程序

支持登录账号

功能: 使用AV,BV,EP号下载,批量下载SS番剧,提取视频封面

支持自定义FFMPEG路径

## 使用

###  一、下载构建版本（仅用于Windows）

1. 下载并安装[ffmpeg](https://ffmpeg.org/)
2. 进入[releases](https://github.com/ScaredCube/biliDownloader/releases)页面下载最新的构建版本
3. 使用单独文件夹放置exe文件
4. 双击执行

### 二、使用源码运行

1. 安装所需库

   ```shell
   pip install bilibili-api-python
   ```

2. 下载源码

   ```shell
   git clone https://github.com/ScaredCube/biliDownloader.git
   cd biliDownloader
   ```

3. 执行代码

   ```shell
   python index.py
   ```

## 致谢

[bilibili-api](https://github.com/Nemo2011/bilibili-api) 及其样例代码

[ffmpeg](http://ffmpeg.org/)
