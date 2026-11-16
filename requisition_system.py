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
            elif normalized == "not approved":
                self.status = "Not approved"
                self.approval_ref = "Not available"
            else:
                print(f"Invalid decision '{decision}' for Requisition {self.requisition_id}.")

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
    # --- Requisitions 1 to 7 ---
    req1 = RequisitionSystem("03/04/2024", "FN19", "John Paul")
    req1.add_requisition([("Office Chair", 250), ("Desk Lamp", 200)])  # $450 -> Auto-Approved

    req2 = RequisitionSystem("05/04/2024", "FN20", "Tracy Brown")
    req2.add_requisition([("Laptop", 1000)])  # $1000 -> Pending

    req3 = RequisitionSystem("07/05/2024", "FN15", "Emma Wellington")
    req3.add_requisition([("Server Rack", 2500), ("UPS Battery", 1000)])  # $3500 -> Pending

    req4 = RequisitionSystem("03/05/2024", "FN02", "Catlin White")
    req4.add_requisition([("Monitor Stand", 190), ("Keyboard", 300)])  # $490 -> Auto-Approved

    req5 = RequisitionSystem("10/05/2024", "FN08", "Liam Patel")
    req5.add_requisition([("Standing Desk", 650)])  # $650 -> Pending

    req6 = RequisitionSystem("12/05/2024", "FN22", "Sophia Chen")
    req6.add_requisition([("Printer Toner", 150), ("A4 Paper Box", 80)])  # $230 -> Auto-Approved

    req7 = RequisitionSystem("14/05/2024", "FN11", "Noah Williams")
    req7.add_requisition([("External Monitor", 500)])  # $500 (Boundary case) -> Pending

    print("--- INITIAL REQUISITIONS & STATISTICS (7 SUBMISSIONS) ---")
    RequisitionSystem.display_requisitions()
    RequisitionSystem.requisition_statistics()

    # Manager reviews selected pending requisitions (total > $499)
    # Leave req2 ($1000) as Pending
    req3.respond_requisition("Not approved")
    req5.respond_requisition("Approved")
    req7.respond_requisition("Approved")

    print("--- UPDATED REQUISITIONS & STATISTICS AFTER MANAGER REVIEW ---")
    RequisitionSystem.display_requisitions()
    RequisitionSystem.requisition_statistics()