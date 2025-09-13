import random
import heapq

class Candidate:
    def __init__(self, aadhar, name, party, age, is_voter):
        self.aadhar = aadhar
        self.name = name
        self.party = party
        self.age = age
        self.is_voter = is_voter
        self.left = None
        self.right = None

class CandidateRegistration:
    def __init__(self):
        self.root = None

    def add_candidate(self, aadhar, name, party, age, is_voter):
        if len(aadhar) == 12 and aadhar.isdigit() and age >= 25 and is_voter:
            new_candidate = Candidate(aadhar, name, party, age, is_voter)
            if self.root is None:
                self.root = new_candidate
                print("Candidate registered successfully.")
            else:
                self._add_candidate_recursively(self.root, new_candidate)
                print("Candidate registered successfully.")
        else:
            print("Invalid candidate does not meet eligibility criteria.")

    def _add_candidate_recursively(self, current_node, new_candidate):
        if new_candidate.aadhar < current_node.aadhar:
            if current_node.left is None:
                current_node.left = new_candidate
            else:
                self._add_candidate_recursively(current_node.left, new_candidate)
        elif new_candidate.aadhar > current_node.aadhar:
            if current_node.right is None:
                current_node.right = new_candidate
            else:
                self._add_candidate_recursively(current_node.right, new_candidate)

    def search_candidate(self, aadhar):
        return self._search_candidate_recursively(self.root, aadhar)

    def _search_candidate_recursively(self, current_node, aadhar):
        if current_node is None or current_node.aadhar == aadhar:
            return current_node
        if aadhar < current_node.aadhar:
            return self._search_candidate_recursively(current_node.left, aadhar)
        return self._search_candidate_recursively(current_node.right, aadhar)

class VotersRegistration:
    def __init__(self):
        self.voters = {}

    def generate_voter_id(self, state, district):
        voter_id = f"{state:02d}{district:02d}"
        while True:
            random_digits = ''.join(random.choices('0123456789', k=4))
            voter_id += random_digits
            if voter_id not in self.voters:
                break
        return voter_id

    def register_voter(self, name, age, state, district):
        if age < 18:
            print("You are not eligible to vote.")
            return

        for voter_info in self.voters.values():
            if voter_info['name'] == name:
                print("This name is already registered.")
                return

        voter_id = self.generate_voter_id(state, district)

        self.voters[voter_id] = {'name': name, 'age': age, 'state': state, 'district': district, 'voted': False}
        print(f"Voter {name} with ID {voter_id} successfully registered.")

    def vote(self, voter_id):
        if voter_id in self.voters:
            if not self.voters[voter_id]['voted']:
                self.voters[voter_id]['voted'] = True
                print(f"Voter with ID {voter_id} has successfully voted.")
                return True
            else:
                print("This voter has already voted.")
        else:
            print("This voter is not registered.")
        return False

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, resident, booth, distance):
        if resident not in self.adj_list:
            self.adj_list[resident] = []
        if booth not in self.adj_list:
            self.adj_list[booth] = []
        self.adj_list[resident].append((booth, distance))
        self.adj_list[booth].append((resident, distance))

    def shortest_path(self, start, end):
        min_heap = [(0, start)]
        distances = {node: float('inf') for node in self.adj_list}
        distances[start] = 0

        while min_heap:
            current_dist, current_node = heapq.heappop(min_heap)

            if current_node == end:
                return distances[end]

            if current_dist > distances[current_node]:
                continue

            for neighbor, edge_weight in self.adj_list[current_node]:
                distance = current_dist + edge_weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(min_heap, (distance, neighbor))

        return float('inf')

class Node:
    def __init__(self, key, count):
        self.key = key
        self.count = count
        self.children = []

class Local:
    def __init__(self, bjp, cong, com):
        self.bjp = bjp
        self.cong = cong
        self.com = com

def build_tree(arr):
    def _build_tree(data, parent_count):
        for key, value in data.items():
            state_count = parent_count[:]
            state_node = Node(key, state_count)
            for local_obj in value:
                max_votes = max(local_obj.bjp, local_obj.cong, local_obj.com)
                if max_votes == local_obj.bjp:
                    state_count[0] += 1
                elif max_votes == local_obj.cong:
                    state_count[1] += 1
                else:
                    state_count[2] += 1
                district_node = Node("District", [local_obj.bjp, local_obj.cong, local_obj.com])
                state_node.children.append(district_node)
            return state_node

    root = Node("National", [0, 0, 0])
    national_counts = [0, 0, 0]
    for key, value in arr.items():
        state_node = _build_tree({key: value}, root.count)
        root.children.append(state_node)
        national_counts[0] += state_node.count[0]
        national_counts[1] += state_node.count[1]
        national_counts[2] += state_node.count[2]
    root.count = national_counts
    return root

def vote(root):
    print("Vote for your favorite party:")
    print("1. BJP")
    print("2. Congress")
    print("3. Communist")
    choice = int(input("Your Choice: "))

    if choice == 1:
        root.count[0] += 1
    elif choice == 2:
        root.count[1] += 1
    elif choice == 3:
        root.count[2] += 1
    else:
        print("Invalid choice")

def print_tree_leaf_to_root(node):
    if node is None:
        return
    for child in node.children:
        print_tree_leaf_to_root(child)
    print(node.key, node.count)

# Main menu driven loop
registration_system = CandidateRegistration()
voter_registry = VotersRegistration()
graph = Graph()
arr = {
    "tn": [Local(30, 40, 50), Local(20, 10, 15), Local(34, 67, 31), Local(14, 58, 33)],
    "kerala": [Local(33, 49, 50), Local(20, 30, 17), Local(34, 68, 54), Local(17, 22, 35)]
}
root = build_tree(arr)

while True:
    print("1. Candidate registration")
    print("2. Voters registration and booth allocation")
    print("3. Vote")
    print("4. Results")
    print("5. Exit")
    n = int(input("Your Choice: "))
    if n == 1:
        # Candidate registration
        aadhar_number = input("Enter Aadhar number: ")
        if len(aadhar_number) != 12 or not aadhar_number.isdigit():
            print("Invalid Aadhar number. Please enter a 12-digit number.")
        else:
            candidate_name = input("Enter candidate name: ")
            candidate_party = input("Enter candidate party: ")
            candidate_age = int(input("Enter candidate age: "))
            is_voter_str = input("Is the candidate a voter? (yes/no): ")
            is_voter = is_voter_str.lower() == 'yes'

            # Add candidate
            registration_system.add_candidate(aadhar_number, candidate_name, candidate_party, candidate_age, is_voter)

            # Searching for a candidate
            candidate = registration_system.search_candidate(aadhar_number)
            if candidate:
                print(f"Candidate {candidate.name} from {candidate.party} party found.")
            else:
                print("Candidate not found.")
    elif n == 2:
        # Voters registration and booth allocation
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        state = int(input("Enter your state (2-digit code): "))
        district = int(input("Enter your district (2-digit code): "))
        voter_registry.register_voter(name, age, state, district)
        # Booth allocation logic here
        # For now, let's assume it's integrated with voter registration
    elif n == 3:
        # Vote
        vote(root)
    elif n == 4:
        # Print the tree from leaf to root
        print_tree_leaf_to_root(root)
    elif n == 5:
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")