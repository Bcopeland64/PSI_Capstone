tasks = []


def add_task(task):
    tasks.append({
        "title": task,
        "completed": False
    })


def complete_task(number):
    if 1 <= number <= len(tasks):
        tasks[number - 1]["completed"] = True
        return True

    return False


def delete_task(number):
    if 1 <= number <= len(tasks):
        tasks.pop(number - 1)
        return True

    return False