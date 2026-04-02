class Square():
    def __init__(self, valA,valB,valC,valD,A,B,C,D):
        # values
        self.valA = valA
        self.valB = valB
        self.valC = valC
        self.valD = valD

        # coordinates
        self.A = A
        self.B = B
        self.C = C 
        self.D = D

    
    def getSquareID(self, thr):
        idx = 0
        if self.valA > thr: idx |= 1
        if self.valB > thr: idx |= 2 
        if self.valC > thr: idx |= 4  
        if self.valD > thr: idx |= 8  
        return idx
    
    def getSegments(self, squareID):
        pX = pY = qX = qY = 0.0
        
        # Midpoints of the four edges
        bottom = ((self.A[0] + self.B[0]) / 2, self.A[1])
        right  = (self.B[0], (self.B[1] + self.C[1]) / 2)
        top    = ((self.D[0] + self.C[0]) / 2, self.D[1])
        left   = (self.A[0], (self.A[1] + self.D[1]) / 2)

        if squareID in (0, 15):
            return pX, pY, qX, qY

        elif squareID in (1, 14): # Bottom-Left corner
            pX, pY = bottom
            qX, qY = left

        elif squareID in (2, 13): # Bottom-Right corner
            pX, pY = bottom
            qX, qY = right

        elif squareID in (4, 11): # Top-Right corner
            pX, pY = right
            qX, qY = top

        elif squareID in (8, 7):  # Top-Left corner
            pX, pY = left
            qX, qY = top

        elif squareID in (3, 12): # Bottom half vs Top half
            pX, pY = left
            qX, qY = right

        elif squareID in (6, 9):  # Right half vs Left half
            pX, pY = bottom
            qX, qY = top

        # elif squareID == 5: # Saddle Case 1 (Diagonal BL & TR)
        #     # Note: Usually returns TWO segments, simplified here to one
        #     pX, pY = bottom
        #     qX, qY = right # (And technically top to left)

        # elif squareID == 10: # Saddle Case 2 (Diagonal BR & TL)
        #     pX, pY = bottom
        #     qX, qY = left  # (And technically top to right)

        return pX, pY, qX, qY
    
    
