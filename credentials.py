import os
from keystoneauth1.identity import v3
from keystoneauth1 import session

class Credentials:
    def __init__(self):
        self.auth_url = os.environ['OS_AUTH_URL']
        self.username = os.environ['OS_USERNAME']
        self.password = os.environ['OS_PASSWORD']
        self.project_name = os.environ['OS_PROJECT_NAME']
        self.user_domain_id='default'
        self.project_domain_id='default'

    def get_token(self):
        auth = v3.Password(auth_url=self.auth_url,
                            username=self.username,
                            password=self.password,
                            project_name=self.project_name,
                            user_domain_id=self.user_domain_id,
                            project_domain_id=self.project_domain_id)
        sess = session.Session(auth=auth)
        token = auth.get_token(sess)
        return token

def main():
    creds = Credentials()
    print( creds.get_token() )

if __name__ == "__main__":
    main()
