import sys
import threading
import time
from datetime import datetime, time as dt_time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import users
from jd_user import JDUser

max_thread = 100


def thread_task(user, sku_id):
    user.secskill(sku_id)


def appoint_task(users, sku_id):
    for user in users:
        user.appoint(sku_id)


def secskill_task(users, sku_id):
    threads = []
    start_time = dt_time(11, 59, 59)
    end_time = dt_time(12, 0, 5)
    while True:
        now = datetime.now().time()
        if now >= start_time:
            if threading.active_count() < max_thread + 1:
                for user in users:
                    thread = threading.Thread(target=thread_task, args=(user, sku_id))
                    threads.append(thread)
                    thread.start()
                time.sleep(0.2)
        if now >= end_time:
            break
    for thread in threads:
        thread.join()
    print('all done')


if __name__ == '__main__':
    # 茅台53度 1499 100012043978
    # 华为Mate60Pro 12GB+512GB 雅川青 6999 100064695864
    sku_id = '100012043978'

    # sxz = JDUser(users.users[0])
    # sxz.secskill(sku_id)

    # 初始化用户
    jd_users = []
    for user in users.users:
        jd_user = JDUser(user)
        jd_users.append(jd_user)

    scheduler = BackgroundScheduler()
    scheduler.add_job(appoint_task, args=[jd_users, sku_id], trigger=CronTrigger(day='*', hour="10", minute='5'),
                      misfire_grace_time=None)
    scheduler.add_job(secskill_task, args=[jd_users, sku_id], trigger=CronTrigger(day='*', hour="11", minute='59'),
                      misfire_grace_time=None)
    scheduler.start()

    # # 预约
    # for user in jd_users:
    #     user.appoint(sku_id)
    #
    # target_time = dt_time(11, 59)
    # while True:
    #     now = datetime.now().time()
    #     if now >= target_time:
    #         break
    #     time.sleep(60)
    #
    # # 抢购
    # threads = []
    # start_time = dt_time(11, 59, 59)
    # end_time = dt_time(12, 0, 5)
    # while True:
    #     now = datetime.now().time()
    #     if now >= start_time:
    #         if threading.active_count() < max_thread + 1:
    #             for user in jd_users:
    #                 thread = threading.Thread(target=thread_task, args=(user, sku_id))
    #                 threads.append(thread)
    #                 thread.start()
    #             time.sleep(0.2)
    #     if now >= end_time:
    #         break
    # for thread in threads:
    #     thread.join()
    # print('all done')

    sys.stdin.read()
