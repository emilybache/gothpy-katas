##
## ChainBox game implementation

class ChainBox(object):
    def __init__(self):
        """
        This is a Python implementation of a board game called ChainBox. I don't
        where this game comes from, who has invented it or whether or not you
        can play it somewhere online. The first I heard of it was in the Nokia
        coder's competition IOI 2001. Unfortunately, all material seems more or
        less lost. If you know, or know someone that knows something about this
        game, please send me an e-mail (johan@pulp.se).

        The rules are very simple.        0000000000   Fig.2
        When the game starts, the board   0000000000   0000000000
        looks like figure 1.              0000000000   0000120000
                                          0000000000   0002211000 <- Here is the
        A 0 indicates an empty square. A  0000120000   0000211000 <- "box"
        1 or 2 indicate player one and    0000210000   0000000000
        two respectively.                 0000000000
                                          0000000000   NOTE! I've trimmed the
        Each player takes turns placing   0000000000   board slightly in height.
        a marker in an empty square on    0000000000   The five missing rows all
        the board.                             Fig.1   contain only zeros.
        
        If a player manages to place 4 markers in a box pattern, he/she wins. A
        box for player 1 is shown in figure 2.

        If no player manages to form a box before the board becomes full. The
        winner is whoever has the longest chain of connected markers on the
        board. A chain can begin and end anywhere on the board. A marker is
        connected to all markers of the same value in it's neighbourhood. Apart
        from positions on the edge and in the corners, all positions have 8
        other positions in their neighbourhoods.
        """

        self.width =  10
        self.height = 10
        self.new_game()

    def new_game(self):
        """
        Initialize the board for a new game.
        """

        self.board = {}

    def place_marker(self, player, position):
        """
        Places a marker for 'player' in 'position' and returns True or returns
        False if 'player' and/or 'position' specifies an invalid move.
        """

        assert player in [1,2]
        assert position[0] in range(10)
        assert position[1] in range(10)

        if position in self.board.keys():
            return False
        
        self.board[position] = player
        return True

    def is_game_over(self):
        """
        Returns -1 if the game is still in play. 0 indicates that the game is
        over, but tied. 1 and 2 indicates that player one and two respectively
        have won the game.
        
        NOTE! This method (currently) doesn't care about "how" you win. It
        returns the same values if you've won with a box as if you've won with
        the longest chain.

        >>> c = ChainBox()
        >>> c.place_marker(1,(3,3))
        True
        >>> c.place_marker(1,(3,4))
        True
        >>> c.place_marker(1,(4,3))
        True
        >>> c.is_game_over()
        -1
        >>> c.place_marker(1,(4,4))
        True
        >>> c.is_game_over()
        1
        """

        # This checks whether or not the board is full...
        if len(self.board.values()) == 100 and \
           0 not in self.board.values():
            # TBD!
            return 0 # 0 indicates a tie but in fact, we should find the longest
                     # "chain" of markers on the board to decide the winner.

        # If it's not full. We check for boxes
        else:
            for x in range(self.width-1):
                for y in range(self.height-1):
                    slice = self._slice((x,y), (2,2))
                    if 0 not in slice[0] and 0 not in slice[1]:
                        # is this slice a box?
                        if slice[0][0] == slice[0][1] and \
                           slice[0][1] == slice[1][0] and \
                           slice[1][0] == slice[1][1]:
                            return slice[0][0] # winner

        return -1 # game is not over

    def _slice(self, position, dimension):
        """
        Returns a part of the board as specified by 'position' and 'dimension'.

        >>> c = ChainBox()

        This cuts out a 2x2 slice of the board (as a nested list) counting from
        position: 1,1

        >>> c._slice((1,1), (2,2))
        [[0, 0], [0, 0]]
        >>> c.place_marker(1,(1,1))
        True
        >>> c.place_marker(2,(2,2))
        True
        >>> c._slice((1,1), (2,2))
        [[1, 0], [0, 2]]

        You're not allowed to go outside the board so

        >>> c.place_marker(1,(9,9))
        True
        >>> c._slice((9,9), (1,1))
        [[1]]

        is fine, but

        >>> c._slice((9,9), (2,2))
        Traceback (most recent call last):
        ...
        AssertionError

        is not!
        """
        assert dimension[0]+ position[0] <= self.width
        assert dimension[1]+ position[1] <= self.height

        result = []
        for h in range(dimension[1]):
            temp = []
            for w in range(dimension[0]):
                try:
                    temp.append(self.board[(position[0]+w,position[1]+h)])
                except KeyError:
                    temp.append(0)

            result.append(temp)
        return result
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
