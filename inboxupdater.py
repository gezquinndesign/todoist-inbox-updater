import json, requests, uuid, todoist
##from todoist.api import TodoistAPI

token = "dd7679bad6a4558c8e23f753d3f30adf31008dc2";
projects = requests.get("https://beta.todoist.com/API/v8/projects", params={"token": token}).json()
dict = projects
inboxId = [obj.get('id') for obj in projects if(obj['name'] == 'Inbox')]
nowId = [obj.get('id') for obj in projects if(obj['name'] == 'NOW')]
filter = "no date"

tasks = requests.get("https://beta.todoist.com/API/v8/tasks", params={"token": token, "project_id": inboxId, "filter": filter}).json()

for task in tasks:
    taskId = task.get('id')
    requests.post("https://beta.todoist.com/API/v8/tasks/%s" % taskId,
        params={"token": token},
        data=json.dumps({"due_string": "today"}),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
        }
    )

tasks = requests.get("https://beta.todoist.com/API/v8/tasks", params={"token": token, "project_id": inboxId}).json()
for task in tasks:
    taskId = task.get('id')
    api = todoist.TodoistAPI(token)
    api.sync()
    item = api.items.get_by_id(taskId)
    item.move(nowId[0])
    api.commit()
