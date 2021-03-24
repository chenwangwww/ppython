import redis
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)
# r.set('foo', 'bar')
# x = r.get('foo')
# print(x)
# print(r'a\nb')
# print(b'a\nb')
# print('a\nb')

r.setex('foo2', 5, 'orange')
x = r.get('foo2')
print(x)
time.sleep(5)
x = r.get('foo2')
print(x)