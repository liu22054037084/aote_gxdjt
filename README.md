# aote_gxdjt

### 这是一个半自动bt下载的cms10的视频更新脚本

###### 它可以利用bt的rss订阅下载后，扫描下载位置的视频位置，并且可以把他移动到指定位置也可以自己设置取消（我们利用网盘挂载，直接把他转移到相关网盘里面，利用其他的网盘映射工具并且可以生成直链接的进行加工，用来减少服务器的占用！),这里面我们已经设置了最优的cms10的数据库写入，建议根据不同需求进行修改（大部分不用修改，只需要自己修改一下分类之类的即可，修改分类的时候也请修改index.php里面的分类，当然这一切看个人需求！）

##### 目前这个项目只是有我们个人使用，后期优化以后，更符合大众以后我们会对其写相关的使用文档！

# 各个文件下文件作用

#### sql_class

###### 	是我写的sql操作的类，里面主要有两个分别是mysql与sqlite的操作，虽然有部分注释，但是注释并不完全，而且根据自己的使用，改动比较大。

#### get_files

###### 	单纯的获取某个文件夹下面的某个后缀的所有文件，包括子文件内部的，为了追求速度，大量的占用了内存，写的也比较怪。

#### v3_api

###### 	在项目中，并没有使用到，这个是Cloudreve的api使用，我们自己摸索的，但是后来舍弃了，不是不好用只是和我们用的其他内容相冲突（比如两个Cloudreve在一个服务器会因为v3调用的问题而冲突）

#### assets

###### 	这个里面放的是一个php网页这个网页，用可视化对sqlite进行部分操作，然后主体程序main.py用sqlite当作储存与条件库进行操作后对mysql写入，这是我们妥协后的产物，毕竟sqlite的功能能省去很多我们自己写的代码（比如说排序与模糊搜索之类的，当然要是后期有更好的办法也许会舍弃，但是我估计不会，毕竟我会用sqlite储存一部分东西作为备份来使用。）

#### .env

###### 	配置文件，我们没有删除我们自己的信息，不过放心，需要有ip认证才能访问的哦亲……

## 我们附带了上传和拉取，嘛……打命令很麻烦，不如搞个能偷懒的~
