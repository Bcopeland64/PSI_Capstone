from src.tasks import tasks, add_task, complete_task, delete_task


def setup_function():
    tasks.clear()


def test_add_task():
    add_task("Study Python")

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Study Python"
    assert tasks[0]["completed"] is False


def test_complete_task():
    add_task("Study Linux")

    result = complete_task(1)

    assert result is True
    assert tasks[0]["completed"] is True


def test_delete_task():
    add_task("Study Networking")

    result = delete_task(1)

    assert result is True
    assert len(tasks) == 0