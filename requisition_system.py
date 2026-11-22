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
        total_cost = 0.0
        for item in items_with_costs:
            total_cost += item[1]
        self.total = total_cost
        self.approve_requisition()
        return self.total

    def approve_requisition(self):
        if self.total < 500:
            self.status = "Approved"
            id_str = str(self.requisition_id)
            self.approval_ref = f"{self.staff_id}{id_str[-3:]}"
        else:
            self.status = "Pending"
            self.approval_ref = "Not available"

    def respond_requisition(self, decision):
        if self.status == "Pending":
            normalized = decision.strip().lower()
            if normalized == "approved":
                self.status = "Approved"
                id_str = str(self.requisition_id)
                self.approval_ref = f"{self.staff_id}{id_str[-3:]}"
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
        if self.total % 1 == 0:
            formatted_total = int(self.total)
        else:
            formatted_total = f"{self.total:.2f}"
        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: ${formatted_total}")
        print(f"Status: {self.status}")
        print(f"Approval Reference Number: {self.approval_ref}\n")

    def display_requisitions(self):
        if len(RequisitionSystem.all_requisitions) == 0:
            print("\nNo requisitions submitted yet.\n")
            return
        print("\n--- ALL REQUISITIONS ---")
        for req in RequisitionSystem.all_requisitions:
            req.display_details()

    def requisition_statistics(self):
        total_submitted = len(RequisitionSystem.all_requisitions)
        approved_count = 0
        pending_count = 0
        not_approved_count = 0

        for r in RequisitionSystem.all_requisitions:
            if r.status == "Approved":
                approved_count += 1
            elif r.status == "Pending":
                pending_count += 1
            elif r.status == "Not approved":
                not_approved_count += 1

        print("Statistics:")
        print("Displaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {total_submitted}")
        print(f"The total number of approved requisitions: {approved_count}")
        print(f"The total number of pending requisitions: {pending_count}")
        print(f"The total number of not approved requisitions: {not_approved_count}\n")


# Main interactive program (Script mode)
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
            if item_name == "":
                if len(items_with_costs) == 0:
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
        pending_reqs = []
        for r in RequisitionSystem.all_requisitions:
            if r.status == "Pending":
                pending_reqs.append(r)

        if len(pending_reqs) == 0:
            print("\nThere are no pending requisitions to review.\n")
            continue

        print("\nPending Requisitions:")
        for r in pending_reqs:
            if r.total % 1 == 0:
                formatted_total = int(r.total)
            else:
                formatted_total = f"{r.total:.2f}"
            print(f" - ID: {r.requisition_id} | Staff: {r.staff_name} ({r.staff_id}) | Total: ${formatted_total}")

        try:
            target_id = int(input("\nEnter the Requisition ID to review: ").strip())
            matched_req = None
            for r in RequisitionSystem.all_requisitions:
                if r.requisition_id == target_id:
                    matched_req = r
                    break

            if matched_req is not None:
                decision = input("Enter decision (Approved / Not approved): ").strip()
                matched_req.respond_requisition(decision)
                print()
            else:
                print(f"Requisition ID {target_id} not found.\n")
        except ValueError:
            print("Invalid Requisition ID. Please enter a number.\n")

    elif choice == "3":
        if len(RequisitionSystem.all_requisitions) == 0:
            print("\nNo requisitions submitted yet.\n")
        else:
            RequisitionSystem.all_requisitions[0].display_requisitions()

    elif choice == "4":
        print()
        if len(RequisitionSystem.all_requisitions) == 0:
            print("Statistics:")
            print("Displaying the Requisition Statistics")
            print("The total number of requisitions submitted: 0")
            print("The total number of approved requisitions: 0")
            print("The total number of pending requisitions: 0")
            print("The total number of not approved requisitions: 0\n")
        else:
            RequisitionSystem.all_requisitions[0].requisition_statistics()

    elif choice == "5":
        print("Exiting Requisition System.")
        print("Thank You")
        print("Regards,")
        print("Pranshu Soni")
        print("Student ID: 20260122")
        break

    else:
        print("Invalid choice. Please select an option between 1 and 5.\n")