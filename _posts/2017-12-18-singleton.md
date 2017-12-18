---
layout: post
title:  "Singleton"
subtitle: ""
date:   2017-12-19 00:15:13 -0400
background: '/img/posts/01.jpg'
---

## 单例

> 只能共享不能复制的资源

## 严格实现
### 创建
```objective-c
+ (instancetype)sharedMediaData {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _instance = [[self alloc] init];
    });
    return _instance;
}

+ (id)allocWithZone:(struct _NSZone *)zone {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _instance = [super allocWithZone:zone];
    });
    return _instance;
}

- (id)copyWithZone:(NSZone *)zone {
    return _instance;
}

```
### 内存管理
~~~
- (id)retain {
	return self;
}

- (NSUInteger)retainCount {
	return NSUIntegerMax;
}

- (void)release {
	// 什么也不做
}

- (id)autorelease {
	return self;
}
~~~
### 子类化一个单例类
`alloc`调用被转发给`super`, 意味着如果不做修改地子类化单例，返回的实例将总是`Singleton`。使用一些`Foundation`中的函数，可以根据类的类型实例化任何对象。  

~~~objective-c
// 在父类的创建方法中可以改为使用 NSAllocateObject
+ (instancetype)sharedMediaData {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _instance = [NSAllocaceObject([self class], 0, NULL) init];
    });
    return _instance;
}
~~~
