class RequisitionSystem:
    requisition_counter = 10000
    all_requisitions = []

    def __init__(self, date, staff_id, staff_name):
        RequisitionSystem.requisition_counter += 1
        self.requisition_id = RequisitionSystem.requisition_counter
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.items = []
        self.total = 0.0
        self.status = "Pending"
        self.approval_ref = "Not available"
        RequisitionSystem.all_requisitions.append(self)

    def add_requisition(self, items_with_costs):
        self.items = items_with_costs
        self.total = sum(cost for _, cost in items_with_costs)
        self.approve_requisition()
        return self.total

    def approve_requisition(self):
        if self.total < 500:
            self.status = "Approved"
            self.approval_ref = f"{self.staff_id}{str(self.requisition_id)[-3:]}"
        else:
            self.status = "Pending"
            self.approval_ref = "Not available"

    def respond_requisition(self, decision):
        if self.status == "Pending":
            normalized = decision.strip().lower()
            if normalized == "approved":
                self.status = "Approved"
                self.approval_ref = f"{self.staff_id}{str(self.requisition_id)[-3:]}"
                print(f"Requisition {self.requisition_id} has been Approved.")
            elif normalized == "not approved":
                self.status = "Not approved"
                self.approval_ref = "Not available"
                print(f"Requisition {self.requisition_id} has been marked as Not approved.")
            else:
                print(f"Invalid decision '{decision}'. Please enter 'Approved' or 'Not approved'.")
        else:
            print(f"Requisition {self.requisition_id} is already '{self.status}' and does not require manager review.")

    def display_details(self):
        formatted_total = int(self.total) if self.total.is_integer() else f"{self.total:.2f}"
        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: ${formatted_total}")
        print(f"Status: {self.status}")
        print(f"Approval Reference Number: {self.approval_ref}\n")

    @classmethod
    def display_requisitions(cls):
        if not cls.all_requisitions:
            print("\nNo requisitions submitted yet.\n")
            return
        print("\n--- ALL REQUISITIONS ---")
        for req in cls.all_requisitions:
            req.display_details()

    @classmethod
    def requisition_statistics(cls):
        total_submitted = len(cls.all_requisitions)
        approved_count = sum(1 for r in cls.all_requisitions if r.status == "Approved")
        pending_count = sum(1 for r in cls.all_requisitions if r.status == "Pending")
        not_approved_count = sum(1 for r in cls.all_requisitions if r.status == "Not approved")

        print("Statistics:")
        print("Displaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {total_submitted}")
        print(f"The total number of approved requisitions: {approved_count}")
        print(f"The total number of pending requisitions: {pending_count}")
        print(f"The total number of not approved requisitions: {not_approved_count}\n")


if __name__ == "__main__":
    while True:
        print("=== Requisition System Menu ===")
        print("1. Submit a new requisition")
        print("2. Manager review (Respond to a pending requisition)")
        print("3. Display all requisitions")
        print("4. Display requisition statistics")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            date = input("Enter Date (DD/MM/YYYY): ").strip()
            staff_id = input("Enter Staff ID (e.g., FN19): ").strip()
            staff_name = input("Enter Staff Name: ").strip()

            items_with_costs = []
            while True:
                item_name = input("Enter item name (or press Enter to finish adding items): ").strip()
                if not item_name:
                    if not items_with_costs:
                        print("You must add at least one item.")
                        continue
                    break

                while True:
                    try:
                        cost = float(input(f"Enter cost for '{item_name}': $").strip())
                        if cost < 0:
                            print("Cost cannot be negative. Try again.")
                            continue
                        items_with_costs.append((item_name, cost))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a numeric cost.")

            req = RequisitionSystem(date, staff_id, staff_name)
            req.add_requisition(items_with_costs)
            print(f"\nRequisition {req.requisition_id} submitted! Current Status: {req.status}\n")

        elif choice == "2":
            pending_reqs = [r for r in RequisitionSystem.all_requisitions if r.status == "Pending"]
            if not pending_reqs:
                print("\nThere are no pending requisitions to review.\n")
                continue

            print("\nPending Requisitions:")
            for r in pending_reqs:
                formatted_total = int(r.total) if r.total.is_integer() else f"{r.total:.2f}"
                print(f" - ID: {r.requisition_id} | Staff: {r.staff_name} ({r.staff_id}) | Total: ${formatted_total}")

            try:
                target_id = int(input("\nEnter the Requisition ID to review: ").strip())
                matched_req = next((r for r in RequisitionSystem.all_requisitions if r.requisition_id == target_id), None)

                if matched_req:
                    decision = input("Enter decision (Approved / Not approved): ").strip()
                    matched_req.respond_requisition(decision)
                    print()
                else:
                    print(f"Requisition ID {target_id} not found.\n")
            except ValueError:
                print("Invalid Requisition ID. Please enter a number.\n")

        elif choice == "3":
            RequisitionSystem.display_requisitions()

        elif choice == "4":
            print()
            RequisitionSystem.requisition_statistics()

        elif choice == "5":
            print("Exiting Requisition System. Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option between 1 and 5.\n")