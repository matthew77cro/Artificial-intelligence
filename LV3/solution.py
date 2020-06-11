import sys
import copy
import math

class Node:
    def __init__(self, feature):
        self.feature = feature
        self.subtrees = dict()

class Leaf:
    def __init__(self, label):
        self.label = label

class CSVData:

    def __init__(self, csv_data = None):
        self.features = list()
        self.features_to_index = dict() # str -> int
        self.examples = list() # list of lists
        self.feature_values = dict() # int -> set of strings
        self.classes = set()

    def copy(self):
        csv = CSVData()

        csv.features = copy.deepcopy(self.features)
        csv.features_to_index = copy.deepcopy(self.features_to_index)
        csv.examples = copy.deepcopy(self.examples)
        csv.feature_values = copy.deepcopy(self.feature_values)
        csv.classes = copy.deepcopy(self.classes)

        return csv

class ID3:

    def __init__(self, cfg):
        self.cfg = cfg
        self.root = None

    def fit(self, csv_data):
        self.csv_data = csv_data
        self.root = self.id3alg(csv_data.copy(), csv_data.copy(), 0)

    def predict(self, csv_data):
        predictions = list()

        for example in csv_data.examples:
            next = self.root

            while(True):
                if(isinstance(next, Leaf)):
                    predictions.append(next.label)
                    break
                fv = example[csv_data.features_to_index[next.feature]]
                next = next.subtrees[fv]

        return predictions

    def id3alg(self, d, dparent, depth):
        if (not(self.cfg["max_depth"] == "-1") and depth >= int(self.cfg["max_depth"])):
            return Leaf(self.most_common_class_label(d))

        if (len(d.examples) == 0):
            label = self.most_common_class_label(dparent)
            return Leaf(label)
        label = self.most_common_class_label(d)
        if(len(d.features) == 0 or self.has_only_this_class_label(d, label)):
            return Leaf(label)
        x = self.most_discriminative_feature(d)
        n = Node(x)
        for v in d.feature_values[d.features_to_index[x]]:
            n.subtrees[v] = self.id3alg(self.isolate(d, x, v), d, depth + 1)
        return n

    def isolate(self, d, feature, value):
        id = int(d.features_to_index[feature])
        dnew = CSVData()

        for h in d.features:
            if (h == feature):
                continue
            dnew.features.append(h)

        dnew.features_to_index = dict()
        for i in range(0, len(dnew.features)):
            dnew.features_to_index[dnew.features[i]] = i

        dnew.feature_values = dict()
        for k, v in d.feature_values.items():
            if(d.features[k] == feature):
                continue
            dnew.feature_values[dnew.features_to_index[d.features[k]]] = v

        for example in d.examples:
            if (example[id] != value):
                continue
            examplenew = list()
            for i in range(0, len(example)):
                if(i==id):
                    continue
                examplenew.append(example[i])
            dnew.examples.append(examplenew)

        dnew.classes = copy.deepcopy(d.classes)

        return dnew

    def informational_gain(self, d):
        ig = dict() # feature -> ig
        counter = self.count_class_labels_for_features(d)

        for feature, dic in counter.items():
            ig_value = 0

            count_by_class = dict()
            count_total = 0

            for c in d.classes:
                count_by_class[c] = 0

            for feature_value, dic2 in dic.items():
                for c, count in dic2.items():
                    count_by_class[c] += count
                    count_total += count

            entropy = 0
            for k, v in count_by_class.items():
                if(not(v == 0)):
                    entropy += v / count_total * math.log2(v / count_total)
            entropy = -1 * entropy

            ig_value = entropy
            for feature_value, dic2 in dic.items():
                count_by_feature_value = 0
                entropy_feature_value = 0
                for c, count in dic2.items():
                    count_by_feature_value += count
                for c, count in dic2.items():
                    if(not(count == 0)):
                        entropy_feature_value += count / count_by_feature_value * math.log2(count / count_by_feature_value)
                entropy_feature_value = -1 * entropy_feature_value

                ig_value -= count_by_feature_value / count_total * entropy_feature_value

            ig[feature] = ig_value

        return ig

    def most_common_class_label(self, d):
        counter = dict()
        mccl_count = 0
        mccl = str()

        for v in d.examples:
            if(v[-1] not in counter):
                counter[v[-1]] = 1
                continue
            counter[v[-1]] += 1

        for k, v in counter.items():
            if(v > mccl_count):
                mccl = k
                mccl_count = v

        return mccl

    def most_discriminative_feature(self, d):
        ig_values = self.informational_gain(d)
        
        max_ig = -1
        max_ig_feature = None

        for k, v in ig_values.items():
            if (v > max_ig):
                max_ig_feature = k
                max_ig = v

        return max_ig_feature

    def count_class_labels_for_features(self, d):
        counter = dict() # feature -> (feature_value -> (class_label -> count))

        for f in d.features:
            if (f == d.features[-1]):
                continue
            counter[f] = dict()
            for fv in d.feature_values[d.features_to_index[f]]:
                counter[f][fv] = dict()
                for c in d.classes:
                    counter[f][fv][c] = 0

        for example in d.examples:
            for i in range(0, len(example) - 1):
                counter[d.features[i]][example[i]][example[-1]] += 1

        return counter

    def has_only_this_class_label(self, d, label):
        for example in d.examples:
            if(not(example[-1] == label)):
                return False

        return True

