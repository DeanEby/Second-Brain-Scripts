# Creates ngrams for a string passed
# input = text for analysis
# n = size of ngram to be made
def ngrams(input, n):
   # splits the input into a list
   input = input.split(' ')
   # define output dictionary
   output = {}
   # iterates over the input list without going out of bounds
   for i in range(len(input)-n+1):
       # creates an Ngram
       g = ' '.join(input[i:i+n])
       # Checks if there is a duplicate ngram already made
       # will not add it to the dict if it is a dupe
       output.setdefault(g, 0)
       output[g] += 1
   return output