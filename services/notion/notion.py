from datetime import datetime
import json
import requests
import sys


class NotionClient:

    def __init__(self, token, database_id) -> None:
        self.token = token
        self.database_id = database_id
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def create_page(self, project_name,task,status, date):
        url = "https://api.notion.com/v1/pages"

        data = {
            "parent": {
                "database_id": self.database_id
            },
            "properties": {
                "Project Name": {
                    "title": [{
                        "text": {
                            "content": project_name
                        }
                    }]
                },
                "Task": {
                    "rich_text": [{
                        "text": {
                            "content": task
                        }
                    }]
                },
                "Status": {
                    "rich_text": [{
                        "text": {
                            "content": status
                        }
                    }]
                },
                "Date": {
                    "date": {
                        "start": date,
                        "end": None
                    }
                },
                
            }
        }

        data = json.dumps(data)
        res = requests.post(url=url, data=data, headers=self.headers)
        return res


if __name__ == "__main__":

    # setting path to import config
    sys.path.append('../../')
    import config

    notion_integration_token = config.NOTION_INTEGRATION_TOKEN
    notion_database_id = config.NOTION_DATABASE_ID
    print(notion_integration_token)
    print(notion_database_id)

    client = NotionClient(token=notion_integration_token,
                          database_id=notion_database_id)

    ## test project attributes
    time_now = datetime.now().astimezone().isoformat()
    status = "Active"
    project_name = "Test1"
    task = "nothing"

    ## sending post request
    res = client.create_page(project_name=project_name,task=task,status=status,date=time_now)

    #checking request response
    if res.status_code == 200:
        print("created successfully....!!!")
    else:
        print(f"error :-> status code = {res.status_code}")