# -*- coding: utf-8 -*-
"""
다국어 단어 데이터베이스
여러 언어의 단어들을 관리
"""

# 언어별 단어 데이터베이스
LANGUAGE_DATABASE = {
    '한국어': [
        # 자연
        '하늘', '땅', '바다', '산', '강', '나무', '꽃', '풀', '돌', '물',
        '불', '바람', '구름', '비', '눈', '해', '달', '별', '빛', '그림자',
        
        # 식물
        '장미', '백합', '국화', '민들레', '해바라기', '난초', '연꽃', '매화',
        '소나무', '대나무', '버들', '단풍나무', '은행나무',
        
        # 동물
        '말', '소', '양', '돼지', '개', '고양이', '새', '물고기', '뱀', '용',
        
        # 신체
        '머리', '눈', '귀', '코', '입', '손', '발', '심장', '피', '뼈',
        
        # 감정/상태
        '사랑', '기쁨', '슬픔', '분노', '두려움', '평화', '행복', '고통',
        
        # 기본 동사
        '가다', '오다', '보다', '듣다', '말하다', '먹다', '마시다', '자다',
        
        # 숫자
        '하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉', '열',
    ],
    
    '영어': [
        # Nature
        'sky', 'earth', 'sea', 'mountain', 'river', 'tree', 'flower', 'grass', 'stone', 'water',
        'fire', 'wind', 'cloud', 'rain', 'snow', 'sun', 'moon', 'star', 'light', 'shadow',
        
        # Plants
        'rose', 'lily', 'chrysanthemum', 'dandelion', 'sunflower', 'orchid', 'lotus',
        'pine', 'bamboo', 'willow', 'maple', 'ginkgo',
        
        # Animals
        'horse', 'cow', 'sheep', 'pig', 'dog', 'cat', 'bird', 'fish', 'snake', 'dragon',
        
        # Body
        'head', 'eye', 'ear', 'nose', 'mouth', 'hand', 'foot', 'heart', 'blood', 'bone',
        
        # Emotions
        'love', 'joy', 'sadness', 'anger', 'fear', 'peace', 'happiness', 'pain',
        
        # Verbs
        'go', 'come', 'see', 'hear', 'speak', 'eat', 'drink', 'sleep',
        
        # Numbers
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    ],
    
    '라틴어': [
        # Natura
        'caelum', 'terra', 'mare', 'mons', 'flumen', 'arbor', 'flos', 'herba', 'lapis', 'aqua',
        'ignis', 'ventus', 'nubes', 'pluvia', 'nix', 'sol', 'luna', 'stella', 'lux', 'umbra',
        
        # Plantae
        'rosa', 'lilium', 'pinus', 'quercus', 'salix',
        
        # Animalia
        'equus', 'bos', 'ovis', 'porcus', 'canis', 'felis', 'avis', 'piscis', 'serpens', 'draco',
        
        # Corpus
        'caput', 'oculus', 'auris', 'nasus', 'os', 'manus', 'pes', 'cor', 'sanguis', 'os',
        
        # Affectus
        'amor', 'gaudium', 'tristitia', 'ira', 'timor', 'pax', 'felicitas', 'dolor',
        
        # Verba
        'ire', 'venire', 'videre', 'audire', 'dicere', 'edere', 'bibere', 'dormire',
        
        # Numeri
        'unus', 'duo', 'tres', 'quattuor', 'quinque', 'sex', 'septem', 'octo', 'novem', 'decem',
    ],
    
    '그리스어': [
        'ouranos', 'ge', 'thalassa', 'oros', 'potamos', 'dendron', 'anthos', 'chloe', 'lithos', 'hudor',
        'pyr', 'anemos', 'nephos', 'huetos', 'chion', 'helios', 'selene', 'aster', 'phos', 'skia',
        'hippos', 'bous', 'probaton', 'hus', 'kuon', 'ailouros', 'ornis', 'ichthus', 'ophis', 'drakon',
        'kephale', 'ophthalmos', 'ous', 'rhis', 'stoma', 'cheir', 'pous', 'kardia', 'haima', 'osteon',
        'agape', 'chara', 'lupe', 'orge', 'phobos', 'eirene', 'eudaimonia', 'algos',
    ],
    
    '아랍어': [
        'sama', 'ard', 'bahr', 'jabal', 'nahr', 'shajara', 'zahra', 'hashish', 'hajar', 'maa',
        'nar', 'rih', 'sahab', 'matar', 'thalj', 'shams', 'qamar', 'najm', 'nur', 'zill',
        'hisan', 'baqara', 'kharuf', 'khinzir', 'kalb', 'qitt', 'tayr', 'samak', 'hayyah', 'tinnin',
        'ras', 'ayn', 'udhun', 'anf', 'fam', 'yad', 'qadam', 'qalb', 'dam', 'azm',
        'hubb', 'farah', 'huzn', 'ghadab', 'khawf', 'salam', 'saada', 'alam',
    ],
    
    '히브리어': [
        'shamayim', 'eretz', 'yam', 'har', 'nahar', 'etz', 'perach', 'esev', 'even', 'mayim',
        'esh', 'ruach', 'anan', 'geshem', 'sheleg', 'shemesh', 'yareach', 'kochav', 'or', 'tzel',
        'sus', 'shor', 'seh', 'chazir', 'kelev', 'chatul', 'tzipor', 'dag', 'nachash', 'tanin',
        'rosh', 'ayin', 'ozen', 'af', 'peh', 'yad', 'regel', 'lev', 'dam', 'etzem',
        'ahava', 'simcha', 'atzuv', 'kaas', 'pachad', 'shalom', 'osher', 'keev',
    ],
}

# 언어 설명
LANGUAGE_INFO = {
    '한국어': '한국어 (Korean) - 동아시아 언어',
    '영어': 'English - 게르만어파',
    '라틴어': 'Latin - 고대 로마 언어, 식물학/의학 용어',
    '그리스어': 'Greek - 고대 그리스, 철학/과학 용어',
    '아랍어': 'Arabic - 중동 언어, 연금술 용어',
    '히브리어': 'Hebrew - 고대 히브리, 신비주의 용어',
}

def get_all_languages():
    """모든 언어 목록 반환"""
    return list(LANGUAGE_DATABASE.keys())

def get_words_by_language(language):
    """특정 언어의 단어들 반환"""
    return LANGUAGE_DATABASE.get(language, [])

def get_all_words():
    """모든 언어의 모든 단어 반환"""
    all_words = []
    for language, words in LANGUAGE_DATABASE.items():
        all_words.extend([(language, word) for word in words])
    return all_words

def get_language_count():
    """언어 수 반환"""
    return len(LANGUAGE_DATABASE)

def get_total_word_count():
    """전체 단어 수 반환"""
    return sum(len(words) for words in LANGUAGE_DATABASE.values())
