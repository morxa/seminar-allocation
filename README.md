# Topic Allocation

This is a small tool to assign students to a list of topics. Each student
provides a ranking for the topics, and the topics are assigned to the students
with the Household Allocation Algorithm.

## Usage
You need a file with a list of topics, and a ranking file for each student.
Check out the `examples` directory for the example files.
A topic file `topics.txt` may look like this:

```
Smith, Pell: Parachute use to prevent death and major trauma related to gravitational challenge: systematic review of randomised controlled trials
Wright: Academia Obscura: The hidden silly side of higher education
Cham, Whiteson: We have no idea
```

Each student ranking needs to contain

1. The name of the student in the first line
1. Each ranked topic on a separate line, with a preceeding rank.
   All topics not in the ranking file are assumed to have the last rank.

The ranking of Kenny McCormick may look like this:

```
Kenny McCormick
2 Smith, Pell: Parachute use to prevent death and major trauma related to gravitational challenge: systematic review of randomised controlled trials
2 Wright: Academia Obscura: The hidden silly side of higher education
1 Cham, Whiteson: We have no idea
```

Assume that we have the three topics above and the two students
_Kenny McCormick_ and _Homer Simpson_. As we have more topics and students, we
have an additional spare file `ranking_spare1.txt` with the placeholder name
_Spare 1_. If you have more topics than students, always prepare additional
spare rankings.

To compute the assignment, run:

    ./semal.py -t example/topics.txt example/ranking*txt

This will print one best assignment, e.g.,:

```
Kenny McCormick: Cham, Whiteson: We have no idea (Rank 1)
Homer Simpson: Smith, Pell: Parachute use to prevent death and major trauma related to gravitational challenge: systematic review of randomised controlled trials (Rank 1)
Spare 1: Wright: Academia Obscura: The hidden silly side of higher education (Rank 3)
```

### Ranking Algorithm
The algorithm randomly assigns one topic to each student and then swaps topics
until no further improvement is possible. This means:
* The absolute rank does not matter, e.g., instead of rank 2, Kenny could also
  assign rank 3 to the first two topics without any difference;
* A student can assign multiple topics to the same rank without any advantage
  or disadvantage
