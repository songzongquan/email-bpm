# 需求说明

## 功能需求

### 角色说明
- 申请人　　　具体项目实施人员
- 运维管理者　即运维负责人，如王雨佳、宋宗权
- 运维执行代理  即是一个服务程序，这可经代替人接收申请邮件，自动执行相关业务处理。
- 项目负责人　即具体项目的负责人，如智慧用电的负责人黄勇
- 平台负责人　即整个cloudiip平台的总负责人  常志刚

### 用例说明

#### 邮箱注册

##### 操作步骤

1. 如果用户给cloudiip_ops@bonc.com.cn邮箱发送邮件，被系统收到后，系统先在内部的邮箱用户列表中查询，发现没有注册，则回复一封邮件，提示用户注册自已的邮箱，并说明理由，还有注册用的excel模板，模板中应包含 姓名，部门、邮箱地址，手机号等。

2. 用户按照提示，编写注册用的excel附件，提交给cloudiip_ops@bonc.com.cn

3. 系统收到该邮件后，下载并解析excel中的申请地址，如果与发件人的地址一致，即通过基本验证，就转发邮件给审核人（即运维管理者）。

4. 审核人通人工判断，此人是否合法，是否为公司员工，然后给以通过处理，或不通过处理。如果通过后，将邮件发回给cloudiip_ops@bonc.com.cn
5. 系统最多5分钟后收到此邮件，根据同意/不同意生成新的邮件，并附件这个申请附件，发给申请人。如果是同意，同时还会将该申请人的地址保存在系统的合法邮箱列中。


#### 域名反向代理申请

##### 操作步骤

1. 首先，由申请人填写一个excel申请单，作为附件发送到cloudiip_ops@bonc.com.cn邮箱。此附件有约定的模板，并由申请人填写要反向代理的域名以及ip地址，申请人员姓名以及对应的项目负责人的姓名。

2. 系统最迟在5分钟后会收到此邮件，并通过对附件名称得知它是域名反向代理申请，并通过将它的内容与模板比对进行合法性检查

3. 如果附件合法性检查通过，则将附件下载到本地，将附件文件名加一个业务流水号的后缀，然后根据域名反向代理申请处理流程，将些修改过的附件，转发给项目负责人。

4. 项目负责人收到申请邮件，下载附件，打开附件excel，填写审批意见和决定，即同意或不同意，然后重新发回给cloudiip_ops@bonc.com.cn。

5. 最多5分钟后，系统会收到此邮件，通过对附件名称与内容分析，得知其业务类型，并按事先定好的处理流程处理，如果项目负责人不同意申请，则将此附件再转发给申请 人者本人，申请者本人或者按要求重新修改申请附件再将发给cloudiip_ops@bonc.com.cn,或者放弃此次申请，重新编写新的申请附件提交申请。如果项目负责人同意申请，则系统会将此附件转发给平台负责人，平台负责的操作与项目负责人相似，也是决定同意或是不同意，填好附件后，转发给cloudiip_ops@bonc.com.cn.

6. 如果平台负责人同意，则系统会将附件转发给运维执行代理对应的邮箱地址。

7. 最多5分钟后，运维执行代理收到该邮件，同样的对附件的名称与内容进行解读，得知是域名反向代理申请，并进行实施处理，实施的参数从附件中提取，并将实施结果写回附件，即在附件中记录，执行时间，执行状态等，然后发给原申请人、项目负责人、平台负责人以及运维管理者。

7. 如果执行代理执行过程中出现异常，则也生成邮件通知一下运维管理者，由运维管理者手工处理。

##### 业务说明

1. excel附件的名称前缘为中文可理解的业务类型，如“域名反向代理申请”，后缀为随机产生流水号，要求全局唯一性。

2. excel附件内容包括两部分，一部分是申请的业务参数，如域名，对应ip地址等，另一部分是流程跟踪信息，即申请人、申请时间、项目负责人 审批时间、平台负责人及审批时间，审批结果，意见等。运维执行人、执行时间，执行状态等。

3. 自始至终，流水号由系统自动生成，在附件流转过程中，附件文件名称不得人为修改，只可修改excel中的内容，并且只能修改特定的表格项，比如，项目负责人不 能改写原始的域名与ip项。

4. 对于执行代理来说，为了安全，它只能接收来自cloudiip_ops@bonc.com.cn发的邮件，其它来源邮件都拒绝接收。

5. 为了保证安全，系统会对收到的发给cloudiip_ops@bonc.com.cn的邮件进行合法检查，只会处理来自bonc.com.cn的并通过注册而来的邮箱的邮件。其它邮件都认不自动作回应，由人工检查处理。



#### dns解析申请

此用例整体处理流程与反向代理处理流程非常相似，不同之处仅限于附件的excel模板的不同，以处执行代理的处理逻辑不同，因此不再赘述审批流程。

#### 虚拟机申请

大体同上，只是现在虚拟机申请暂时做不到执行代理自动执行，可能最后环节是发邮件给IDC运维负责人，如郭澳达，它执行完后按约定填写附件，发回给cloudiip_ops@bonc.com.cn

其它流程同上。


#### 堡垒机权限申请

同上。

特别说明，执行代理可能不能直接调用脚本来执行堡垒机授权，因暂时没有可编程的接口，希望能通过python webdriver模拟人工操作web界面来实现。如若实现不了，则只能由运维人员手工执行。但会让系统随机分配任务。
