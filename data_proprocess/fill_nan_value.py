# -*- coding: utf-8 -*
from pandas import Series, DataFrame
import pandas as pd


def FindFeactureNAorValue(data, feacture_cols, axis=0, value = 'NA', prob_dropFct = 0.95):
    '''
    函数说明：寻找每一个特征有多少value值，默认为：缺失值，及所占比率
    输入：data——整个数据集，包括Index，target
        feacture_cols——特征名
        prob_dropFct——大于这个比例，就丢掉该特征
    输出：numValue——DataFrame  index='feacture1', columns=['numnumValue', 'probnumValue']
        dropFeacture_cols——要丢掉的特征列名
    '''
    # 计算x中value值个数
    def num_Value(x, value = 'NA'):
        if value == 'NA':
            return sum(x.isnull())   #寻找缺失值个数
        else:
            return sum(x == value)  #寻找某个值value个数

    numValue = data[feacture_cols].apply(num_Value, axis=axis,args=[value])
    numValue = DataFrame(numValue, columns = ['numValue'])
    nExample = data.shape[0]
    probValue = map(lambda x: round(float(x)/nExample, 4), numValue['numValue'])
    numValue['probValue'] = probValue


    #寻找缺失值大于prob_dropFct的特征 m, , ,.
    dropFeacture = numValue[numValue['probValue'] >= prob_dropFct]
    dropFeacture_cols = list(dropFeacture.index)

    return numValue,dropFeacture_cols


def FillNAorValueOfNum(data, numFct_cols, value = 'NA', replaceNA = 'mean'):
    '''
    函数说明：为数值变量填上缺失值，缺失值为特征均值，中位数，众数
    输入：data——整个数据集，包括Index，target
        numFct_cols——数值特征名
        value ——'NA'或-1，-1也有可能为NA
        replaceNA——'mean'、'mode'、'median'
    输出：newData——DataFrame 替换value值
    '''
    #用均值、众数、中位数替换每一个特征缺失值或value值
    def fillValue(x, value=-1, replaceNA='mean'):
        if replaceNA == 'mean':
            replaceValue = x.mean()
        if replaceNA == 'mode':
            x_mode = x.mode()
            if len(x_mode) > 1:
                replaceValue = x_mode[0]
            else:
                replaceValue = x_mode
        if replaceNA == 'median':
            replaceValue = x.median()

        replaceValue = x.mean()

        x[x == value] = replaceValue
        return x

    numData = data[numFct_cols]
    if replaceNA == 'mean':
        if value == 'NA':
            newData = numData.fillna(numData.mean(),inplace=True)
        else:
            newData = numData.apply(fillValue, axis = 0, args=(value, replaceNA))

    if replaceNA == 'mode':
        if value == 'NA':
            newData = numData.fillna(numData.mode(),inplace=True)

        else:
            newData = numData.apply(fillValue, axis = 0, args=(value, replaceNA))

    if replaceNA == 'median':
        if value == 'NA':
            newData = numData.fillna(numData.median(),inplace=True)
        else:
            newData = numData.apply(fillValue, axis = 0, args=(value, replaceNA))

    return newData


from sklearn.preprocessing import LabelEncoder
def FillNAofCat(data, feacture_cols):
    '''
    函数说明：为类别变量填上缺失值，认为缺失值是新的一类
    输入：data——整个数据集，包括Index，target
        feacture_cols——特征名
    输出：catData——DataFrame 数值化后的类别特征样本
    '''
    catData = data[feacture_cols]
    catData = catData.fillna(value = -9999)

    #创建分类特征的标签编码器 jiushi字符串转化为数字
    for var in feacture_cols:
        number = LabelEncoder()
        catData[var] = number.fit_transform(catData[var].astype('str'))

    return catData


def CatToDummy(data, catfct_cols):
    '''
    函数说明：类别变量转化为哑变量
    输入：data——整个数据集，包括Index，target
        catfct_cols——类别特征名
    输出：dummyCatData——DataFrame
    '''
    catData = data[catfct_cols]
    dummyCatData = pd.get_dummies(catData,columns=catfct_cols, sparse = True)

    return dummyCatData


def GetNewValueOfNAfeacture(data, feacture_cols):
    '''
    函数说明：为有缺失值的变量创建一个新的变量 对缺失值标志为1，否则为0
    输入：data——整个数据集，包括Index，target
        feacture_cols——特征名
    输出：newData——DataFrame类型
    '''
    newData = data[feacture_cols]
    for var in feacture_cols:
        if newData[var].isnull().any() == True:
            newData[var+'_NA'] = newData[var].isnull()*1

    newData = newData.drop(feacture_cols,1)

    return newData