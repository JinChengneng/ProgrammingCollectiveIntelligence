
from math import sqrt

# 初始化字典
critics={
 'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
}

#欧几里得距离评价
def euclidean_distance(prefs, person1, person2):
    sum_of_squares = sum( pow( (prefs[person1][item] - prefs[person2][item]) ,2 )
    for item in prefs[person1] if item in prefs[person2])
    
    return 1/(sqrt(sum_of_squares)  + 1)

# 皮尔逊相关度评价
def pearson_correlation_score(prefs, person1, person2):
    shared_items ={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            shared_items[item] = 1
            
    n = len(shared_items)
            
    if n == 0:
        return 0
    
    sum1 = sum(prefs[person1][item] for item in shared_items)
    sum2 = sum(prefs[person2][item] for item in shared_items)
    
    sum1Sq = sum(pow(prefs[person1][item],2) for item in shared_items)
    sum2Sq = sum(pow(prefs[person2][item],2) for item in shared_items)
    
    pSum = sum(prefs[person1][item] * prefs[person2][item] for item in shared_items)
    
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den == 0:
        return 0
    
    return num/den

# 为评论者打分
def topMatches(prefs, person, n=5, similarity=pearson_correlation_score):
    scores= [(similarity(prefs,person,other),other) for other in prefs if other!= person]
    
    scores.sort()
    scores.reverse()
    return scores[0:n]
    
# 推荐商品
def getRecommendations(prefs, person, similarity=pearson_correlation_score):
    totalScores = { }
    similaritySum = { }
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <=0 :
            continue
        
        for item in prefs[other]:
            if item not in prefs[person]:
                totalScores.setdefault(item,0)
                totalScores[item] += prefs[other][item] * sim
                similaritySum.setdefault(item,0)
                similaritySum[item] += sim
    
    ranking = [(total/similaritySum[item], item) for item,total in totalScores.items()]

    ranking.sort()
    ranking.reverse()
    return ranking

# 对字典进行倒置处理 
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person] = prefs[person][item]
    return result

# 基于用户的系统过来
print(getRecommendations(critics,'Toby'))

# 基于物品的协同过滤
movies = transformPrefs(critics)
print(topMatches(movies,'Superman Returns'))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
