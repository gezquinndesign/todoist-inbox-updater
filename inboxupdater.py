import json, requests, uuid, os

from todoist.api import TodoistAPI

token = os.environ['API_TOKEN']
destination = os.environ['DESTINATION_PROJECT']
projects = requests.get("https://api.todoist.com/rest/v1/projects", params={"token": token}).json()
dict = projects
inboxId = [obj.get('id') for obj in projects if(obj['name'] == 'Inbox')]
nowId = [obj.get('id') for obj in projects if(obj['name'] == destination)]
filter = "no date"

tasks = requests.get("https://api.todoist.com/rest/v1/tasks", params={"token": token, "project_id": inboxId, "filter": filter}).json()

for task in tasks:
    taskId = task.get('id')
    requests.post("https://api.todoist.com/rest/v1/tasks/%s" % taskId,
        params={"token": token},
        data=json.dumps({"due_string": "today"}),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
        }
    )

tasks = requests.get("https://api.todoist.com/rest/v1/tasks", params={"token": token, "project_id": inboxId}).json()
for task in tasks:
    taskId = task.get('id')
    api = TodoistAPI(token)
    api.sync()
    item = api.items.get_by_id(taskId)
    item.move(project_id=nowId[0])
    api.commit()
