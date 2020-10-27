import gitlab
class GitlabAPI(object):
    """
    参数为gitlab仓库地址和个人private_take
    """
    def __init__(self, *args, **kwargs):
        self.gl = gitlab.Gitlab('http://git.midea.com', private_token='wjssRFSQGe2KXxyhbxaj', api_version='3')

    def get_user_id(self, username):
        """
        通过用户名获取用户id
        :param username:
        :return:
        """
        user = self.gl.users.get_by_username(username)
        return user.id

    def get_group_id(self, groupname):
        """
        通过组名获取组id
        :param groupname:
        :return:
        """
        group = self.gl.groups.get(groupname, all=True)
        return group.id

    def get_user_projects(self, userid):
        """
        获取用户所拥有的项目
        :param userid:
        :return:
        """
        projects = self.gl.projects.owned(userid=userid, all=True)
        result_list = []
        for project in projects:
            result_list.append(project.http_url_to_repo)
        return result_list

    def get_group_projects(self, groupname):
        """
        获取组内项目！！！！！！！其他博客也有类似方法，实测不能拿到群组内项目，现经过小改动，亲测可满足要求
        :param groupname:
        :return:
        """
        group = self.gl.groups.get(groupname, all=True)
        projects = group.projects.list(all=True)
        return projects


    def getContent(self, projectID):
        """
        通过项目id获取文件内容
        :param projectID:
        :return:
        """
        projects =self.gl.projects.get(projectID)
        f = projects.files.get(file_path='指定项目中的文件路径', ref='master')
        content = f.decode()
        # print(content)
        return content.decode('utf-8')

    def get_all_group(self):
        """
        获取所有群组
        :return:
        """
        return self.gl.groups.list(all=True)

if __name__ == '__main__':
    gitlab = GitlabAPI()
    print(gitlab.get_user_id('何伟宏'))