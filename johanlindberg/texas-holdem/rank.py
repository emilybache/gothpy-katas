### Texas Hold'Em

# Poker Hand Rankings:
# -------------------
# 1. Royal Flush: A, K, Q, J, 10 all of the same suit
# 2. Straight Flush: Any five card sequence in the same suit (Ex: 4, 5, 6, 7, 8)
# 3. Four of a Kind: All four cards of the same index (Ex: Q, Q, Q, Q)
# 4. Full House: Three of a kind combined with a pair (Ex: K, K, 3, 3, 3)
# 5. Flush: Any five cards of the same suit, but not in sequence
# 6. Straight: Five cards in sequence, but not in the same suit  
# 7. Three of a Kind: Three cards of the same index
# 8. Two Pair: Two separate pairs (Ex: Q, Q, 7, 7)
# 9. Pair: Two cards of the same index
# 10. High Card:

# faces and suits
T, J, Q, K, A = 10, 'Jack', 'Queen', 'King', 'Ace'
c, d, h, s = 'Clubs', 'Diamonds', 'Hearts', 'Spades'

def generate_ranks():
    result = {}

    suits = [c, d, h, s]
    faces = [A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A]
    Jack, Queen, King, Ace = 11, 12, 13, 14

    # all high-cards:
    for face in faces[1:]:
        key = [face]
        result[str(key)] = (10+ eval(str(face)), 'High Card: %s' % (eval(str(face)))) 
    
    # all pairs
    for face in faces[1:]:
        key = [face, face]
        result[str(key)] = (9, 'Pair')

    # all two pairs
    for pface in faces[1:]:
        for tface in faces[:-1]:
            if pface != tface:
                if pface < tface:
                    key = [pface, pface, tface, tface]
                else:
                    key = [tface, tface, pface, pface]
            result[str(key)] = (8, 'Two Pairs')

    # all three of a kinds
    for face in faces[1:]:
        key = [face, face, face]
        result[str(key)] = (7, 'Three of a Kind')

    # all straights
    for f in range(len(faces)- 4):
        key = [faces[f], faces[f+1], faces[f+2], faces[f+3], faces[f+4]]
        result[str(key)] = (6, 'Straight')

    # all flushes
    for suit in suits:
        key = [suit, suit, suit, suit, suit]
        result[str(key)] = (5, 'Flush')

    # all full houses
    for pface in faces[1:]:
        for tface in faces[:-1]:
            if pface != tface:
                if pface < tface:
                    key = [pface, pface, tface, tface, tface]
                else:
                    key = [tface, tface, pface, pface, pface]
            result[str(key)] = (4, 'Full House')

    # all four of a kinds
    for face in faces[1:]:
        key = [face, face, face, face]
        result[str(key)] = (3, 'Four of a Kind')

    # all straight flushes
    for suit in suits:
        for f in range(len(faces)- 4):
            key = [(faces[f], suit), (faces[f+1], suit), (faces[f+2], suit), (faces[f+3], suit), (faces[f+4], suit)]
            result[str(key)] = (2, 'Straight Flush')

    # all royal flushes
    for suit in suits:
        key = [(T, suit), (J, suit), (Q, suit), (K, suit), (A, suit)]
        result[str(key)] = (1, 'Royal Flush')   

    return result

ranks = generate_ranks()

def read_hands_from_file(filename):
    result = []

    f = open(filename)
    for line in f.readlines():
        org = []
        hand = []
        for card in line.split():
            org.append(card)
            hand.append((eval(card[0]), eval(card[1])))
                        
        result.append([hand, org])
            
    f.close()
    return result

def rank(filename):
    hands = read_hands_from_file(filename)
    results = {}
    for hand, org in hands:
        if len(hand) == 7:
            rank, explanation = 100, None
            both = sorted(hand, key = lambda card: card[0])
            face = sorted([card[0] for card in hand])
            suit = sorted([card[1] for card in hand])
            for size in range(5):
                for start in range(len(hand) - size):
                    for dictionary in [both, face, suit]:
                        try:
                            key = str([dictionary[start + i] for i in range(size + 1)])
                            if ranks[key][0] < rank:
                                rank, explanation = ranks[key]

                        except KeyError:
                            pass
                
                        results[' '.join(org)] = rank, explanation
        else:
            results[' '.join(org)] = 100, 'Fold'

    return results

def print_score(filename):
    ranks = rank(filename)
    winner = None
    for hand, value in sorted(ranks.iteritems(), key = lambda (k,v): (v,k)):
        print hand, "=>", value[1],
        if winner is None or winner == value:
            winner = value
            print "*"
        else:
            print

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        print_score(sys.argv[-1])

    else:
        print "Usage: [python] rank.py <filename>"
        sys.exit(1)
    
