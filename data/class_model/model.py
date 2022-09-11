import numpy as np
import argparse
import pickle
import os
class Model:
    grams = {}
    grams1 = {}

    def __getstate__(self) -> dict:
        state = {}
        state["grams"] = self.grams
        state["grams1"] = self.grams1
        return state

    def __setstate__(self, state: dict):
        self.grams = state["grams"]
        self.grams1 = state["grams1"]

    def fit(self, n=3, input_dir="stdin"):
        if input_dir == "stdin":
            a = []
            s = input().split()
            for i in range(len(s)):
                fl = 0
                s[i] = s[i].lower()
                if s[i][-1] == '.' or s[i][-1] == '!' or s[i][-1] == '?':
                    fl = 1
                    s[i] = s[i][:-1]
                if s[i][-1] == ',':
                    s[i] = s[i][:-1]
                if len(a) < n:
                    a.append(s[i])
                else:
                    a.pop(0)
                    a.append(s[i])
                if len(a) == n:
                    if self.grams.get(" ".join(a[:-1])) is None:
                        self.grams[" ".join(a[:-1])] = {}
                    if self.grams[" ".join(a[:-1])].get(a[-1]) is None:
                        self.grams[" ".join(a[:-1])][a[-1]] = 0

                    self.grams[" ".join(a[:-1])][a[-1]] += 1
                if fl:
                    a = []
        else:
            os.chdir(input_dir)
            for dirpath, dirnames, filenames in os.walk(os.getcwd()):

                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    if len(filename) >= 4 and filename[len(filename) - 3:] == "pkl":
                        continue
                    file = open(path, "r", encoding='utf-8')
                    a = []
                    try:
                        s = file.read().split()
                    except UnicodeDecodeError:
                        file.close()
                        try:
                            file = open(path, "r", encoding='utf-16')
                            s = file.read().split()
                        except UnicodeDecodeError:
                            file = open(path, "r", encoding='ansi')
                            s = file.read().split()
                    for i in range(len(s)):
                        fl = 0
                        s[i] = s[i].lower()
                        if s[i][-1] == '.' or s[i][-1] == '!' or s[i][-1] == '?':
                            fl = 1
                            s[i] = s[i][:-1]
                        if len(s[i]) and (s[i][-1] == ',' or s[i][-1] == '"' or s[i][-1] == "»"):
                            s[i] = s[i][:-1]
                        if len(s[i]) and (s[i][0] == '"' or s[i][0] == "«"):
                            s[i] = s[i][1:]
                        if len(a) < n:
                            a.append(s[i])
                        else:
                            a.pop(0)
                            a.append(s[i])
                        if len(a) == n:
                            if self.grams.get(" ".join(a[:-1])) is None:
                                self.grams[" ".join(a[:-1])] = {}
                            if self.grams[" ".join(a[:-1])].get(a[-1]) is None:
                                self.grams[" ".join(a[:-1])][a[-1]] = 0
                            self.grams[" ".join(a[:-1])][a[-1]] += 1
                            if self.grams1.get(a[-2]) is None:
                                self.grams1[a[-2]] = {}
                            if self.grams1[a[-2]].get(a[-1]) is None:
                                self.grams1[a[-2]][a[-1]] = 0
                            self.grams1[a[-2]][a[-1]] += 1

                        if fl:
                            a = []
                    file.close()
        for pref in self.grams:
            sm = 0
            for nxt in self.grams[pref]:
                sm += self.grams[pref][nxt]
            for nxt in self.grams[pref]:
                self.grams[pref][nxt] /= sm
        for pref in self.grams1:
            sm = 0
            for nxt in self.grams1[pref]:
                sm += self.grams1[pref][nxt]
            for nxt in self.grams1[pref]:
                self.grams1[pref][nxt] /= sm

    def generate(self, pref="", length=1, n=2):
        pref = pref.split()
        for i in range(len(pref)):
            pref[i] = pref[i].lower()
            if pref[i][-1] == '.' or pref[i][-1] == '!' or pref[i][-1] == '?':
                pref[i] = pref[i][:-1]
            if pref[i][-1] == ',':
                pref[i] = pref[i][:-1]
        for i in range(length):
            if len(pref) < n - 1:
                if len(pref) > 0 and self.grams1.get(pref[-1]) is not None:
                    nxt = list(self.grams1[pref[-1]].keys())[
                        np.random.choice(len(list(self.grams1[pref[-1]].keys())),
                                         p=list(self.grams1[pref[-1]].values()))]
                    pref.append(nxt)
                else:
                    nxt = list(self.grams1.keys())[
                        np.random.choice(len(list(self.grams1.keys())))]
                    pref.append(nxt)
            else:
                s = pref[len(pref) - n + 1]
                for j in range(len(pref) - n + 2, len(pref)):
                    s = s + " " + pref[j]
                if self.grams.get(s) is not None:
                    nxt = list(self.grams[s].keys())[
                        np.random.choice(len(list(self.grams[s].keys())), p=list(self.grams[s].values()))]
                    pref.append(nxt)
                elif self.grams1.get(pref[-1]) is not None:
                    nxt = list(self.grams1[pref[-1]].keys())[
                        np.random.choice(len(list(self.grams1[pref[-1]].keys())),
                                         p=list(self.grams1[pref[-1]].values()))]
                    pref.append(nxt)
                else:
                    nxt = list(self.grams1.keys())[
                        np.random.choice(len(list(self.grams1.keys())))]
                    pref[-1] = pref[-1] + ','
                    pref.append(nxt)
        return pref

