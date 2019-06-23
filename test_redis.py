import redis
client = redis.StrictRedis()

client.flushall()
#print(client.hget("庄子_page_229", "content").decode("utf-8"))
#print(client.hgetall("庄子_page_229"))
#client.hexists("庄子_page_229", "content")

#print(client.hgetall("庄子_page_0"))

#print(client.ttl("庄子_page_229"))

#test_json = {"a":'{"e":3,"m":5}',
#             "b":'{"f":4}'
#             }
#print (test_json)
#client.hmset("test_map", test_json)