default_cfg = {"max_depth" : "-1", "num_trees" : "1", "feature_ratio" : "1.", "example_ratio" : "1."}

def load_csv(filename):
    file = open(filename, 'r')

    csv = CSVData()
    firstLine = True
    for line in file:
        line = str(line).strip()
        linelist = line.split(',')
        if (firstLine):
            csv.features = linelist
            for i in range(0, len(linelist)):
                csv.features_to_index[linelist[i]] = i
                csv.feature_values[i] = set()
            firstLine = False
            continue
        for i in range(0, len(linelist)):
            csv.feature_values[i].add(linelist[i])
        csv.examples.append(linelist)
        csv.classes.add(linelist[-1])

    file.close()
    return csv

def load_cfg(filename):
    global default_cfg

    file = open(filename, 'r')

    cfg = dict()
    for line in file:
        line = str(line).strip().split("=")
        cfg[line[0]] = line[1]

    for k, v in default_cfg.items():
        if (k not in cfg):
            cfg[k] = v

    file.close()
    return cfg

def main():
    argc = len(sys.argv)
    argv = sys.argv

    fit_data = load_csv(argv[1])
    test_data = load_csv(argv[2])
    config = load_cfg(argv[3])

    id3 = ID3(config)
    id3.fit(fit_data)

    # Print tree BFS
    next = list()
    next.append((0, id3.root))
    first = True
    while(not(len(next) == 0)):
        depth, n = next[0]
        del next[0]
        if(first):
            print(str(depth) + ":" + n.feature, end = '')
            first = False
        else:
            print(", " + str(depth) + ":" + n.feature, end = '')
        for k, v in n.subtrees.items():
            if(isinstance(v, Leaf)):
                continue
            next.append((depth + 1, v))

    print()
    predictions = id3.predict(test_data)
    for p in predictions:
        print(p + " ", end='')

    print()

    # accuracy
    correct = 0

    for i in range(0, len(test_data.examples)):
        if(predictions[i] == test_data.examples[i][-1]):
            correct += 1

    print(correct/len(test_data.examples))

    # error matrix
    matrix = list()

    # init matrix
    for i in range(0, len(test_data.classes)):
        matrix.append([0] * len(test_data.classes))

    c = list(fit_data.classes)
    c.sort()

    for i in range(0, len(test_data.examples)):
        matrix[c.index(test_data.examples[i][-1], 0, len(c))][c.index(predictions[i], 0, len(c))] += 1

    for i in range(0, len(test_data.classes)):
        for j in range(0, len(test_data.classes)):
            print(str(matrix[i][j]), end=' ')
        print()

main()