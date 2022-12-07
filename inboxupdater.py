import json, requests, uuid, os

token = os.environ['API_TOKEN']
destination = os.environ['DESTINATION_PROJECT']

projectsResponse = requests.post("https://api.todoist.com/sync/v9/sync", data={"sync_token":"*", "resource_types":'["projects"]'}, headers={"Authorization": "Bearer "+token}).json()
projects = projectsResponse['projects']

inboxId = [obj.get('id') for obj in projects if(obj['name'] == "Inbox")][0]
nowId = [obj.get('id') for obj in projects if(obj['name'] == destination)][0]

tasksResponse = requests.post("https://api.todoist.com/sync/v9/projects/get_data", data={"project_id":inboxId}, headers={"Authorization": "Bearer "+token}).json()

tasks = tasksResponse['items']

commands = []

for task in tasks:
    taskId = task.get('id')
    commands.append({
        "type": "item_update", 
        "uuid": str(uuid.uuid4()), 
        "args": {
            "id": taskId, 
            "due": {"string": "today"}
        }
    })
    commands.append({
        "type": "item_move",
        "uuid": str(uuid.uuid4()), 
        "args": {
            "id": taskId, 
            "project_id": nowId
        }
    })

batchResponse = requests.post("https://api.todoist.com/sync/v9/sync", data={"commands":json.dumps(commands)}, headers={"Authorization": "Bearer "+token}).json()

print(batchResponse)
