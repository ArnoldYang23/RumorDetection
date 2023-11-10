# 
# RumorDetection(written by English)
A project based on NLP and machine learning, aiming to identify rumors in social media.
# Rumor Detection

Traditional rumor detection models typically construct features based on the content of rumors, user attributes, and propagation methods. However, manually constructing features may lead to one-sided considerations and waste human resources. In this work, we use methods such as CNN and BERT to build a rumor detection model. By vectorizing rumor events in the text, we can explore deep features representing the text, leading to better results.

- **Language**: Python
- **Research Members**: Professor Patrick Houlihan with CIS Group2

## Dataset
Special thanks to [https://github.com/thunlp/Chinese_Rumor_Dataset](https://github.com/thunlp/Chinese_Rumor_Dataset)

- [./rumors_v170613.json](https://github.com/SophiaHanx/RumorDetection#rumors_v170613json)

This dataset includes 31,669 rumors reported from September 4, 2009, to June 12, 2017. Each line in the file represents a rumor in JSON format, with the following field interpretations:

- **rumorCode**: Unique code for the rumor, used to directly access the report page.
- **title**: Title content of the reported rumor.
- **informerName**: Weibo name of the informant.
- **informerUrl**: Weibo link of the informant.
- **rumormongerName**: Weibo name of the rumor spreader.
- **rumormongerUrl**: Weibo link of the rumor spreader.
- **rumorText**: Rumor content.
- **visitTimes**: Number of visits to the rumor.
- **result**: Result of the rumor review.
- **publishTime**: Time when the rumor was reported.

[CED_Dataset](https://github.com/SophiaHanx/RumorDetection#ced_dataset)
Contains repost and comment information related to the original Weibo text, with a total of **1,538 rumors and 1,849 non-rumors**. The dataset is divided into original Weibo text and its corresponding repost/comment content.

- original-microblog folder: All original Weibo texts (including rumors and non-rumors).
- non-rumor-repost and rumor-repost folders: Contain repost and comment information corresponding to non-rumor and rumor original texts, respectively. (This dataset does not distinguish between comments and reposts).

Each original text, comment, or repost in this data file is in JSON format, with some field interpretations:

- Original Weibo information:
  - **text**: Text content of the original Weibo.
  - **user**: User information who posted the original Weibo.
  - **time**: Time when the user posted the original Weibo (timestamp format).
- Repost/Comment information:
  - **uid**: User ID of the user who posted the repost/comment.
  - **text**: Text content of the repost/comment (if some users repost without adding comment content, this field is empty).
  - **data**: Time when the repost/comment was posted (format: 2014-07-24 14:37:38).

## Dataset Preprocessing
[RumorDetection.py](https://github.com/ArnoldYang23/RumorDetection/blob/main/RumorDetection.py "RumorDetection.py")

This code segment is mainly used for preprocessing the Chinese rumor dataset, including unzipping the dataset, parsing the original Weibo data, generating a data dictionary, creating serialized representation data, and defining a data reader function.

The following is an analysis of the main steps and outputs of this code:

1. **Unzipping the dataset**

2. **Parsing the original Weibo data**

3. **Generating `all_data.txt` file**

4. **Generating the data dictionary `dict.txt` and `dict.xlsx`**

5. **Creating serialized representation data and splitting into training and validation data**

6. **Data reader function `data_reader`**

7. **Calling the data reader function**



# 谣言检测
	传统的谣言检测模型一般根据谣言的内容、用户属性、传播方式人工地构造特征，而人工构建特征存在考虑片面、浪费人力等现象。本次时间使用CNN、BERT等方法构建谣言检测模型，将文本中的谣言事件向量化来挖掘表示文本深层的特征，可以产生更好的效果
 - **语言**：Python
- **研究成员**：Patrick Houlihan教授、CIS第二组小组成员：杨思博 、邹茏骅、黄德明、 高晟玮
## 数据集
在此感谢
[https://github.com/thunlp/Chinese_Rumor_Dataset](https://github.com/thunlp/Chinese_Rumor_Dataset)

[./rumors_v170613.json](https://github.com/SophiaHanx/RumorDetection#rumors_v170613json)

该数据集共包含从2009年9月4日至2017年6月12日的31669条谣言。文件中，每一行为一条json格式的谣言数据，字段释义如下：

- **rumorCode**: 该条谣言的唯一编码，可以通过该编码直接访问该谣言举报页面。
- **title**: 该条谣言被举报的标题内容
- **informerName**: 举报者微博名称
- **informerUrl**: 举报者微博链接
- **rumormongerName**: 发布谣言者的微博名称
- **rumormongerUr**: 发布谣言者的微博链接
- **rumorText**: 谣言内容
- **visitTimes**: 该谣言被访问次数
- **result**: 该谣言审查结果
- **publishTime**: 该谣言被举报时间

[CED_Dataset](https://github.com/SophiaHanx/RumorDetection#ced_dataset)
包含与微博原文相关的转发与评论信息，数据集中共包含**谣言1538条和非谣言1849条**。该数据集分为微博原文与其转发/评论内容。

- original-microblog文件夹：所有微博原文（包含谣言与非谣言）；
- non-rumor-repost和rumor-repost文件夹：分别包含非谣言原文与谣言原文的对应的转发与评论信息。（该数据集中并不区分评论与转发）

该数据文件中，每条原文，评论或评论均为json格式的数据，部分字段释义如下：

- 微博原文信息：
    - **text**: 微博原文的文字内容
    - **user**: 发布该条微博原文的用户信息
    - **time**: 用户发布该条微博原文的时间（时间戳格式）
- 转发/评论信息：
    - **uid**: 发布该转发/评论的用户ID
    - **text**: 转发/评论的文字内容（若部分用户转发时不添加评论内容，该项无内容）
    - **data**: 该转发/评论的发布时间（格式如：2014-07-24 14:37:38）

## 数据集预处理
[RumorDetection.py](https://github.com/ArnoldYang23/RumorDetection/blob/main/RumorDetection.py "RumorDetection.py")

这段代码主要是用于对中文谣言数据集进行预处理，包括解压缩数据集，解析原始微博数据，生成数据字典，创建序列化表示的数据，以及定义数据读取器函数。

以下是对这段代码的主要步骤和输出进行的分析：

1. **解压缩数据集**

2. **解析原始微博数据**

3. **生成`all_data.txt`文件**
  
4. **生成数据字典`dict.txt`和`dict.xlsx`**

5. **创建序列化表示的数据并划分训练数据与验证数据**
   
6. **数据读取器函数`data_reader`**

7. **调用数据读取器函数**
   
