class rulesets:

    mr = None

    def __init__(self, mr):
        self.mr = mr

    # https://en.wikipedia.org/wiki/Nelson_rules
    def nelson_rules(self):
        #   Rule 1
        # 	One point is more than 3σ from the mean.
        #   One sample is out of control.
        #
        #   Rule 2
        #   Nine (or more) points in a row are on the same side of the mean.
        #	Some prolonged bias exists.
        #
        #   Rule 3
        #   Six (or more) points in a row are continually increasing (or decreasing).
        #   A trend exists.
        #
        #   Rule 4
        #   Fourteen (or more) points in a row alternate in direction, increasing then decreasing.
        #   This much oscillation is beyond noise. Note that the rule is concerned with directionality only. The position of the mean and the size of the standard deviation have no bearing.
        #
        #   Rule 5
        #   Two (or three) out of three points in a row are more than 2σ from the mean in the same direction.
        #   There is a medium tendency for samples to be mediumly out of control.The position of the third point is unspecified.
        #
        #   Rule 6
        #   Four (or five) out of five points in a row are more than 1σ from the mean in the same direction.
        #   There is a strong tendency for samples to be slightly out of control. The position of the fifth point is unspecified.
        #
        #   Rule 7
        #   Fifteen points in a row are all within 1σ of the mean on either side of the mean.
        #   With 1σ, greater variation would be expected.
        #
        #   Rule 8
        #   Eight points in a row exist, but none within 1σ of the mean, and the points are in both directions from the mean.
        #   Jumping from above to below whilst missing the 1σ band is rarely random.
        return "not implemented"
        
    # https://en.wikipedia.org/wiki/Western_Electric_rules
    def western_electic_rules(self):
        #   Rule 1
        #   Any single data point falls outside the 3σ-limit from the mean
        #
        #   Rule 2
        # 	Two out of three consecutive points fall beyond the 2σ-limit, on the same side of the mean
        #
        #   Rule 3
        #   Four out of five consecutive points fall beyond the 1σ-limit, on the same side of the mean
        #
        #   Rule 4
        #   Eight consecutive points fall on the same side of the mean
        return "not implemented"

    def basic_rules(self):
        violations = { }
        #   Rule 1
        #   Any single data point falls outside the 3σ-limit from the mean
        rule1 = []
        bins = self.mr.individuals_bins()
        for item in range(len(bins)):
            if bins[item] > 3 or bins[item] < -3:
                rule1.append(item)
        violations['Rule 1'] = rule1

        #   Rule 2
        #   Seven consecutive points fall on the same side of the mean
        samples = 7
        rule2 = []
        sides = self.mr.individuals_sides()
        rolling = [0] * samples
        for item in range(len(sides)):
            rolling.append(sides[item])
            rolling = rolling[1:]
            if abs(sum(rolling)) == samples:
                for index in range(samples):
                    rule2.append(item - index + 1)
        violations['Rule 2'] = sorted(list(set(rule2)))

        return violations