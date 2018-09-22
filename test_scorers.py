import scorers

short_street_scorer = scorers.StreetScorer(4, "Short street", 30)
long_street_scorer = scorers.StreetScorer(5, "Long street", 40)

bad_throw = [1,6,3,4,4]
short_street_1 = [1,4,6,3,2]
short_street_2 = [6,6,3,5,4]
long_street_1 = [2,3,4,5,6]
long_street_2 = [2,3,1,5,4]

test_cases = [
    (short_street_scorer, bad_throw, 0),
    (long_street_scorer, bad_throw, 0),
    (short_street_scorer, short_street_1, 30),
    (long_street_scorer, short_street_1, 0),
    (short_street_scorer, short_street_2, 30),
    (long_street_scorer, short_street_2, 0),
    (short_street_scorer, long_street_1, 30),
    (long_street_scorer, long_street_1, 40),
    (short_street_scorer, long_street_2, 30),
    (long_street_scorer, long_street_2, 40)]

results = [scorer.ComputeScore(dice) == expected_result for
           (scorer, dice, expected_result) in test_cases]

for i, result in zip(range(len(results)),results):
  if result:
    print "Test case %d passed!" % i
  else:
    print "Test case %d failed :(" % i

    

