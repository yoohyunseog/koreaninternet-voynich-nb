# -*- coding: utf-8 -*-
"""
다국어 단어 데이터베이스
여러 언어의 단어들을 관리
"""

# 언어별 단어 데이터베이스
LANGUAGE_DATABASE = {
    '영어': [
        # Nature & Elements
        'sky', 'earth', 'sea', 'ocean', 'mountain', 'hill', 'valley', 'river', 'stream', 'lake',
        'tree', 'forest', 'wood', 'branch', 'leaf', 'root', 'bark', 'flower', 'petal', 'seed',
        'grass', 'herb', 'weed', 'moss', 'fern', 'vine', 'bush', 'shrub',
        'stone', 'rock', 'crystal', 'mineral', 'metal', 'iron', 'gold', 'silver', 'copper', 'bronze',
        'water', 'rain', 'dew', 'mist', 'fog', 'cloud', 'storm', 'thunder', 'lightning', 'tempest',
        'fire', 'flame', 'ember', 'ash', 'smoke', 'spark', 'blaze', 'inferno',
        'wind', 'breeze', 'gale', 'air', 'breath', 'gust', 'whirlwind',
        'snow', 'ice', 'frost', 'hail', 'sleet', 'glacier',
        'sun', 'moon', 'star', 'planet', 'comet', 'meteor', 'constellation',
        'light', 'shadow', 'darkness', 'dawn', 'dusk', 'twilight', 'noon', 'midnight',
        'soil', 'sand', 'clay', 'mud', 'dust', 'dirt', 'gravel',
        
        # Animals
        'horse', 'mare', 'stallion', 'foal', 'pony', 'donkey', 'mule',
        'cow', 'bull', 'calf', 'ox', 'buffalo', 'bison',
        'sheep', 'lamb', 'ram', 'ewe', 'goat', 'kid', 'billy',
        'pig', 'boar', 'sow', 'hog', 'swine', 'piglet',
        'dog', 'hound', 'pup', 'puppy', 'wolf', 'fox', 'jackal', 'coyote',
        'cat', 'kitten', 'lion', 'tiger', 'leopard', 'panther', 'lynx', 'cheetah',
        'bear', 'deer', 'elk', 'moose', 'stag', 'doe', 'fawn', 'reindeer',
        'bird', 'eagle', 'hawk', 'falcon', 'owl', 'crow', 'raven', 'dove', 'swan', 'duck', 'goose',
        'parrot', 'peacock', 'sparrow', 'robin', 'wren', 'thrush', 'lark', 'nightingale',
        'fish', 'salmon', 'trout', 'carp', 'pike', 'eel', 'bass', 'perch', 'sturgeon',
        'whale', 'dolphin', 'shark', 'ray', 'octopus', 'squid', 'crab', 'lobster', 'shrimp',
        'snake', 'serpent', 'viper', 'cobra', 'python', 'adder', 'asp', 'rattlesnake',
        'dragon', 'wyvern', 'basilisk', 'phoenix', 'griffin', 'unicorn', 'pegasus',
        'bee', 'wasp', 'ant', 'spider', 'moth', 'butterfly', 'beetle', 'dragonfly', 'cricket',
        'frog', 'toad', 'lizard', 'turtle', 'tortoise', 'crocodile', 'alligator',
        'rabbit', 'hare', 'mouse', 'rat', 'squirrel', 'beaver', 'otter', 'badger', 'weasel',
        
        # Plants & Herbs
        'rose', 'lily', 'lotus', 'orchid', 'violet', 'iris', 'tulip', 'daisy', 'poppy', 'lavender',
        'jasmine', 'chrysanthemum', 'carnation', 'magnolia', 'peony', 'dahlia', 'hydrangea',
        'pine', 'oak', 'elm', 'ash', 'birch', 'maple', 'willow', 'cedar', 'cypress', 'yew',
        'bamboo', 'palm', 'fir', 'spruce', 'hazel', 'alder', 'beech', 'chestnut',
        'ginkgo', 'cherry', 'plum', 'peach', 'apple', 'pear', 'fig', 'olive', 'date',
        'sage', 'thyme', 'basil', 'mint', 'parsley', 'rosemary', 'oregano', 'dill', 'coriander',
        'chamomile', 'valerian', 'yarrow', 'dandelion', 'nettle', 'clover', 'thistle',
        'ginger', 'garlic', 'onion', 'leek', 'fennel', 'anise', 'cumin', 'saffron',
        'aloe', 'cactus', 'ivy', 'mistletoe', 'holly', 'heather', 'wisteria', 'azalea',
        'marigold', 'sunflower', 'hibiscus', 'gardenia', 'camellia', 'begonia', 'zinnia',
        'petunia', 'pansy', 'snapdragon', 'foxglove', 'bluebell', 'bellflower', 'snowdrop',
        'buttercup', 'primrose', 'anemone', 'ranunculus', 'geranium', 'tansy', 'verbena',
        'mugwort', 'wormwood', 'comfrey', 'sorrel', 'borage', 'plantain', 'chicory',
        'marjoram', 'savory', 'tarragon', 'lemongrass', 'bay', 'laurel', 'juniper',
        'larch', 'sequoia', 'redwood', 'sycamore', 'poplar', 'hawthorn', 'rowan',
        'elder', 'elderberry', 'mulberry', 'blackberry', 'raspberry', 'strawberry',
        'blueberry', 'cranberry', 'currant', 'gooseberry', 'pomegranate', 'apricot',
        'quince', 'persimmon', 'melon', 'cucumber', 'gourd', 'squash', 'pumpkin',
        'yam', 'turnip', 'radish', 'carrot', 'beet', 'celery', 'spinach', 'lettuce',
        'cabbage', 'kale', 'arugula', 'parsnip',
        
        # Body Parts
        'head', 'skull', 'brain', 'face', 'forehead', 'temple', 'cheek', 'jaw', 'chin',
        'eye', 'eyebrow', 'eyelash', 'eyelid', 'pupil', 'iris', 'retina', 'cornea',
        'ear', 'lobe', 'nose', 'nostril', 'mouth', 'lip', 'tongue', 'tooth', 'teeth', 'gum', 'palate',
        'neck', 'throat', 'shoulder', 'arm', 'elbow', 'wrist', 'hand', 'finger', 'thumb', 'palm', 'fist',
        'chest', 'breast', 'bosom', 'rib', 'spine', 'back', 'waist', 'hip', 'belly', 'navel', 'abdomen',
        'leg', 'thigh', 'knee', 'calf', 'shin', 'ankle', 'foot', 'heel', 'toe', 'sole',
        'heart', 'lung', 'liver', 'kidney', 'spleen', 'stomach', 'intestine', 'bladder', 'womb',
        'blood', 'vein', 'artery', 'pulse', 'bone', 'marrow', 'cartilage', 'tendon', 'muscle', 'nerve',
        'skin', 'flesh', 'hair', 'nail', 'sweat', 'tear', 'saliva',
        
        # Abstract & Emotions
        'love', 'hate', 'fear', 'anger', 'rage', 'wrath', 'fury', 'ire',
        'joy', 'happiness', 'pleasure', 'delight', 'bliss', 'ecstasy', 'rapture',
        'sadness', 'sorrow', 'grief', 'misery', 'melancholy', 'despair', 'anguish',
        'hope', 'faith', 'trust', 'belief', 'doubt', 'skepticism', 'certainty',
        'peace', 'calm', 'tranquility', 'serenity', 'harmony', 'balance',
        'war', 'battle', 'conflict', 'strife', 'combat', 'struggle', 'fight',
        'freedom', 'liberty', 'justice', 'truth', 'wisdom', 'knowledge', 'understanding', 'enlightenment',
        'power', 'strength', 'force', 'might', 'energy', 'vigor', 'potency',
        'courage', 'bravery', 'valor', 'honor', 'glory', 'pride', 'dignity',
        'beauty', 'grace', 'elegance', 'charm', 'splendor', 'magnificence',
        'good', 'evil', 'virtue', 'vice', 'sin', 'righteousness', 'wickedness',
        'life', 'death', 'birth', 'rebirth', 'resurrection', 'mortality', 'immortality',
        'time', 'eternity', 'infinity', 'fate', 'destiny', 'fortune', 'luck', 'chance',
        'dream', 'vision', 'prophecy', 'omen', 'sign', 'miracle', 'wonder',
        'soul', 'spirit', 'essence', 'being', 'existence', 'consciousness',
        'mind', 'thought', 'memory', 'reason', 'intellect', 'wisdom',
        
        # Actions & Verbs
        'walk', 'run', 'leap', 'jump', 'climb', 'crawl', 'creep', 'slide', 'slip', 'stride',
        'stand', 'sit', 'lie', 'kneel', 'bow', 'bend', 'stretch', 'reach', 'squat',
        'see', 'look', 'watch', 'gaze', 'stare', 'glance', 'peer', 'observe', 'behold', 'witness',
        'hear', 'listen', 'heed', 'attend', 'hearken',
        'speak', 'talk', 'say', 'tell', 'whisper', 'shout', 'cry', 'call', 'sing', 'chant', 'utter',
        'eat', 'drink', 'taste', 'swallow', 'chew', 'bite', 'devour', 'feast', 'dine',
        'sleep', 'wake', 'rest', 'slumber', 'doze', 'dream', 'snore',
        'work', 'labor', 'toil', 'serve', 'obey', 'command', 'rule', 'reign', 'govern',
        'make', 'create', 'build', 'forge', 'craft', 'shape', 'form', 'mold', 'fashion',
        'destroy', 'break', 'shatter', 'crush', 'ruin', 'demolish', 'wreck', 'smash',
        'give', 'take', 'receive', 'offer', 'grant', 'bestow', 'donate', 'present',
        'hold', 'grasp', 'grip', 'clutch', 'seize', 'catch', 'grab', 'release', 'drop',
        'open', 'close', 'shut', 'lock', 'unlock', 'seal', 'bind', 'tie', 'untie', 'fasten',
        'cut', 'slice', 'chop', 'split', 'cleave', 'sever', 'divide', 'separate',
        'heal', 'cure', 'mend', 'restore', 'revive', 'renew', 'repair', 'remedy',
        'hurt', 'harm', 'wound', 'injure', 'damage', 'pain', 'ache', 'suffer',
        'teach', 'learn', 'study', 'read', 'write', 'draw', 'paint', 'inscribe',
        'think', 'know', 'understand', 'realize', 'recognize', 'remember', 'recall', 'forget',
        'feel', 'sense', 'perceive', 'experience', 'touch',
        'want', 'desire', 'wish', 'crave', 'yearn', 'long', 'covet',
        'need', 'require', 'demand', 'seek', 'search', 'find', 'discover', 'locate',
        'grow', 'increase', 'expand', 'swell', 'rise', 'ascend', 'mount', 'soar',
        'shrink', 'decrease', 'diminish', 'wane', 'fall', 'descend', 'sink', 'decline',
        'begin', 'start', 'commence', 'initiate', 'originate', 'launch',
        'end', 'finish', 'complete', 'conclude', 'cease', 'stop', 'halt', 'terminate',
        'change', 'transform', 'convert', 'alter', 'modify', 'shift', 'vary',
        'move', 'travel', 'journey', 'wander', 'roam', 'drift', 'migrate',
        'come', 'go', 'arrive', 'depart', 'leave', 'enter', 'exit', 'pass', 'proceed',
        'follow', 'lead', 'guide', 'direct', 'show', 'point', 'indicate',
        'hide', 'conceal', 'cover', 'veil', 'mask', 'reveal', 'expose', 'uncover', 'unveil',
        'protect', 'guard', 'defend', 'shield', 'shelter', 'safeguard',
        'attack', 'assault', 'strike', 'hit', 'smite', 'beat', 'punch',
        'kill', 'slay', 'murder', 'execute', 'sacrifice', 'slaughter',
        'live', 'exist', 'survive', 'endure', 'persist', 'remain', 'stay', 'dwell',
        'die', 'perish', 'expire', 'decay', 'rot', 'wither', 'fade', 'vanish',
        'burn', 'ignite', 'kindle', 'blaze', 'scorch', 'char', 'singe',
        'flow', 'stream', 'pour', 'gush', 'drip', 'leak', 'trickle',
        'shine', 'glow', 'gleam', 'glitter', 'sparkle', 'flash', 'glimmer',
        
        # Time & Seasons
        'morning', 'morn', 'dawn', 'sunrise', 'daybreak', 'aurora',
        'noon', 'midday', 'afternoon', 'evening', 'dusk', 'sunset', 'twilight',
        'night', 'midnight', 'nocturne',
        'day', 'today', 'yesterday', 'tomorrow', 'week', 'month', 'year', 'decade', 'century',
        'spring', 'summer', 'autumn', 'fall', 'winter', 'season',
        'era', 'epoch', 'age', 'period', 'cycle', 'phase',
        'moment', 'instant', 'second', 'minute', 'hour',
        'past', 'present', 'future', 'eternity', 'forever', 'eternal', 'everlasting',
        
        # Direction & Position
        'up', 'down', 'above', 'below', 'over', 'under', 'beneath', 'underneath',
        'front', 'back', 'fore', 'rear', 'behind', 'ahead', 'forward', 'backward',
        'left', 'right', 'side', 'lateral',
        'inside', 'outside', 'within', 'without', 'interior', 'exterior',
        'center', 'middle', 'midst', 'core', 'heart',
        'top', 'bottom', 'summit', 'peak', 'apex', 'base', 'foundation',
        'edge', 'border', 'boundary', 'limit', 'margin', 'rim', 'brink', 'verge',
        'corner', 'angle', 'point', 'tip', 'end',
        'near', 'far', 'close', 'distant', 'remote', 'adjacent',
        'north', 'south', 'east', 'west',
        
        # Human & Society
        'human', 'person', 'people', 'man', 'woman', 'child', 'infant', 'baby',
        'boy', 'girl', 'youth', 'maiden', 'lad', 'lass',
        'adult', 'elder', 'ancient', 'ancestor', 'descendant', 'offspring',
        'father', 'mother', 'parent', 'son', 'daughter', 'brother', 'sister', 'sibling',
        'family', 'kin', 'kindred', 'clan', 'tribe', 'race', 'nation', 'people',
        'friend', 'companion', 'comrade', 'ally', 'partner', 'mate',
        'enemy', 'foe', 'rival', 'adversary', 'opponent',
        'stranger', 'guest', 'visitor', 'traveler', 'wanderer', 'pilgrim',
        'king', 'queen', 'prince', 'princess', 'lord', 'lady', 'noble', 'knight', 'duke',
        'priest', 'monk', 'nun', 'bishop', 'pope', 'clergy', 'abbot', 'friar',
        'wizard', 'witch', 'sorcerer', 'mage', 'sage', 'prophet', 'oracle', 'seer', 'mystic',
        'healer', 'physician', 'doctor', 'surgeon', 'apothecary', 'herbalist',
        'warrior', 'soldier', 'fighter', 'champion', 'hero', 'knight', 'guard',
        'merchant', 'trader', 'seller', 'buyer', 'customer', 'vendor',
        'smith', 'carpenter', 'mason', 'farmer', 'shepherd', 'hunter', 'fisher', 'miller',
        'servant', 'slave', 'master', 'lord', 'ruler', 'sovereign', 'emperor',
        'teacher', 'student', 'scholar', 'scribe', 'writer', 'poet', 'artist', 'painter',
        
        # Objects & Tools
        'book', 'scroll', 'tome', 'manuscript', 'page', 'letter', 'word', 'text', 'document',
        'pen', 'quill', 'ink', 'pencil', 'chalk', 'brush', 'stylus',
        'sword', 'blade', 'knife', 'dagger', 'spear', 'lance', 'arrow', 'bow', 'axe', 'mace',
        'shield', 'armor', 'helmet', 'mail', 'plate', 'gauntlet', 'breastplate',
        'staff', 'rod', 'wand', 'scepter', 'crown', 'ring', 'amulet', 'talisman', 'charm',
        'cup', 'chalice', 'goblet', 'bowl', 'plate', 'dish', 'pot', 'jar', 'vase', 'flask',
        'bottle', 'barrel', 'cask', 'chest', 'box', 'casket', 'coffer', 'trunk',
        'key', 'lock', 'chain', 'rope', 'cord', 'thread', 'string', 'wire', 'cable',
        'stone', 'gem', 'jewel', 'pearl', 'diamond', 'ruby', 'emerald', 'sapphire', 'amethyst',
        'coin', 'gold', 'silver', 'treasure', 'wealth', 'riches', 'fortune',
        'cloth', 'fabric', 'silk', 'wool', 'linen', 'cotton', 'leather', 'hide',
        'garment', 'robe', 'cloak', 'mantle', 'tunic', 'dress', 'gown', 'shirt', 'coat', 'vest',
        'shoe', 'boot', 'sandal', 'slipper',
        'house', 'home', 'dwelling', 'hall', 'chamber', 'room', 'tower', 'castle', 'palace', 'temple',
        'door', 'gate', 'portal', 'entrance', 'exit', 'window', 'wall', 'floor', 'ceiling', 'roof',
        'path', 'road', 'way', 'route', 'trail', 'lane', 'street', 'avenue',
        'bridge', 'ford', 'crossing', 'pass', 'gate',
        'ship', 'boat', 'vessel', 'craft', 'bark', 'galley', 'barge', 'ferry',
        'wheel', 'axle', 'cart', 'wagon', 'carriage', 'chariot',
        'table', 'chair', 'throne', 'seat', 'bench', 'bed', 'couch', 'stool',
        'lamp', 'torch', 'candle', 'lantern', 'beacon', 'brazier',
        'mirror', 'glass', 'lens', 'crystal', 'prism',
        'bell', 'horn', 'drum', 'flute', 'lyre', 'harp', 'lute', 'pipe',
        
        # Medicine & Alchemy
        'poison', 'venom', 'toxin', 'antidote', 'remedy', 'cure', 'medicine', 'drug', 'potion',
        'elixir', 'tincture', 'salve', 'ointment', 'balm', 'unguent', 'lotion',
        'disease', 'illness', 'sickness', 'plague', 'pestilence', 'fever', 'pain', 'ache', 'malady',
        'health', 'wellness', 'vitality', 'vigor', 'strength',
        'essence', 'extract', 'powder', 'dust', 'ash',
        
        # Medieval Medicine & Herbalism
        'bloodletting', 'venesection', 'phlebotomy', 'leeches', 'lancet', 'scalpel',
        'humors', 'phlegm', 'cholera', 'melancholia', 'sanguine',
        'purgation', 'purgative', 'cathartic', 'emetic', 'laxative',
        'diuretic', 'sudorific', 'demulcent', 'astringent', 'expectorant',
        'apothecary', 'herbalist', 'alchemist', 'physician', 'leech', 'surgeon',
        'mortar', 'pestle', 'alembic', 'crucible', 'retort', 'distillation',
        'pharmacopoeia', 'materia', 'officinalis', 'simples', 'compound',
        'bloodstone', 'touchstone', 'bezaars', 'unicorn', 'mithridates',
        'theriac', 'diascordium', 'laudanum', 'aqua', 'spiritus',
        'gall', 'myrrh', 'frankincense', 'benzoin', 'mastic', 'turpentine',
        'borax', 'vitriol', 'saltpeter', 'cinnabar', 'realgar',
        'opium', 'senna', 'rhubarb', 'castor', 'mercury', 'quicksilver',
        
        # Alchemy & Metals
        'aurum', 'argentum', 'sulfur', 'mercury', 'arsenic', 'antimony',
        'copper', 'tin', 'lead', 'zinc', 'iron', 'bronze',
        'calcination', 'dissolution', 'separation', 'conjunction', 'fermentation', 'distillation',
        'sublimation', 'coagulation', 'putrefaction', 'mortification', 'multiplication',
        'transmutation', 'quintessence', 'philosopher', 'stone', 'elixir',
        'alchemist', 'adept', 'magus', 'hermetic', 'cabalistic',
        
        # Zodiac & Astrology
        'zodiac', 'astrology', 'planetary', 'celestial', 'astral',
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces',
        'jupiter', 'mars', 'saturn', 'venus', 'mercury', 'apollo', 'lunar', 'solar',
        'horoscope', 'aspect', 'conjunction', 'opposition', 'trine', 'square',
        'ascendant', 'descendant', 'midheaven', 'nadir', 'cusp',
        
        # Bathing & Humoral Therapy
        'bath', 'bathhouse', 'bathing', 'ablution', 'immersion', 'submersion',
        'hot', 'warm', 'lukewarm', 'cold', 'ice', 'thermal', 'steam',
        'spring', 'bath', 'basin', 'tub', 'vessel', 'receptacle',
        'water', 'mineral', 'sulfur', 'salt', 'spring', 'well', 'source',
        'vapor', 'stream', 'smoke', 'exhalation',
        'complexion', 'temperament', 'constitution', 'balance', 'equilibrium',
        'heat', 'moisture', 'dryness', 'coldness', 'quality',
        
        # Mystical & Religious
        'god', 'goddess', 'deity', 'divine', 'holy', 'sacred', 'blessed', 'sanctified',
        'angel', 'demon', 'devil', 'spirit', 'ghost', 'phantom', 'specter',
        'prayer', 'blessing', 'curse', 'spell', 'incantation', 'ritual', 'ceremony',
        'altar', 'shrine', 'temple', 'church', 'monastery', 'abbey',
        'heaven', 'hell', 'paradise', 'purgatory', 'underworld', 'abyss',
        'magic', 'sorcery', 'witchcraft', 'enchantment', 'charm',
        
        # Common Words
        'the', 'a', 'an', 'this', 'that', 'these', 'those',
        'and', 'or', 'but', 'nor', 'yet', 'so', 'for',
        'of', 'in', 'on', 'at', 'to', 'from', 'by', 'with', 'without',
        'if', 'when', 'where', 'why', 'how', 'who', 'what', 'which',
        'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'done',
        'can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must',
        'not', 'no', 'yes', 'all', 'some', 'any', 'each', 'every', 'none',
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
        'first', 'second', 'third', 'last', 'next', 'final',
        'very', 'much', 'many', 'more', 'most', 'less', 'least', 'few', 'little',
        'great', 'small', 'large', 'huge', 'tiny', 'vast', 'immense',
        'good', 'bad', 'better', 'worse', 'best', 'worst',
        'new', 'old', 'young', 'ancient', 'modern', 'fresh', 'stale',
        'hot', 'cold', 'warm', 'cool', 'burning', 'freezing',
        'wet', 'dry', 'moist', 'damp', 'arid',
        'hard', 'soft', 'rough', 'smooth', 'sharp', 'dull', 'blunt',
        'heavy', 'light', 'dense', 'thin', 'thick',
        'high', 'low', 'tall', 'short', 'long', 'deep', 'shallow',
        'wide', 'narrow', 'broad', 'slim', 'fat', 'lean',
        'fast', 'slow', 'quick', 'swift', 'rapid', 'sluggish',
        'strong', 'weak', 'powerful', 'feeble', 'mighty', 'frail',
        'loud', 'quiet', 'silent', 'noisy', 'still',
        'bright', 'dark', 'dim', 'pale', 'vivid', 'dull',
        'clear', 'cloudy', 'opaque', 'transparent', 'obscure',
        'clean', 'dirty', 'pure', 'impure', 'foul', 'pristine',
        'true', 'false', 'real', 'fake', 'genuine', 'counterfeit',
        'whole', 'half', 'part', 'piece', 'fragment', 'portion',
        'full', 'empty', 'filled', 'void', 'vacant',
        'alive', 'dead', 'living', 'dying', 'mortal', 'immortal',
        'sacred', 'holy', 'divine', 'blessed', 'cursed', 'profane',
        'secret', 'hidden', 'revealed', 'obvious', 'manifest',
        'strange', 'odd', 'weird', 'peculiar', 'curious', 'normal', 'ordinary',
    ],
}

# 언어 설명
LANGUAGE_INFO = {
    '영어': 'English - 1000+ words: nature, medicine, alchemy, mysticism, medieval vocabulary',
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
