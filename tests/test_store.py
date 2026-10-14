import pytest

from todo.store import TaskStore


def test_add_and_persist(tmp_path):
    path = tmp_path / "tasks.json"
    store = TaskStore(path)
    store.add("buy milk")
    store.add("write report")

    reloaded = TaskStore(path)
    assert [t["title"] for t in reloaded.tasks] == ["buy milk", "write report"]
    assert [t["id"] for t in reloaded.tasks] == [1, 2]


def test_complete_and_pending(tmp_path):
    store = TaskStore(tmp_path / "tasks.json")
    store.add("a")
    store.add("b")
    store.complete(1)
    assert [t["title"] for t in store.pending()] == ["b"]


def test_remove_missing_raises(tmp_path):
    store = TaskStore(tmp_path / "tasks.json")
    with pytest.raises(KeyError):
        store.remove(42)
