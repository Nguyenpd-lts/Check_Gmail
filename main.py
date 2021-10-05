import os
import threading
from hotmail_verified import Hotmail_Veri
import queue
from optsim import _OTPSim
import configparser


def _desktop_work_size():
    # return [1600, 870]
    from win32api import GetMonitorInfo, MonitorFromPoint
    monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
    work_area = monitor_info.get("Work")
    return [work_area[2], work_area[3]]

# Desktop\Learn-Tool\Python\InstaPy>
class AppMain:
    def __init__(self):
        self.accounts = []
        self.input_list = []
        self.task_list = []

        self.log_queue = queue.Queue()
        self.task_queue = []

        conf = configparser.ConfigParser()
        conf.read('config.ini')

        self.max_thread = int(conf['Main']['MaxThreads'])

    def read_accounts(self):
        with open('input.txt', encoding='utf-8', mode='r') as f:
            contents = f.read()
            self.input_list = contents.splitlines()
        self.paser_account()
        
    def paser_account(self):
        for _ in self.input_list:
            tt = _.split("|")
            self.accounts.append({
                "email": tt[0],
                "pwd": tt[1],
            })
        if len(self.accounts) == 0:
            input(" no data")
            exit(0)
        
    def run(self):
        print('>>> Initializing....')
        self.read_accounts()

        t = threading.Thread(target=self.monitor_log)
        t.setDaemon(True)
        t.start()

        print("> Processing")
        os.system('cls')
        # print(self.log_queue)
        # SET POS
        work_rows = 2
        work_colums = 5
        margin_s = 4
        margin_w = 2
        padding_s = 8
        padding_h = 8

        desktop_work_size = _desktop_work_size()
        desktop_width = desktop_work_size[0]
        desktop_height = desktop_work_size[1]

        work_width = desktop_width - margin_s * 2
        work_height = desktop_height - padding_s * 2

        per_width = int((work_width - (work_colums - 1)
                         * margin_w) / work_colums)
        per_height = int(
            (work_height - (work_rows - 1) * padding_h) / work_rows)

        org_left = margin_s
        org_top = padding_s
        current_colum = 1
        current_row = 1
        count = 1
        # SET POS

        size  = self.max_thread
        # tt_chunks = [self.accounts[i:i + size] for i in range(0, len(self.accounts), size)]
        # print(tt_chunks)
        tt_chunks = []
        for i in range(0, len(self.accounts), size):
            tt_chunks.append(self.accounts[i:i + size])
        _c = 1
        _t = 1
        for tt in tt_chunks:
            _c += 1
            for acc in tt:
                if current_colum % (work_colums+1) == 0:
                    current_colum = 1
                    current_row += 1
                if count % (work_colums*work_rows+1) == 0:
                    current_colum = 1
                    current_row = 1

                pos = [org_left + (per_width + margin_w) * (current_colum - 1),
                    org_top + (per_height + padding_h) * (current_row - 1),
                    per_width,
                    per_height]

                current_colum += 1
                count += 1
                self.register_task(acc, pos)

            self.exec_tasks_wait()
            self.task_list = []
            count = 1
            current_colum = 1
            current_row = 1

    def monitor_log(self):
        while True:
            t = self.log_queue.get()
            out_file = 'output_success.txt'
            print('t' + str(t))
            c = t['_id']
            done = t['_success']
            m = t['acc']
            print(c, m)
            if not done:
                out_file = 'output_failed.txt'
            text = m['email'] + "|" + m["pwd"]
            print(text, "-->", str(c) + "|" + str(done))
            with open(out_file, mode='a+', encoding='utf-8') as f:
                f.write(text + '\n')

    def register_task(self, acc, pos):
        # print(acc)
        worker = threading.Thread(target=self.run_per_task, args=(acc, pos,))
        worker.setDaemon(True)
        self.task_list.append(worker)

    def exec_tasks_wait(self):
        for w in self.task_list:
            w.start()
        
        for w in self.task_list:
            w.join()

    def run_per_task(self, acc, pos):
        try:
            print('Acc Check: ' + str(acc))
            ins = Hotmail_Veri(email=acc["email"], pwd=acc["pwd"], w_position=pos)
            _id, _success = ins.run()
            self.log_queue.put({
                "acc": acc,
                "_id": _id,
                "_success": _success
            })
            del ins
        except Exception as e:
            print('Error:' + str(e))

    def test_otp(self):
        print(self)
        self.otp_sim = _OTPSim(api_key='0253e78da675579c2fd5a54c86e019ae')
        self.otp_sim.run()
        self.phone = '0{}'.format(self.otp_sim.phone)

if __name__=="__main__":
    try:
        print('Start')
        ins = AppMain()
        ins.run()

    except Exception as e:
        input('>>> ERR' + str(e))
