import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)	

# return appropriate N that satisfies the error bounds
def findN(eps,m):
	# For an m-bit pattern, the max value of f(p) is less than 26^m
	# If the algorithm outputs a false match, then a mod q = b mod q where a and b are hash values of text and pattern
	# Hence it follows q divides |a-b| and the number of prime factors is less than log(26^m) = mlog26 --- all base 2 from CLAIM 1
	# Clearly, if the total number of primes is Z, then probability of a false output is mlog26/Z 
	# We need mlog26/Z < eps
	# Hence, Z > mlog26/eps
	# From CLAIM 2, we have Z > N/2logN
	# Hence the suitable N can be found as N/2logN > (mlog26)/eps -> N > (2mlog26)/eps


	# Our N is such that
	# N/math.log2(N) > 2*m*math.log2(26)/eps = k
	# Since (N**(1/2))>logN we have (N/logN)>(N**(1/2)). So if we take N=ceil(((2*m*log26)/(eps))**2) it will satisfy the inequality.
	k = 2*m*math.log(26,2)//eps
	N = k^2+1
	return N

# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
	# Time Complexity: O((m+n)logq)
	# Working Memory: O(k+logn+logq)

	Out = []
	fpp, fpx = 0, 0
	alpha = pow(26,len(p),q)

	# O(m logq)
	for i in range(0, len(p)):								# Computing Initial fp Values
		fpp += (pow(26, len(p)-i-1,q) *((ord(p[i])-65) %q) %q)
		fpx += (pow(26, len(p)-i-1,q) *((ord(x[i])-65) %q) %q)
	fpp = fpp % q
	fpx = fpx % q
	if (fpp == fpx): Out.append(0)

	# O(n logq)
	for j in range(len(p), len(x)):
		fpx = ((26 %q)*fpx %q) - ((alpha)*((ord(x[j-len(p)])-65) %q) %q) + ((ord(x[j])-65) %q)
		fpx = fpx % q
		if (fpp == fpx): Out.append(j-len(p)+1)
	return Out
		
# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
	# Time Complexity: O((m+n)logq)
	# Working Memory: O(k+logn+logq)
	
	Out = []
	fpp1, fpp2, fpx1, fpx2 = 0, 0, 0, 0
	k_ind = 0

	# O(m logq)
	for i in range(0, len(p)):						# Computing Initial fp Values
		if (p[i]) == "?":
			fpp1 = fpp2
			fpp2 = 0
			fpx1 = fpx2
			fpx2 = 0
			k_ind = i										# Length Of Sub-pattern before '?'
		else:
			fpp2 += (pow(26, len(p)-i-1,q)*((ord(p[i])-65) %q))%q
			fpx2 += (pow(26, len(p)-i-1,q)*((ord(x[i])-65) %q))%q
	fpp1 = fpp1 % q
	fpx1 = fpx1 % q
	fpp2 = fpp2 % q
	fpx2 = fpx2 % q
	if (fpp1 == fpx1 and fpp2 == fpx2): Out.append(0)

	# O(n logq)
	for j in range(len(p), len(x)):
		fpx1 = ((26 %q)*fpx1)%q - (pow(26, len(p),q)*((ord(x[j-len(p)])-65) %q) %q) + (pow(26, len(p)-k_ind,q)*((ord(x[j-len(p)+k_ind])-65) %q) %q)
		fpx2 = ((26 %q)*fpx2)%q - (pow(26, len(p)-k_ind-1,q)*((ord(x[j-len(p)+k_ind+1])-65) %q) %q) + ((ord(x[j])-65) %q)
		fpx1 = fpx1 %q
		fpx2 = fpx2 %q
		if ((fpp1 + fpp2) %q == (fpx1 + fpx2) %q): Out.append(j-len(p)+1)
	return Out