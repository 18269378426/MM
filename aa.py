#
a = 'hello world'
# print('数字：' + a + '\n\r'+ 'hello world')
a = a[:4]
print(a)

#加密手段
import hashlib
# hash = hashlib.md5()#创建了一个md5算法的对象(md5不能反解)，即造出hash工厂
# hash.update(bytes('password',encoding='utf-8'))#运送原材料喽，要对哪个字符串进行加密，就放这里
# print(hash.hexdigest())#产出hash值,拿到加密字符串