# BillfishScripts

## 将pixiv图按作者分文件夹存储
### 入库Billfish并刮削
- 在Billfish素材库下新建`待处理`文件夹, 将**以pid开头**的pixiv图片放入文件夹内
- 入库完成后, 使用[Pixiv2Billfish](https://github.com/Ai-desu-2333/Pixiv2Billfish)刮削Tag
### 执行脚本
修改root为素材库路径, `python move_dir_by_author.py`即可, 有缺的库自行补上
可能会存在`Error:404`刮削失败的, 需要手动处理, 会移动到`CantDeal`文件夹内
### 附上无损压缩图像脚本
jpeg优化
```powershell
 Get-ChildItem -Filter *.jpg | ForEach-Object -Parallel { jpegoptim -s --all-progressive "$_"} -ThrottleLimit 16
```
png->webp
```powershell
Get-ChildItem -Filter *.png | ForEach-Object -Parallel { cwebp -z 9 -v "$_" -o "$($_.Directory)\$($_.Basename).webp" } -ThrottleLimit 16
```
