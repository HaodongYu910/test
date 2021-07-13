from github import Github


class GitMethod:
    """
       git api 仓库获取 信息
       github 文档  https://pygithub.readthedocs.io/en/latest/introduction.html
    """

    def __init__(self):
        self.g = Github(base_url="https://git.biomind.com.cn/api/v3",
                        login_or_token="5a705c7de4dcf30f12ae8a6c706753ed1c8fe81d")

    # g = Github('github.dev@biomind.ai', 'cr4ckm3PL5').get_user()
    # for repo in g.get_user().get_repos():
    #     print(repo.name)
    # 获取项目分支信息
    def gitBranch(self, project):
        branchList = []

        repo = self.g.get_repo(project)
        for i in repo.get_branches():
            branchList.append(i.name)
        return branchList

    def commitInfo(self, project, branch):
        branch = self.g.get_repo(project).get_branch(branch)
        print(branch.commit)

# if __name__ == '__main__':
#     g = GitMethod()
#     print(g.gitBranch("AI-Platform/Biomind-Radiology"))
#
#     print(print(g.commitInfo("AI-Platform/Biomind-Radiology", "master")))
