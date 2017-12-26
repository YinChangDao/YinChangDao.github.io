---
layout: post
title:  "Core Data 基础"
subtitle: ""
date:   2017-12-26 22:30:13 -0400
background: '/img/posts/04.jpg'
---

### 一.基础
Core Date 使用 **NSManagedObjectModel** 的实例对象为刚要。这个 model 是 **NSEntityDescription** 的实例对象的集合。一个 **NSEntityDescription** 对象可以当做是数据库中的一个表格。 

#### managed object model 
* 使用 **NSAttributeDescription** 创建各种 **properties** 和 **relationships**；  
* 将这些 **attributes** 装进 **entity** 中；  
* 将这些 **entities** 初始化 **manage object model**.  

#### managed object context
* 使用 **managed object model** 初始化创建一个**NSPersistentStoreCoordinator** 对象；  
* 创建一个存放数据库的路径；
* 使用这个路径创建一个 **NSPersistentStore** 对象，并且设置存储数据的格式（XML, JSON...）  
* 创建一个 **NSManagedObjectContext** 对象，并设置并发类型为主队列并发；
* 设置 **managed object context** 的 **coordinator**。  

#### save  
* 创建模型对象，使用 **insertIntoManagedObjectContext** 初始化；
* 设置模型对象对应 **attributes** 的各属性值;   
* 调用 **managed object context** 的 **save** 方法进行保存。

#### fetch
* **NSFetchRequest**  
* [moc excuteFecthRequest: error:]

### 二.要点

#### override
* 不鼓励重载 **initWithEntity:insertIntoManagedObjectContext:** 和 **description**。
* 如果基本属性类型中不足以表达想要的属性，如NSColor, 这种情况需要子类化 **NSManagedObject**.
* 初始化方法 **initWithEntity:insertIntoManagedObjectContext:** 不建议重载，但是可以重载 **awakeFromInsert** 和 **awakeFromFetch** 方法，**awakeFromInsert**方法在对象创建后调用，在整个对象的生命周期中只会调用一次，可以重载该方法，在该方法中记录对象被创建的时间是很方便的。**awakeFromFetch** 方法在获取过程中，对象从持久化存储库中重新被初始化时调用。在创建临时对象或者缓存时可以使用这个方法。  
* 不要重载 **dealloc** 方法，可以重载 **didTurnIntoFault**方法。  

#### Connecting the Model to Views
* 在 iOS 中，可以使用 **NSFetchedResultsController** 把模型和视图联系起来。  
* 在初始化好 fetchedResultsController 后需要调用它的 **performFetch** 方法以开始监控 managed model 的变化情况。  
* tableView 的数据源方法可以十分方便的调用 fetchedResultsController 的相关提取数据的方法来实现视图和数据的逻辑。  
* 通过 fetchResultsController 的一些代理方法可以操作数据的增加/删除/改变等操作。
* 将数据按指定的字段进行分组：

```objective-c
// Create and configure a fetch request with the Book entity.
    NSFetchRequest *fetchRequest = [[NSFetchRequest alloc] init];
    NSEntityDescription *entity = [NSEntityDescription entityForName:@"Book" inManagedObjectContext:self.managedObjectContext];
    [fetchRequest setEntity:entity];
// Create the sort descriptors array.
    NSSortDescriptor *authorDescriptor = [[NSSortDescriptor alloc] initWithKey:@"author" ascending:YES];
    NSSortDescriptor *titleDescriptor = [[NSSortDescriptor alloc] initWithKey:@"title" ascending:YES];
    NSArray *sortDescriptors = @[authorDescriptor, titleDescriptor];
    [fetchRequest setSortDescriptors:sortDescriptors];
    
    // Create and initialize the fetch results controller.
    //** ! 用于分段的keypath 1.必须也是一个 sortDescriptor. 2.必须是第一个 sortDescriptor；
    //** ! 对数据进行缓存，但是数据改变时，必须提前调用 deleteCacheWithName：使缓存失效
    _fetchedResultsController = [[NSFetchedResultsController alloc] initWithFetchRequest:fetchRequest 
    managedObjectContext:self.managedObjectContext 
    sectionNameKeyPath:@"author" cacheName:@"Root"];
    _fetchedResultsController.delegate = self;
```

* 任何时候传递一个 **NSManagedObject** 引用，都应该声明为 weak ，这可以保护你的 ViewController 在 NSManagedObject 被删除时不会引用一个不存在的对象。使用 weak 当对象被删除时，属性会被自动置为 nil。

### Concurrency
为了不使界面迟钝，在处理数据时（如将 json 数据导入 core data）应该放在子线程中进行处理.
 






