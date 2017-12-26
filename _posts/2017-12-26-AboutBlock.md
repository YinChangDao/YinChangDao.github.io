---
layout: post
title:  "Block 对变量的拷贝"
subtitle: ""
date:   2017-12-26 22:10:13 -0400
background: '/img/posts/03.jpg'
---

## Block 对变量的拷贝

#### 1.不可变类型的属性
> **test1** 中 **block** 里使用 `_nameArr` 实际上是 `self.nameArr`, 这里 **block** 拷贝的是指针 **self**, 用 **self'** 表示, 而 **self'** 和 **self** 指向同一块内存，故 2s 后打印的 `_nameArr` 是已经改变了指向的新的数组。

```objective-c
...
@property (nonatomic, strong) NSArray *nameArr;
...
    
- (void)test1 {
    _nameArr = @[@"Penny", @"Amy"];
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSLog(@"_nameArr: %@", _nameArr);
    });
    
    _nameArr = @[@"Sheldon", @"Leonard"];
}
.
.
2017-03-15 15:41:08.788189 BlockTest[4610:1392720] _nameArr: (
    Sheldon,
    Leonard
)

```

#### 2.不可变类型的局部变量
> **test2** 中 **block** 拷贝了 `tempArr`指针, 2s 后打印的还是这个拷贝的指针指向的内容，即原内容，而外部的 `tempArr` 实际上已经改变了指向，这里 `tempArr` 原先指向的内存将在 **block** 执行完毕后释放。

```objective-c
- (void)test2 {
    NSArray *tempArr = @[@"Penny", @"Amy"];
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSLog(@"tempArr: %@", tempArr);
    });
    
    tempArr = @[@"Sheldon", @"Leonard"];
}

.
.
2017-03-15 15:48:54.515345 BlockTest[4616:1393958] tempArr: (
    Penny,
    Amy
)
```

#### 3.可变类型的属性
> **test3** 同 **test1**, 只不过 2s 后打印的是增加了数据的原数组。

```objective-c
...
@property (nonatomic, strong) NSMutableArray *mutableNameArr;
...

- (void)test3 {
    _mutableNameArr = [NSMutableArray arrayWithArray:@[@"Penny", @"Amy"]];
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSLog(@"mutableNameArr: %@", _mutableNameArr);
    });
    
    [_mutableNameArr addObject:@"Bernadette"];
}

.
.
2017-03-15 15:53:23.541348 BlockTest[4620:1394686] mutableNameArr: (
    Penny,
    Amy,
    Bernadette
)
```

#### 4.可变类型的局部变量
> **test4** 中 **block** 拷贝了 `mutableTempArr` 指针, 外部的 `mutableTempArr` 并没有改变指向，只是添加了一个数据，故 2s 后 **block** 中拷贝的指针指向的这同一块内存是已经添加了数据的原数组。

```objective-c
- (void)test4 {
    NSMutableArray *mutableTempArr = [NSMutableArray arrayWithArray:@[@"Penny", @"Amy"]];
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSLog(@"mutableTempArr: %@", mutableTempArr);
    });
    
    [mutableTempArr addObject:@"Bernadette"];
}

2017-03-15 15:56:55.511302 BlockTest[4626:1395731] mutableTempArr: (
    Penny,
    Amy,
    Bernadette
)
```


#### 5.基本数据类型局部变量
> **test5** **test6** 演示了加了 **__block** 修饰的变量在外部修改了，那么 **block** 内部也可见，当然，在 **block** 内部修改了，外部也可见。

```objective-c
- (void)test5 {
    NSInteger i = 0;
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSLog(@"i: %ld", i);
    });
    
    i = 1;
}

.
.
2017-03-15 16:01:08.140533 BlockTest[4632:1396576] i: 0
```

#### 6.加__block的基本数据类型局部变量
```objective-c
- (void)test6 {
    __block NSInteger i = 0;
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSLog(@"i: %ld", i);
    });
    
    i = 1;
}

.
.
2017-03-15 16:03:33.550104 BlockTest[4640:1397522] i: 1
```
 


