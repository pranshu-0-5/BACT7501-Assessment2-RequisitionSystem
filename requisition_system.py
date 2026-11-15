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