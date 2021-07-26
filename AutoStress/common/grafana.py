# import requests
#
#
# def download_img(url, headers, img_name):
#
#
#     """根据url下载图片"""
#
#     # 请求url地址
#     res = requests.get(url=url, headers=headers)
#
#     # 将返回的图片数据，写入文件保存
#     with open(img_name, 'wb') as f:
#         f.write(res.content)
#
#
# def main():
#     # 设置图片的url地址
#     url = 'http://10.10.10.2:8084/render/d-solo/9CWBz0bik/qa-node-exporter-jian-kong-zhan-shi-kan-ban?orgId=1&from=1626883200000&to=1626969599000&var-interval=1m&var-env=&var-name=&var-node=10.10.10.2:8089&var-maxmount=%2Frootfs&panelId=13&width=1000&height=500&tz=Asia%2FShanghai'
#     # 设置请求headers信息
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
#     }
#     # 设置保存本地图片的名称
#     img_name = "D:\\save2.png"
#     # 执行下载图片
#     download_img(url, headers, img_name)
#
#
# if __name__ == '__main__':
#     main()
