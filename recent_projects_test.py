import unittest
from unittest import mock

from recent_projects import create_json, Project, find_app_data, find_recentprojects_file, read_projects_from_file, \
    filter_and_sort_projects


class Unittests(unittest.TestCase):
    def setUp(self):
        self.recentProjectsPath = '/Users/JohnSnow/Library/Application Support' \
                                  '/JetBrains/IntelliJIdea2020.2/options/recentProjects.xml'
        self.example_projects_paths = ["~/Documents/spring-petclinic", "~/Desktop/trash/My Project (42)"]

        with mock.patch("os.path.expanduser") as mock_expanduser:
            mock_expanduser.return_value = '/Users/JohnSnow/Documents/spring-petclinic'
            self.example_project = Project(self.example_projects_paths[0])

    @mock.patch('os.path.isfile')
    def test_create_json(self, mock_isfile):
        mock_isfile.return_value = False
        expected = '{"variables": {"bundle_id": "app_name"}, ' \
                   '"items": [{"title": "spring-petclinic", ' \
                   '"subtitle": "~/Documents/spring-petclinic", ' \
                   '"arg": "~/Documents/spring-petclinic", ' \
                   '"type": "file"}]}'
        self.assertEqual(expected, create_json([self.example_project], "app_name"))

    @mock.patch("os.path.expanduser")
    @mock.patch('os.path.isfile')
    @mock.patch("builtins.open", mock.mock_open(read_data="custom_project_name"))
    def test_create_json_from_custom_name(self, mock_isfile, mock_expand_user):
        mock_expand_user.return_value = '/Users/JohnSnow/Documents/spring-petclinic'
        mock_isfile.return_value = True
        expected = '{"variables": {"bundle_id": "app_name"}, ' \
                   '"items": [{"title": "custom_project_name", ' \
                   '"subtitle": "~/Documents/spring-petclinic", ' \
                   '"arg": "~/Documents/spring-petclinic", ' \
                   '"type": "file"}]}'
        self.assertEqual(expected, create_json([Project("~/Documents/spring-petclinic")], "app_name"))

    @mock.patch("builtins.open", mock.mock_open(read_data='{"clion": {"bundle_id": "com.jetbrains.clion", "folder_name": "CLion"}}'))
    def test_read_app_data(self):
        self.assertEqual(find_app_data("clion"), {
            "folder_name": "CLion",
            "bundle_id": "com.jetbrains.clion"
        })

        with self.assertRaises(SystemExit) as exitcode:
            find_app_data("rider")
        self.assertEqual(exitcode.exception.code, 1)

    @mock.patch("builtins.open")
    def test_read_app_data_products_file_missing(self, mock_open):
        mock_open.side_effect = IOError()
        with self.assertRaises(SystemExit) as exitcode:
            find_app_data("clion")
        self.assertEqual(exitcode.exception.code, 1)

    @mock.patch("os.path.expanduser")
    @mock.patch("os.walk")
    def test_find_recent_files_xml(self, mock_walk, expand_user):
        expand_user.return_value = '/Users/JohnSnow/Library/Application Support/JetBrains/'
        mock_walk.return_value = iter([
            ('/Path',
             ['IntelliJIdea2020.1',
              'IntelliJIdea2020.2',
              'IntelliJIdea2020.2-backup',
              'GoLand2020.1',
              'GoLand2020.2'], []),
        ])
        """Happy Flow"""
        self.assertEqual(find_recentprojects_file({"folder_name": "IntelliJIdea"}),
                         self.recentProjectsPath)

    @mock.patch("os.path.expanduser")
    @mock.patch("os.walk")
    def test_find_recent_files_xml_android_studio(self, mock_walk, expand_user):
        expand_user.return_value = '/Users/JohnSnow/Library/Application Support/Google/'
        mock_walk.return_value = iter([
            ('/Path',
             ['AndroidStudio4.0',
              'AndroidStudio4.1',
              'Chrome'], []),
        ])
        """Happy Flow"""
        self.assertEqual(
            find_recentprojects_file({"folder_name": "AndroidStudio"}),
            '/Users/JohnSnow/Library/Application Support/Google/AndroidStudio4.1/options/recentProjects.xml')

    @mock.patch("builtins.open", mock.mock_open(
        read_data='<application>'
                  '<component name="RecentProjectsManager">'
                  '<option name="additionalInfo">'
                  '<map>'
                  '<entry key="$USER_HOME$/Desktop/trash/My Project (42)" />'
                  '<entry key="$USER_HOME$/Documents/spring-petclinic" />'
                  '</map>'
                  '</option>'
                  '</component>'
                  '</application>'))
    def test_read_projects(self):
        self.assertEqual(list(read_projects_from_file(self.recentProjectsPath)), self.example_projects_paths)

    def test_filter_projects(self):
        projects = list(map(Project, self.example_projects_paths))
        self.assertEqual([Project(self.example_projects_paths[0])], filter_and_sort_projects("petclinic", projects))

    def test_filter_projects_no_query(self):
        projects = list(map(Project, self.example_projects_paths))
        self.assertEqual(filter_and_sort_projects("", projects), projects)

    def test_project_equals(self):
        project = Project(self.example_projects_paths[0])
        self.assertTrue(project == Project("~/Documents/spring-petclinic"))
        self.assertFalse(project == "some-other-object")

    def test_project_sort_on_match_type(self):
        project = Project(self.example_projects_paths[0])
        self.assertEqual(project.sort_on_match_type("sp"), 0)
        self.assertEqual(project.sort_on_match_type("spring-petclinic"), 1)
        self.assertEqual(project.sort_on_match_type("foobar"), 2)


if __name__ == '__main__':  # pragma: nocover
    unittest.main()
