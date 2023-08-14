import threading
import time
import logging

class Coordinator:
    def __init__(self):
        self.participants = []
    
    def add_participant(self, participant):
        self.participants.append(participant)
    
    def start(self):
        print("Coordinator: Starting 2PC")
        logging.error("err")
        # Phase 1: Prepare
        all_votes_commit = True
        for participant in self.participants:
            if not participant.prepare():
                all_votes_commit = False
        
        # Phase 2: Commit or Abort
        if all_votes_commit:
            for participant in self.participants:
                participant.commit()
        else:
            for participant in self.participants:
                participant.abort()
        
        print("Coordinator: 2PC completed")

class Participant:
    def __init__(self, name):
        self.name = name
        self.vote = None
    
    def prepare(self):
        print(f"{self.name}: Prepared")
        # Simulate participant's decision (commit or abort)
        # For demonstration purposes, we'll hard-code the decision here
        self.vote = "commit"  # Change to "abort" to simulate an abort decision
        return self.vote == "commit"
    
    def commit(self):
        if self.vote == "commit":
            print(f"{self.name}: Committing")
            # Simulate applying changes to local data
            time.sleep(2)
            print(f"{self.name}: Committed")
        else:
            print(f"{self.name}: Not committing")
    
    def abort(self):
        print(f"{self.name}: Aborting")
        
        # Simulate rolling back changes
        time.sleep(2)
        print(f"{self.name}: Aborted")

def main():
    coordinator = Coordinator()
    participant1 = Participant("Participant 1")
    participant2 = Participant("Participant 2")
    
    coordinator.add_participant(participant1)
    coordinator.add_participant(participant2)
    
    coordinator_thread = threading.Thread(target=coordinator.start)
    participant_threads = [
        threading.Thread(target=participant.prepare) for participant in coordinator.participants
    ]
    
    coordinator_thread.start()
    for thread in participant_threads:
        thread.start()
    
    coordinator_thread.join()
    for thread in participant_threads:
        thread.join()

if __name__ == "__main__":
    main()
