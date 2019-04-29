# email-bpm  简介

email-bpm ,顾名思义是利用email系统实现的ｂｐｍ，ｂｐｍ是指business process management,即业务流程管理，往小了说就是一个工作流系统．
开发本项目的初衷是：

- 希望拥有一个足够简单，并且方便自行扩展的业务流程引擎，可以执行一些简单的人类业务工单流转和简单的自动任务
- 它要支持复杂的网络环境，并不依赖于ｗｅｂ服务器和数据库系统
- 使用简单，并且与现有工作方式相近

目前应用它的主要场景是可以实现运维工作中一些资源申请审批与实施工作．尽可能用它来实现办公的自动化．

## 技术实现思路

利用email系统的低成本，和消息机制来实现任务通知；python语言来实现主逻辑，包括流程调度引擎，解析流程定义，通过收发邮件实现消息传递；通过excel模板定义工单界面，通过json来定义流程描述，通过excel来实现流程实例及日志的保存．另外开发自化运维任务的执行代理，用python开发，可调用shell脚本来实现对主机系统上的资源的操作．比如实现ｄｎｓ的维护，nginx反向代理的维护等

后期可以通过不断的补充流程定义，excel模板和执行代理端的脚本来扩展新的业务场景．


##  开发人员参考

### python 操作 excel 的模块
官方　　　https://pypi.org/project/openpyxl/
中文入门　https://segmentfault.com/a/1190000016256490
### python　访问邮箱的模块
发邮件　　https://docs.python.org/3/library/smtplib.html
收邮件　　https://docs.python.org/3/library/imaplib.html





