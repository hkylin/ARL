import unittest
from app import celerytask
from app.utils import conn_db as conn

task_data = {
    'name': '自动化测试',
    'target': '10.0.83.6',
    'start_time': '-',
    'status': 'waiting',
    'type': 'ip',
    'options': {
        'domain_brute': True,
        'domain_brute_type': 'test',
        'port_scan_type': 'test',
        'port_scan': True,
        'service_detection': False,
        'service_brute': False,
        'os_detection': False,
        'site_identify': True,
        'site_capture': False,
        'file_leak': False,
        'alt_dns': False,
        'url_spider': False,
        'ssl_cert': False,
        'fetch_api_path': False,
        'fofa_search': False,
    }
}


def submit_task(task_data):
    conn('task').insert_one(task_data)
    task_id = str(task_data.pop("_id"))
    task_data["task_id"] = task_id
    celerytask.arl_task(options=task_data)

    return task_data

class TestExecTask(unittest.TestCase):
    def test_exec_task(self):
        submit_task(task_data)
        query = {"task_id": task_data["task_id"]}

        if task_data["options"]["port_scan"]:
            self.assertTrue(len(list(conn("site").find(query))) >= 1)
            self.assertTrue(len(list(conn("ip").find(query))) >= 1)


if __name__ == '__main__':
    unittest.main()