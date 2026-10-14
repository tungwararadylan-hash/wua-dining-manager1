# BEFORE refactoring: one messy function doing everything (Lab 7 starting point)
def process(kind, id, hall, queue, meal, tickets):
    if kind == "student":
        limit = 2
        label = "Student"
    elif kind == "staff":
        limit = 1
        label = "Staff"
    elif kind == "admin":
        limit = 0
        label = "Admin"
    else:
        return "bad user"
    if id in tickets and tickets[id] >= limit:
        return "no more meals"
    tickets[id] = tickets.get(id, 0) + 1
    queue.append(id)
    print("Queue length is now", len(queue))      # hard-coded notification
    if len(queue) > 50:
        print("ALERT: kitchen, queue too long")   # duplicated alert logic
    print(label, id, "served at", hall, meal)
    return "ok"
