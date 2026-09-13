from src.logic import analyze_process, get_recent_files
from src.utils import calculate_sha256

def test_analyze_normal_process():
    process = {
        "name": "test.exe",
        "exe": "C:\\Program Files\\test.exe",
        "status": "running"
    }

    risk, reasons = analyze_process(process)

    assert risk == "NORMAL"
    assert reasons == []

def test_analyze_process_from_temp():
    process = {
        "name": "test.exe",
        "exe": "C:\\Users\\Test\\AppData\\Local\\Temp\\test.exe",
        "status": "running"
    }

    risk, reasons = analyze_process(process)

    assert risk == "REVIEW"
    assert "Executable is running from a temporary folder" in reasons


def test_calculate_sha256(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    file_hash = calculate_sha256(test_file)

    assert file_hash == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

def test_get_recent_files(tmp_path):
    test_file = tmp_path / "recent.txt"
    test_file.write_text("hello")

    recent_files = get_recent_files(tmp_path)

    assert len(recent_files) == 1
    assert recent_files[0]["path"] == str(test_file)
    assert "modified_time" in recent_files[0]

    