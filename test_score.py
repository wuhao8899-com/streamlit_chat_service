from nltk.translate.bleu_score import sentence_bleu
import jieba

def bleu_score(true_answer : str, generate_answer : str) -> float:
    # true_anser : 标准答案，str 类型
    # generate_answer : 模型生成答案，str 类型
    true_answers = list(jieba.cut(true_answer))
    # print(true_answers)
    generate_answers = list(jieba.cut(generate_answer))
    # print(generate_answers)
    bleu_score = sentence_bleu(true_answers, generate_answers)
    return bleu_score

true_answer = '周志华老师的《机器学习》（西瓜书）是机器学习领域的经典入门教材之一，周老师为了使尽可能多的读者通过西瓜书对机器学习有所了解, 所以在书中对部分公式的推导细节没有详述，但是这对那些想深究公式推导细节的读者来说可能“不太友好”，本书旨在对西瓜书里比较难理解的公式加以解析，以及对部分公式补充具体的推导细节。'

answer1 = '周志华老师的《机器学习》（西瓜书）是机器学习领域的经典入门教材之一，周老师为了使尽可能多的读者通过西瓜书对机器学习有所了解, 所以在书中对部分公式的推导细节没有详述，但是这对那些想深究公式推导细节的读者来说可能“不太友好”，本书旨在对西瓜书里比较难理解的公式加以解析，以及对部分公式补充具体的推导细节。'

