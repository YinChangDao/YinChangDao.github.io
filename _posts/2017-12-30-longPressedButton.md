---
layout: post
title:  "实现UIButton的长按响应事件功能"
subtitle: ""
date:   2017-12-30 20:33:38 -0400
background: '/img/posts/05.jpg'
---

## 实现UIButton的长按响应事件功能

> 需求： 长按一个按钮，希望隔 0.3 秒触发一次事件

```objective-c
...
_inLoop = NO;
...

- (IBAction)clickedNextBtnDown:(UIButton *)sender {
    _isTouchNext = YES;
    [self nextData];
}

- (IBAction)clickedNextBtnUp:(id)sender {
    _isTouchNext = NO;
}

- (void)nextData {
    //** ! _inLoop 是为了阻止多次快速点按后，一个 0.3 秒内可能出现多次响应的情况
    if ( !_inLoop ) {
        _inLoop = YES;
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(0.3 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            _inLoop = NO;
            if (_isTouchNext) {
                [self nextData];
            }
        });
    }
}
```