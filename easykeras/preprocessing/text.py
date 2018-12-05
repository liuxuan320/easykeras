#coding:utf-8

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

class TextProcessor():
    """文本预处理

    将文本（或词语序列）转换为定长词语编号序列
    或者词袋(Bag-Of-Word)编号序列

    Attributes:
        tokenizer: Keras自带的文本处理工具类
        has_dic: 是否已经生成词表
    """

    def __init__(self):
        """初始化文本预处理类"""
        self.tokenizer = Tokenizer()
        self.has_dic = False

    def get_vocabulary(self):
        """获取词表

        Returns:
            词表字典，将词语映射到词语编号。例如:

            {'I': 54,
            'love': 23,
            'Keras': 6}

            词语编号从1开始
        """
        if (not self.has_dic):
            print('请先调用 read_all_texts() 函数生成词表!')
            return None
        return self.tokenizer.word_index

    def get_words_num(self):
        """获取词语数量

        Returns:
            词表中的词语数量
        """
        if (not self.has_dic):
            print('请先调用 read_all_texts() 函数生成词表!')
            return 0
        return len(self.tokenizer.word_index)

    def read_all_texts(self, *texts):
        """浏览所有的文本

        对所有样例文本中的词语进行编号，建立词表

        Args:
            texts: 一个或多个文本列表，
                   每个元素可以是用空格分开的原始文本，
                   也可以是词语列表

        Returns:
            词表字典，将词语映射到词语编号。例如:

            {'I': 54,
            'love': 23,
            'Keras': 6}

            词语编号从1开始
        """
        list = []
        for text in texts:
            list.extend(text)
        if (len(list) == 0):
            print('传入文本为空!')
            return None
        self.tokenizer.fit_on_texts(list)
        self.has_dic = True
        return self.tokenizer.word_index
    
    def _process_text(self, texts, length):
        """处理文本"""
        # 词语字符串->词语编号列表
        sequences = self.tokenizer.texts_to_sequences(texts)
        # 统一长度
        return pad_sequences(sequences, maxlen=length)

    def _vectorize_sequences(self, texts, dimension):
        """词袋编号"""
        # 词语字符串->词语编号列表
        sequences = self.tokenizer.texts_to_sequences(texts)
        # 创建一个形状为(len(sequences), dimension)的零矩阵
        results = np.zeros((len(sequences), dimension))
        for i, sequence in enumerate(sequences):
            results[i, sequence] = 1. # 将results[i]的指定索引设为1
        return results

    def texts_to_num(self, length, *texts):
        """文本转换为数字编号序列

        将文本中的词语映射为对应的词语编号

        Args:
            length: 转换后的序列长度(词语数量)
                    超过截断，不足补零
            texts: 一个或多个文本列表，
                   每个元素可以是用空格分开的原始文本，
                   也可以是词语列表

        Returns:
            一个或多个转换后的二维数字矩阵。例如：

            ['a b c', 'a b', 'd'] -> [[2 1 3]
                                      [0 2 1]
                                      [0 0 4]]

            数字编号从1开始，不足在开头补0.
        """
        if (not self.has_dic):
            print('请先调用 read_all_texts() 函数生成词表!')
            return tuple([None for x in range(len(texts))])
        return tuple([self._process_text(x, length) for x in texts])

    def texts_to_bow(self, *texts):
        """文本转换为词袋编号序列

        将文本转换为词袋向量，长度为词表
        向量每一维对应一个词语，文本中出现为1，未出现为0

        Args:
            texts: 一个或多个文本列表，
                   每个元素可以是用空格分开的原始文本，
                   也可以是词语列表

        Returns:
            一个或多个转换后的二维矩阵。例如：

            ['a b c', 'a b', 'd'] -> [[0. 1. 1. 1. 0. 0.]
                                      [0. 1. 1. 0. 0. 0.]
                                      [0. 0. 0. 0. 1. 0.]]

            每一维对应一个词语，文本中出现为1，未出现为0
        """
        if (not self.has_dic):
            print('请先调用 read_all_texts() 函数生成词表!')
            return tuple([None for x in range(len(texts))])
        return tuple([self._vectorize_sequences(x, self.get_words_num()+1) for x in texts])
    
if __name__ == "__main__":
    texts_1 = ['中国 的 首都 是 北京', '北京 天安门', '中国']
    texts_2 = ['我 在 中国', '北京 是 中国 的 首都']
    # texts_1 = [['中国', '的', '首都', '是', '北京'], ['北京', '天安门'], ['中国']]
    # texts_2 = [['我', '在', '中国'], ['北京', '是', '中国', '的', '首都']]
    print('texts1:', texts_1)
    print('texts2:', texts_2)

    processor = TextProcessor() # 文本预处理器
    # 读取文本，生成词表
    processor.read_all_texts(texts_1, texts_2)
    print('词表大小:', processor.get_words_num())
    print('词表:', processor.get_vocabulary())
    # 文本转换为数字编号序列
    print('转换为数字序列(长度4)：')
    texts_1_num, texts_2_num = processor.texts_to_num(4, texts_1, texts_2)
    print('texts1:\n', texts_1_num)
    print('texts2:\n', texts_2_num)
    # 转换为词袋编号序列
    print('转换为词袋编号序列：')
    texts_1_bow, texts_2_bow = processor.texts_to_bow(texts_1, texts_2)
    print('texts1:\n', texts_1_bow)
    print('texts2:\n', texts_2_bow)
    