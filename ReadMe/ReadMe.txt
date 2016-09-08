1. spark 简略输出:

Spark（和PySpark）的执行可以特别详细，很多INFO日志消息都会打印到屏幕。开发过程中，这些非常恼人，因为可能丢失Python栈跟踪或者print的输出。为了减少Spark输出 – 你可以设置SPARKHOME/conf下的log4j。首先，拷贝一份SPARK_HOME/conf/log4j.properties.template文件，去掉“.template”扩展名。

~$ cp $SPARK_HOME/conf/log4j.properties.template $SPARK_HOME/conf/log4j.properties

编辑新文件，用WARN替换代码中出现的INFO。你的log4j.properties文件类似：

# Set everything to be logged to the console
 log4j.rootCategory=WARN, console
 log4j.appender.console=org.apache.log4j.ConsoleAppender
 log4j.appender.console.target=System.err
 log4j.appender.console.layout=org.apache.log4j.PatternLayout
 log4j.appender.console.layout.ConversionPattern=%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n
# Settings to quiet third party logs that are too verbose
 log4j.logger.org.eclipse.jetty=WARN
 log4j.logger.org.eclipse.jetty.util.component.AbstractLifeCycle=ERROR
 log4j.logger.org.apache.spark.repl.SparkIMain$exprTyper=WARN
 log4j.logger.org.apache.spark.repl.SparkILoop$SparkILoopInterpreter=WARN


2. Spark ML Pipeline :

前面提到，本文的目的是使用 Spark ML Pipeline 构建一个对目标数据集进行分类预测的机器学习工作流，案例背景已经相当清晰，在了解了数据集本
身和 ML Pipeline 的相关知识后，接下来就是编程实现了。关于实现基本思路和关键的 11 个步骤笔者已经在代码中做了详细解释，为了方便读者理解
，这里特别的把该实例的 Pipeline 里包含的 4 个 Stage 重点介绍下。

这四个 Stage 分别对应代码注释里的步骤 2-5，作用如下：

第一个，使用 StringIndexer 去把源数据里的字符 Label，按照 Label 出现的频次对其进行序列编码, 如，0,1,2，…。在本例的数据中，可能这个
步骤的作用不甚明显，因为我们的数据格式良好，Label 本身也只有两种，并且已经是类序列编码的”0”和”1”格式。但是对于多分类问题或者是 Label
本身是字符串的编码方式，如”High”,”Low”,”Medium”等，那么这个步骤就很有用，转换后的格式，才能被 Spark 更好的处理。

第二个，使用 VectorAssembler 从源数据中提取特征指标数据，这是一个比较典型且通用的步骤，因为我们的原始数据集里，经常会包含一些非指标数
据，如 ID，Description 等。

第三个，创建一个随机森林分类器 RandomForestClassifier 实例，并设定相关参数，主要是告诉随机森林算法输入 DataFrame 数据里哪个列是特征
向量，哪个是类别标识，并告诉随机森林分类器训练 5 棵独立的子树。

第四个，我们使用 IndexToString Transformer 去把之前的序列编码后的 Label 转化成原始的 Label，恢复之前的可读性比较高的 Label，这样
不论是存储还是显示模型的测试结果，可读性都会比较高。

这几个 Stage 都会被用来构建 Pipeline 实例，并且会按照顺序执行，最终我们根据得到的 PipelineModel 实例，进一步调用其 transform 方法
，去用训练好的模型预测测试数据集的分类。


3. 一个典型的机器学习构建包含若干个过程
(1)源数据ETL
(2)数据预处理
(3)特征选取
(4)模型训练与验证
以上四个步骤可以抽象为一个包括多个步骤的流水线式工作，从数据收集开始至输出我们需要的最终结果。因此，对以上多个步骤、进行抽象建模，
简化为流水线式工作流程则存在着可行性，对利用spark进行机器学习的用户来说，流水线式机器学习比单个步骤独立建模更加高效、易用。

受 scikit-learn 项目的启发，并且总结了MLlib在处理复杂机器学习问题的弊端(主要为工作繁杂，流程不清晰)，旨在向用户提供基于DataFrame
之上的更加高层次的 API 库，以更加方便的构建复杂的机器学习工作流式应用。一个pipeline 在结构上会包含一个或多个Stage，每一个 Stage
 都会完成一个任务，如数据集处理转化，模型训练，参数设置或数据预测等，这样的Stage 在 ML 里按照处理问题类型的不同都有相应的定义和实现
 。两个主要的stage为Transformer和Estimator。Transformer主要是用来操作一个DataFrame 数据并生成另外一个DataFrame 数据，比如svm
 模型、一个特征提取工具，都可以抽象为一个Transformer。Estimator 则主要是用来做模型拟合用的，用来生成一个Transformer。可能这样说
 比较难以理解，下面就以一个完整的机器学习案例来说明spark ml pipeline是怎么构建机器学习工作流的。