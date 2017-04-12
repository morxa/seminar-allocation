#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#  Created:  Wed 12 Apr 2017 09:11:44 CEST
#  Copyright  2017  Till Hofmann <hofmann@kbsg.rwth-aachen.de>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Library General Public License for more details.
#
#  Read the full text in the LICENSE.GPL file in the doc directory.

"""
Seminar allocation
"""

import argparse
import random
import re

class Error(Exception):
    """ Base class for errors in this module. """
    pass
class NoImprovementPossibleError(Error):
    """ The given assignment cannot be improved. """
    pass

class Student(object):
    """ A student with a topic ranking and optionally a topic assignment. """
    def __init__(self, ranking_file, topic_list):
        """ Initialize the student from the given ranking file.

        The file's first line is expected to be the student's name, the
        following lines are expected to be a ranking of the form:
        <rank1> <topic1>
        <rank2> <topic2>

        Args:
            ranking_file: A file object with the studen't ranking
            topic_list: A list of valid topic names
        """
        lines = ranking_file.readlines()
        assert(len(lines) > 0), \
                'Ranking file {} is empty'.format(ranking_file.name)
        self.name = lines[0].strip()
        self.ranking = {}
        # Default rank is the lowest rank possible.
        for topic in topic_list:
            self.ranking[topic] = len(topic_list)
        for line in lines[1:]:
            match = re.match(pattern='(\d+)\s+(.*)$', string=line)
            assert len(match.groups()) == 2
            rank = int(match.groups()[0])
            topic = match.groups()[1]
            assert topic in topic_list, \
                    '{} has invalid topic: {}'.format(self.name, topic)
            self.ranking[topic] = rank
    def __str__(self):
        return 'Student: {}\nRanking: {}'.format(self.name, self.ranking)
    def __repr__(self):
        return self.name

class Allocator(object):
    """ Computes a topic allocation. """
    def __init__(self, topics, students):
        """ Initialize the allocator with the given list of Students.
        Args:
            topics: A list of topics
            students: A list of Student objects
        """
        self.topics = topics
        self.students = students
    def assign(self):
        """ Compute the best topic allocation. """
        random_assignment_indices = list(range(len(self.topics)))
        random.shuffle(random_assignment_indices)
        assignment = {}
        for i in range(len(self.students)):
            assignment[self.students[i]] = \
                self.topics[random_assignment_indices[i]]
        while True:
            try:
                assignment = self.improve_assignment(assignment)
            except NoImprovementPossibleError:
                break
        return assignment


    def improve_assignment(self, assignment):
        """ Improves the given assignment with household allocation.

        The assignment is improved by finding a pair of students who prefer the
        other student's topic over their own topic.

        Throw an exception if the assignment cannot be improved.

        Args:
            assignment: A Dictionary of assignments (key: student, value: topic).
        Returns:
            The improved assignment.
        """
        students = assignment.keys()
        # Shuffle students so we don't prefer students at the beginning.
        random.shuffle(students)
        for s1 in students:
            t1 = assignment[s1]
            for s2 in students:
                if s1 == s2:
                    continue
                t2 = assignment[s2]
                if (s1.ranking[t1] > s1.ranking[t2]
                    and s2.ranking[t2] >= s2.ranking[t1]):
                    assignment[s1] = t2
                    assignment[s2] = t1
                    return assignment
        raise NoImprovementPossibleError

def get_topics(topic_file):
    """ Get a list of topics from a file. """
    return [ line.strip() for line in topic_file.readlines() ]

def main():
    """ Main function.

    Parses command line arguments and calls the allocator.
    """
    parser = argparse.ArgumentParser(
        description='Seminar slot allocation using the household allocation '
                    'algorithm.')
    parser.add_argument('-t', '--topic-file', type=argparse.FileType('r'),
                        help='a file containing a list of topics, one per line')
    parser.add_argument('student_rankings', nargs='+',
                        metavar='student_ranking',
                        type=argparse.FileType('r'),
                        help="a file with the ranking of a single student, "
                             "first line is the student's name")
    args = parser.parse_args()
    topics = get_topics(args.topic_file)
    students = []
    for ranking in args.student_rankings:
        students.append(Student(ranking, topics))
    assert(len(topics) >= len(students))
    allocator = Allocator(topics, students)
    assignment = allocator.assign()
    keys = assignment.keys()
    keys.sort()
    for student in keys:
        topic = assignment[student]
        print('{}: {} (Rank {})'.format(
            student.name, topic, student.ranking[topic]))

if __name__ == '__main__':
    main()
