[toc]

```
├── data
├── name.txt
├── post.py
├── readme.md
├── requirements.txt
├── utils
    ├── data.back.json
    ├── speechTranscriptDownloader.py
    ├── YoutubeCrawler.py
    ├── YoutubeDataApi.py
    └── youtube_dl

```

整个思路大概是先使用YoutubeCrawler.py 先把链接爬取下来，目前该代码逻辑上还有点问题，使用的api是1.2介绍的接口，每日会有请求数量限制。

然后使用speechTranscriptDownloader.py 把音频和字幕下载下来



## 1.1 使用流程

**不需要登陆**

1. 打开youtube，地区设置为国家（可选，不是必要条件）

2. 使用特定的语言搜索，在过滤栏中筛选出选择字幕，筛选出有字幕的视频，打开视频后设置字幕语言

   **注意** 搜索到的视频标题最好是全是当前国家语言，否则音频会与字幕不是同一个语言

3. 将其链接放到1.2 提取音频网站处下载，并且原视频提取字幕（注意有多种语言的字幕）

### 1.2 寻找资源

#### [YouTube Data API 开发文档](https://developers.google.com/youtube/v3/getting-started)

[Youtube Data Api](https://developers.google.com/youtube/v3/quickstart/python)

YouTube API中的[Search/list接口](https://developers.google.com/youtube/v3/docs/search/list)，可以直接根据关键字获取符合条件的vedio、channel、playlist，下面是官方给出的demo

#### 1.2.1 查找某个频道所有视频

1.  `查询某频道的播放列表`

```http
GET https://youtube.googleapis.com/youtube/v3/playlists?part=id%2CcontentDetails&channelId=UC_x5XG1OV2P6uZZ5FSM9Ttw&maxResults=25&pageToken=(此参数为空时为第一页的结果)&key=[YOUR_API_KE# 语音语料收集

# 1. 使用YouTube

## 1.1 使用流程

**不需要登陆**

1. 打开youtube，地区Y] HTTP/1.1

```

其中part为返回信息的要求，channalId 为频道的id，进入主页可以从url查看到,返回值中包含nextPageToken，为下一页分页pageToken的参数。

```json
{
  "kind": "youtube#playlistListResponse",
  "etag": "0GG12we-Ghpy-L5Lrh9Kmgelc2s",
  "nextPageToken": "CBkQAA",
  "pageInfo": {
    "totalResults": 447,
    "resultsPerPage": 25
  },
  "items": [
    {
      "kind": "youtube#playlist",
      "etag": "1QtT7t36J_m18HLeQUmlwGxNfjw",
      "id": "PLOU2XLYxmsIL5MoZ5LrrxfVk3V04evsMm",
      "contentDetails": {
        "itemCount": 33
      }
    },
    {
      "kind": "youtube#playlist",
      "etag": "fMRNHbKWazt8V25eYp0kUUcSylE",
      "id": "PLOU2XLYxmsILJWy1k3BO7dScDSPL4KM2e",
      "contentDetails": {
        "itemCount": 7
      }
    },
    {
      "kind": "youtube#playlist",
      "etag": "A4996LXwaN7MR2ab9cyVCF_sk5E",
      "id": "PLOU2XLYxmsIKhzT-8-78KerqzhBfVhMyI",
      "contentDetails": {
        "itemCount": 6
      }
    }]
}
```




2. `根据播放列表查视频列表`

```http
   GET https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails%2Cid&playlistId=PLOU2XLYxmsIL5MoZ5LrrxfVk3V04evsMm&pageToken=(此参数为空时为第一页的结果)&key=[YOUR_API_KEY] HTTP/1.1
   
```

```json
   {
     "kind": "youtube#playlistItemListResponse",
     "etag": "1X4Z0wTmU2TJpYIRYQD-bf2NFX4",
     "nextPageToken": "CAUQAA",
     "items": [
       {
         "kind": "youtube#playlistItem",
         "etag": "fSMdJGz36AQf96npa0T2a_E9QMg",
         "id": "UExPVTJYTFl4bXNJTDVNb1o1THJyeGZWazNWMDRldnNNbS5DQ0MyQ0Y4Mzg0M0VGOEYw",
         "contentDetails": {
           "videoId": "DcN_hcHXR_0",
           "videoPublishedAt": "2019-05-18T00:00:00Z"
         }
       },
       {
         "kind": "youtube#playlistItem",
         "etag": "6sMOFXDb6o1ppzewT9zmXMK-gSI",
         "id": "UExPVTJYTFl4bXNJTDVNb1o1THJyeGZWazNWMDRldnNNbS4zRjM0MkVCRTg0MkYyQTM0",
         "contentDetails": {
           "videoId": "xMBkZRCA_Lo",
           "videoPublishedAt": "2020-04-02T15:00:25Z"
         }
       }]
   }
```

#### 1.2.2 参看某个视频字幕情况

```http
GET https://youtube.googleapis.com/youtube/v3/captions?part=id%2Csnippet&videoId=SHipM46j7SM&key=[YOUR_API_KEY] HTTP/1.1

```
其中part，进入主页可以从url查看到,返回值中包含nextPageToken，为下一页分页pageToken的参数。
```json
{
  "kind": "youtube#captionListResponse",
  "etag": "B5AQbxG15r3IERx01hWYfIuzPuM",
  "items": [
    {
      "kind": "youtube#caption",
      "etag": "O3Fi1TTQB0649009HcW70tqR_H8",
      "id": "fbwzK3OCDh7MqCSaOp6XFcdar2-XaHwB",
      "snippet": {
        "videoId": "7YkgHYElvso",
        "lastUpdated": "2020-12-07T07:01:56.637174Z",
        "trackKind": "standard",
        "language": "vi",
        "name": "",
        "audioTrackType": "unknown",
        "isCC": false,
        "isLarge": false,
        "isEasyReader": false,
        "isDraft": false,
        "isAutoSynced": false,
        "status": "serving"
      }
    }
  ]
}

```

### 1.3 使用youtube-dl下载音频及字幕

`注意`： youtube-dl 请使用utils文件夹下已经下载好的工具包，我在里面修改过一点点的源码，为了配合speechTranscriptDownloader.py的使用

[github地址](https://github.com/ytdl-org/youtube-dl)

youtubu-dl 支持网站[列表](https://github.com/ytdl-org/youtube-dl/blob/master/docs/supportedsites.md) 

#### 1.3.1 下载

* linux，mac安装

```bash
sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
# 或者
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
```

* window点击[下载](https://yt-dl.org/latest/youtube-dl.exe),并把文件路径加入到环境变量PATH中

#### 1.3.2  使用

**相关参数**

```
-x, --extract-audio              将视频转换成音频(需要ffmpeg或者 avconv和fprobe
                                 或者avprobe)
                                 
--audio-format FORMAT            指定音频格式: "best", "aac",
                                 "flac", "mp3", "m4a", "opus", "vorbis",
                                 "wav"; 默认为"best"; 在不加 -x 下不起作用
                                 
--audio-quality QUALITY          指定 ffmpeg/avconv 音频质量,输入0到9的数字
                                 0最好，9最，默认为5
                                 for VBR or a specific bitrate like 128K
                                 (default 5)
                                 
-w, --no-overwrites              不覆盖文件

--no-post-overwrites             不覆盖后处理后的音频文件，没有此参数默认覆盖之前的文件

--proxy                          使用代理翻墙下载， 需要指定协议，支持HTTP/HTTPS/SOCKS协议.
                                 如果要使用socket协议需要指定.例如socks5://127.0.0.1:1080

--write-sub                      保存字幕文件

--write-auto-sub                 保存自动生成的字幕文件，只支持youtube

--all-subs                       下载所有可用的字幕文件

--list-subs                      列出所有可用的字幕文件

--sub-format FORMAT              指定字幕格式: "srt" 或者 "ass/srt/best"

--sub-lang LANGS                 指定字幕语言（可选），使用--list-sub 来查看支持的语言
```
**示例**

打开一个视频，地址为https://www.youtube.com/watch?v=pTFMz8gn0WA

```bash
youtube-dl --list-subs https://www.youtube.com/watch?v=pTFMz8gn0WA --proxy socks5://127.0.0.1:1080
```

在没有字幕的情况下提示如下

```bash
[youtube] pTFMz8gn0WA: Downloading webpage
WARNING: video doesn't have subtitles
[youtube] pTFMz8gn0WA: Looking for automatic captions
WARNING: Couldn't find automatic captions for pTFMz8gn0WA
pTFMz8gn0WA has no automatic captions
pTFMz8gn0WA has no subtitles

```

可以通过搜索并筛选有字幕的视频

打开youtube的[FBNC Vietnam](https://www.youtube.com/channel/UC7723FqVehXq2zeRb3tP0hQ)频道，此频道为越南语的新闻播报频道，并且有越南语字幕

选择其中一个视频https://www.youtube.com/watch?v=jf9fc70RX60

```bash
youtube-dl --list-subs https://www.youtube.com/watch?v=jf9fc70RX60 --proxy socks5://127.0.0.1:1080
```

```bash
[youtube] jf9fc70RX60: Downloading webpage
[youtube] jf9fc70RX60: Looking for automatic captions
Available automatic captions for jf9fc70RX60:
Available subtitles for jf9fc70RX60:
Language formats
vi       vtt, ttml, srv3, srv2, srv1

```
下载
```bash
youtube-dl -x --audio-format wav --write-sub --sub-lang vi --sub-format vtt https://www.youtube.com/watch?v=jf9fc70RX60 --proxy socks5://127.0.0.1:1080
```

下载成功

```ba
[youtube] jf9fc70RX60: Downloading webpage
[info] Writing video subtitles to: Tin tức _ Bản tin trưa 17_11 _ Ông Trump sẽ trừng phạt Trung Quốc để trói tay ông Biden _ FBNC-jf9fc70RX60.vi.vtt
[download] Destination: Tin tức _ Bản tin trưa 17_11 _ Ông Trump sẽ trừng phạt Trung Quốc để trói tay ông Biden _ FBNC-jf9fc70RX60.webm
[download] 100% of 13.12MiB in 00:27
[ffmpeg] Destination: Tin tức _ Bản tin trưa 17_11 _ Ông Trump sẽ trừng phạt Trung Quốc để trói tay ông Biden _ FBNC-jf9fc70RX60.wav
Deleting original file Tin tức _ Bản tin trưa 17_11 _ Ông Trump sẽ trừng phạt Trung Quốc để trói tay ông Biden _ FBNC-jf9fc70RX60.webm (pass -k to keep)

```



### 1.4 注意事项

* 以上收集的数据有大量噪声，包括背景音乐，环境噪声，静音等等
* 很大概率会爬到MV， 会有大量音乐部分，空白部分。可以选择一些流量比较大一点，视频质量高且有字幕的youtuber，固定爬取
