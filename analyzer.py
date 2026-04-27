import re
from collections import Counter

def analyze_comments(comments_data):
    buy_keywords = ['beli', 'order', 'checkout', 'pengen beli', 'mau beli', 'pesan', 'co', 'pay', 'ambil', 'mau dong', 'bungkus', 'ready']
    positive_keywords = ['bagus', 'keren', 'lucu', 'menarik', 'mantap', 'suka', 'kece', 'gokil', 'rekomendasi']
    negative_keywords = ['jelek', 'mahal', 'kecewa', 'buruk', 'penipu', 'bohong', 'parah', 'gak banget', 'nyesel']
    question_keywords = ['?', 'berapa', 'dimana', 'gimana', 'cara', 'apa', 'kapan', 'lokasi', 'harga']

    results = []
    category_counts = {
        'Positif Ingin Beli': 0,
        'Positif Tidak Beli': 0,
        'Negatif': 0,
        'Pertanyaan': 0
    }
    
    all_words = []

    for text in comments_data:
        text_lower = text.lower()
        
        # Count keyword matches
        buy_matches = sum(1 for kw in buy_keywords if kw in text_lower)
        pos_matches = sum(1 for kw in positive_keywords if kw in text_lower)
        neg_matches = sum(1 for kw in negative_keywords if kw in text_lower)
        q_matches = sum(1 for kw in question_keywords if kw in text_lower)
        
        total_matches = buy_matches + pos_matches + neg_matches + q_matches
        
        # Classification
        category = 'Positif Tidak Beli'
        
        if q_matches > 0:
            category = 'Pertanyaan'
        elif neg_matches > 0:
            category = 'Negatif'
        elif buy_matches > 0:
            category = 'Positif Ingin Beli'
        elif pos_matches > 0:
            category = 'Positif Tidak Beli'
        else:
            category = 'Positif Tidak Beli' # default fallback
            
        category_counts[category] += 1
        
        # Confidence score (simulated based on match density)
        words = re.findall(r'\w+', text_lower)
        all_words.extend([w for w in words if len(w) > 3])
        
        confidence = 0
        if total_matches > 0:
            confidence = min(100, (total_matches / max(1, len(words) // 5)) * 100)
            if confidence < 50:
                confidence = 50 + confidence # baseline 50% if matched
        else:
            confidence = 40 # low confidence if no keywords matched
            
        results.append({
            'text': text,
            'category': category,
            'confidence': round(min(100, confidence))
        })

    # Word count for insight
    word_counts = Counter(all_words)
    stop_words = {'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'untuk', 'pada', 'dengan', 'aku', 'kamu', 'dia', 'kita', 'buat', 'ada', 'juga', 'aja'}
    top_words = [word for word, count in word_counts.most_common() if word not in stop_words][:5]

    total_comments = len(comments_data)
    
    conversion_rate = (category_counts['Positif Ingin Beli'] / total_comments) if total_comments > 0 else 0
    opportunity_rate = (category_counts['Pertanyaan'] / total_comments) if total_comments > 0 else 0

    return {
        'comments': results,
        'analytics': {
            'total': total_comments,
            'categories': category_counts,
            'conversion_rate': conversion_rate,
            'opportunity_rate': opportunity_rate
        },
        'top_keywords': top_words
    }
