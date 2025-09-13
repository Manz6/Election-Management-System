Election Management System
Project Overview:

This project is a menu-driven Election Management System that simulates how candidates, voters, and election results are managed. It combines Binary Search Tree (BST), Graph, and Tree data structures to handle different parts of the system.

Features:

1) Candidate Registration (BST)
Stores candidates in a Binary Search Tree using Aadhaar as a key.
Ensures eligibility (Aadhaar = 12 digits, age ≥ 25, must be a voter).
Allows searching candidates by Aadhaar.

2) Voter Registration (Dictionary)
Registers voters with a unique voter ID (state + district + random digits).
Prevents duplicate registrations.
Ensures only eligible voters (age ≥ 18)
Tracks whether a voter has already voted.

3) Booth Allocation (Graph)
Graph structure connects residents and polling booths.
Dijkstra’s algorithm (heapq) finds the shortest path to allocate the nearest booth.

4)Voting (Tree)
Hierarchical tree structure (National → States → Districts).
Each district stores votes for parties (BJP, Congress, Communist).
Aggregates results upward to state and national level.

5)Menu System
Candidate Registration
Voter Registration & Booth Allocation
Voting
Display Results (leaf to root traversal)
Exit

Data Structures Used:

Binary Search Tree (BST) → Candidate management.
Dictionary (Hash Map) → Voter database.
Graph → Polling booth allocation (shortest path).
Tree → Election result aggregation.

How to Run:

Make sure you have Python 3 installed.
Save the code in a file, e.g., election_system.py.

Run the program:
python election_system.py
Follow the menu options to register candidates, register voters, vote, and view results.

Example Flow:

Register a candidate with Aadhaar.
Register voters with state/district codes.
Allocate booths using graph connections.
Cast votes for parties.
Display results from district → state → national.
