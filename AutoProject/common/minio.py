# from minio import Minio
# from minio.error import InvalidResponseError
# import logging
# logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置
#
#
#
# class Bucket:
#     def __init__(self, host="192.168.2.99:80", access_key='biomind', secret_key='biomind123'):
#         # 使用endpoint、access key和secret key来初始化self.minioClient对象。
#         self.minioClient = Minio(host,
#                                  access_key=access_key,
#                                  secret_key=secret_key,
#                                  secure=False)
#
#     # 创建桶(调用make_bucket来创建一个存储桶) make_bucket函数
#     """
#     注：创建桶命名限制：小写字母，句点，连字符和数字是
#     唯一允许使用的字符（使用大写字母、下划线等命名会报错），长度至少应为3个字符
#     """
#
#     def create_bucket(self):
#         try:
#             if self.minioClient.bucket_exists(bucket_name='pictures'):  # bucket_exists：检查桶是否存在
#                 logger.info("该存储桶已经存在")
#             else:
#                 self.minioClient.make_bucket("pictures")
#                 logger.info("存储桶创建成功")
#         except InvalidResponseError as err:
#             logger.error(err)
#
#     # 列出所有的存储桶 list_buckets函数
#     def get_bucket_list(self):
#         try:
#             buckets = self.minioClient.list_buckets()
#             for bucket in buckets:
#                 logger.info(bucket.name, bucket.creation_date)  # 获取桶的名称和创建时间
#         except InvalidResponseError as err:
#             logger.error(err)
#
#     # 删除存储桶
#     def get_remove_bucket(self):
#         try:
#             self.minioClient.remove_bucket("pictures")
#             logger.info("删除存储桶成功")
#         except InvalidResponseError as err:
#             logger.error(err)
#
#     # 列出存储桶中所有对象  或者使用 list_objects_v2也可
#     def get_bucket_files(self):
#         try:
#             objects = self.minioClient.list_objects('testfiles', prefix=None,
#                                                     recursive=True)  # prefix用于过滤的对象名称前缀
#             for obj in objects:
#                 logger.info(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
#                       obj.etag, obj.size, obj.content_type)
#         except InvalidResponseError as err:
#             logger.error(err)
#
#     # 列出存储桶中未完整上传的对象
#     def get_list_incomplete_uploads(self):
#         try:
#             uploads = self.minioClient.list_incomplete_uploads('testfiles',
#                                                                prefix=None,
#                                                                recursive=True)
#             for obj in uploads:
#                 logger.info(obj.bucket_name, obj.object_name, obj.upload_id, obj.size)
#         except InvalidResponseError as err:
#             logger.error(err)
#
#     # 获取存储桶的当前策略
#     def bucket_policy(self):
#         try:
#             policy = self.minioClient.get_bucket_policy('testfiles')
#             logger.info(policy)
#         except InvalidResponseError as err:
#             logger.error(err)
#
#     # # 给指定的存储桶设置存储桶策略
#     # def get_set_bucket_policy(self):
#     #     try:
#     #         self.minioClient.set_bucket_policy('testfiles', policy.READ_ONLY)
#     #     except InvalidResponseError as err:
#     #         logger.error(err)
#
#     # 获取存储桶上的通知配置
#     def bucket_notification(self):
#         try:
#             # 获取存储桶的通知配置。
#             notification = self.minioClient.get_bucket_notification('testfiles')
#             logger.info(notification)
#             # 如果存储桶上没有任何通知：
#             # notification  == {}
#         except InvalidResponseError as err:
#             logger.error(err)
#
#     # 给存储桶设置通知配置
#     def set_bucket_notification(self, bucket_name, notification):
#         pass
#
#     # 删除存储桶上配置的所有通知
#     def remove_all_bucket_notifications(self, bucket_name):
#         try:
#             self.minioClient.remove_all_bucket_notifications('mybucket')
#         except InvalidResponseError as err:
#             logger.error(err)
#
#     # 监听存储桶上的通知
#     def listen_bucket_notification(self, bucket_name, prefix, suffix, events):
#         pass
#
#
# if __name__ == '__main__':
#     Bucket().bucket_notification()
