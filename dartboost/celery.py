# 아래는 우리가 작성한 celery.py 모듈이 라이브러리들과 충돌하여 
# 문제가 발생하지 않도록 돕습니다.
from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

def task_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                '*': state.event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)
# 커맨드라인에서 셀러리를 편하게 사용하기 위해 DJANGO_SETTINGS_MODULE 
# 환경 변수를 기본 값으로 설정했습니다.
# 이 구문이 꼭 필요한 것은 아니지만 항상 설정(settings) 모듈을 
# 셀러리 프로그램에 전달하도록 해주기 때문에 시간을 절약할 수 있습니다. 
# 다음에 나올 app 인스턴스 생성보다 반드시 앞서 설정해야 한다는 점, 기억하세요.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dartboost.settings')

#'셀러리' 프로그램을 위해 기본 장고 설정파일을 설정합니다.

# 인스턴스를 만듭니다. 인스턴스를 여러 개 만들 수 있지만 
# 장고를 사용하는 경우에는 굳이 그럴 필요없이 하나로 충분합니다.
app = Celery('dartboost')

#여기서 문자열을 사용하는 것은 워커(worker)가 자식 프로세스로 설정 객체를 직렬화(serialize)하지 않아도 된다는 뜻입니다.  
#뒤에 namespace='CELERY'는 모든 셀러리 관련 설정 키는 'CELERY_' 라는 접두어를 가져야 한다고 알려줍니다.  
app.config_from_object('django.conf:settings', namespace='CELERY')  

#등록된 장고 앱 설정에서 task를 불러옵니다.  
app.autodiscover_tasks()
task_monitor(app)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))