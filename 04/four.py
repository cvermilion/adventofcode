#!/usr/bin/env python3

with open("input.txt") as f:
    phrases = f.read().splitlines()

def has_no_dupe(phrase):
    words = phrase.split()
    return len(words) == len(set(words))

def has_no_anagram(phrase):
    words = phrase.split()
    words = ["".join(sorted(w)) for w in words]
    return len(words) == len(set(words))

print("Part 1: {:d}", len(list(filter(has_no_dupe, phrases))))
print("Part 2: {:d}", len(list(filter(has_no_anagram, phrases))))
