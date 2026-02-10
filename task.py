class StringHandler:
    def getString(self,word):
        self.word = word
    def printString(self):
        return self.word.upper()
s = StringHandler() 
s.getString(input())
print(s.printString())
