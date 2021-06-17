import glob
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from janome.tokenizer import Tokenizer


def load_sauna_text():
    category = {
        'yunoizumi': 1,
        'meguminoyu': 2,
        'rainbow-motoyawata': 3,
        'yulax': 4,
        'mabashi-yu': 5,
    }

    docs = []
    labels = []

    for c_name, c_id in category.items():
        files = glob.glob(
            "./text/{c_name}/*.txt".format(c_name=c_name))

        text = ''
        for file in files:
            with open(file, 'r', errors='ignore') as f:
                lines = f.read().splitlines()

                text="".join(lines)
                
            docs.append(text)
            labels.append(c_id)

    return docs, labels


docs, labels = load_sauna_text()

# indices は0からドキュメントの数までの整数をランダムに並べ替えた配列
random.seed()
indices = list(range(len(docs)))
# 9割をトレーニングデータとする
separate_num = int(len(docs) * 0.9)

random.shuffle(indices)

train_data = [docs[i] for i in indices[0:separate_num]]
train_labels = [labels[i] for i in indices[0:separate_num]]
test_data = [docs[i] for i in indices[separate_num:]]
test_labels = [labels[i] for i in indices[separate_num:]]

# テキストを分割する関数
t = Tokenizer()

def tokenize1(text):
    tokens = t.tokenize(",".join(text))
    noun = []
    for token in tokens:
        noun.append(token.surface)
    return noun


# Tf-idfを用いてtrain_dataをベクトル化してください
vectorizer = TfidfVectorizer(tokenizer=tokenize1)
train_matrix = vectorizer.fit_transform(train_data)

# ナイーブベイズを用いて分類をおこなってください。
clf = MultinomialNB()
clf.fit(train_matrix, train_labels)

# ランダムフォレストを用いて分類をおこなってください
clf2 = RandomForestClassifier(n_estimators=100)
clf2.fit(train_matrix, train_labels)

# テストデータを変換
test_matrix = vectorizer.transform(test_data)

# 分類結果を表示
print(clf.score(train_matrix, train_labels))
print(clf.score(test_matrix, test_labels))
print(clf2.score(train_matrix, train_labels))
print(clf2.score(test_matrix, test_labels))

# 単語の抽出
def tokenize2(text):
    tokens = t.tokenize(text)
    noun = []
    for token in tokens:
        # 「名詞」「動詞」「形容詞」「形容動詞」を取り出してください
        partOfSpeech = token.part_of_speech.split(',')[0]

        if partOfSpeech == '名詞':
            noun.append(token.surface)
        if partOfSpeech == '動詞':
            noun.append(token.surface)
        if partOfSpeech == '形容詞':
            noun.append(token.surface)
        if partOfSpeech == '形容動詞':
            noun.append(token.surface)
    return noun


# 単語の抽出して学習
t = Tokenizer()
vectorizer = TfidfVectorizer(tokenizer=tokenize2)
train_matrix = vectorizer.fit_transform(train_data)
test_matrix = vectorizer.transform(test_data)
clf.fit(train_matrix, train_labels)
clf2.fit(train_matrix, train_labels)

# 結果を表示
print(clf.score(train_matrix, train_labels))
print(clf.score(test_matrix, test_labels))
print(clf2.score(train_matrix, train_labels))
print(clf2.score(test_matrix, test_labels))